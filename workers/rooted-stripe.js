// ROOTED Stripe Worker — Cloudflare Worker backend
//
// SOURCE OF RECORD. This file was previously only in Cloudflare, meaning the deployed
// Worker had no version history and no diff. Retrieved from Cloudflare on 6 Aug 2026 and
// committed here. Edit this file, then paste into Cloudflare — not the other way round.
//
// Pricing model: Free, and Member at $10/month or one annual price.
// (An earlier three-tier model with a $19 Premium is retired — do not reintroduce it.)
//
//   POST /create-checkout-session  → starts a Member subscription, monthly or annual
//   POST /create-portal-session    → lets an existing member manage/cancel
//   POST /webhook                  → Stripe calls this on payment events; syncs Supabase
//
// Required secrets (Settings → Variables and Secrets, all type "Secret"):
//   STRIPE_SECRET_KEY          — sk_live_... (or sk_test_... while testing)
//   STRIPE_WEBHOOK_SECRET      — whsec_..., shown when you create the webhook in Stripe
//   STRIPE_PRICE_ID            — price_..., the $10/mo recurring Price
//   STRIPE_PRICE_ID_ANNUAL     — price_..., the annual recurring Price   [NEW]
//   SUPABASE_URL               — same value as SUPABASE_URL in Index.html
//   SUPABASE_SERVICE_ROLE_KEY  — Supabase Settings → API. NOT the anon key; this one
//                                bypasses Row Level Security and must never reach the client
//   SITE_URL                   — e.g. https://rootedapproved.com

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Stripe-Signature',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      if (url.pathname === '/create-checkout-session' && request.method === 'POST') {
        return await createCheckoutSession(request, env, corsHeaders);
      }
      if (url.pathname === '/create-portal-session' && request.method === 'POST') {
        return await createPortalSession(request, env, corsHeaders);
      }
      if (url.pathname === '/webhook' && request.method === 'POST') {
        return await handleWebhook(request, env, corsHeaders);
      }
      return new Response(JSON.stringify({ error: 'Not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    } catch (e) {
      console.error('Worker error:', e);
      // Surface the real reason rather than a generic message — this is what let us
      // diagnose the chat Worker bug instantly instead of guessing.
      return new Response(JSON.stringify({
        error: 'Server error',
        detail: String(e && e.message ? e.message : e).slice(0, 300),
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }
  },
};

// ---- Stripe REST helper (no SDK needed — Stripe's API works fine over plain fetch) ----
async function stripeRequest(env, path, formParams) {
  const body = new URLSearchParams(formParams);
  const res = await fetch(`https://api.stripe.com/v1/${path}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: body.toString(),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error?.message || 'Stripe request failed');
  return data;
}

// ---- Supabase REST helpers (service role key = full access, server-side only) ----
async function supabaseUpdateProfile(env, userId, fields) {
  const res = await fetch(`${env.SUPABASE_URL}/rest/v1/profiles?id=eq.${userId}`, {
    method: 'PATCH',
    headers: {
      apikey: env.SUPABASE_SERVICE_ROLE_KEY,
      Authorization: `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      Prefer: 'return=minimal',
    },
    body: JSON.stringify(fields),
  });
  if (!res.ok) console.error('Supabase update failed:', await res.text());
}

async function supabaseFindProfileByCustomerId(env, stripeCustomerId) {
  const res = await fetch(
    `${env.SUPABASE_URL}/rest/v1/profiles?stripe_customer_id=eq.${stripeCustomerId}&select=id`,
    {
      headers: {
        apikey: env.SUPABASE_SERVICE_ROLE_KEY,
        Authorization: `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
      },
    }
  );
  const rows = await res.json();
  return rows[0]?.id || null;
}

// ---- Plan resolution -------------------------------------------------------------
// The client sends a plan KEY, never a raw Stripe price ID. If the client could pass a
// price ID directly, anyone could open devtools and check out against a $0 price they
// found elsewhere in the account. Keys are resolved server-side against env vars, so the
// only purchasable prices are the two configured here.
function resolvePriceId(plan, env) {
  const PLANS = {
    monthly: env.STRIPE_PRICE_ID,
    annual: env.STRIPE_PRICE_ID_ANNUAL,
  };
  const key = plan === 'annual' ? 'annual' : 'monthly'; // default monthly on anything unrecognised
  const priceId = PLANS[key];
  if (!priceId) {
    throw new Error(
      `No Stripe price configured for the "${key}" plan. ` +
      `Set ${key === 'annual' ? 'STRIPE_PRICE_ID_ANNUAL' : 'STRIPE_PRICE_ID'} in the Worker secrets.`
    );
  }
  return { key, priceId };
}

// ---- Endpoint 1: start a new subscription ----
async function createCheckoutSession(request, env, corsHeaders) {
  const { userId, email, plan } = await request.json();
  if (!userId || !email) {
    return new Response(JSON.stringify({ error: 'Missing userId or email' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  const { key, priceId } = resolvePriceId(plan, env);

  const session = await stripeRequest(env, 'checkout/sessions', {
    mode: 'subscription',
    'line_items[0][price]': priceId,
    'line_items[0][quantity]': '1',
    'payment_method_types[0]': 'card',
    allow_promotion_codes: 'true',
    customer_email: email,
    client_reference_id: userId,
    success_url: `${env.SITE_URL}/?checkout=success`,
    cancel_url: `${env.SITE_URL}/?checkout=cancelled`,
    // Lets us find this customer again later for cancellations/renewals via webhook
    'subscription_data[metadata][supabase_user_id]': userId,
    // Recorded so support questions like "am I on monthly or annual?" are answerable
    // from Stripe alone, without cross-referencing price IDs by hand.
    'subscription_data[metadata][plan]': key,
  });

  return new Response(JSON.stringify({ url: session.url }), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders },
  });
}

// ---- Endpoint 2: manage/cancel an existing subscription ----
async function createPortalSession(request, env, corsHeaders) {
  const { customerId } = await request.json();
  if (!customerId) {
    return new Response(JSON.stringify({ error: 'Missing customerId' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  const session = await stripeRequest(env, 'billing_portal/sessions', {
    customer: customerId,
    return_url: `${env.SITE_URL}/`,
  });

  return new Response(JSON.stringify({ url: session.url }), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders },
  });
}

// ---- Endpoint 3: Stripe calls this automatically on payment events ----
// Both plans grant the same access, so the tier written is 'member' either way. This is
// correct for a two-tier model and deliberately does not branch on plan.
async function handleWebhook(request, env, corsHeaders) {
  const signature = request.headers.get('Stripe-Signature');
  const payload = await request.text();

  const valid = await verifyStripeSignature(payload, signature, env.STRIPE_WEBHOOK_SECRET);
  if (!valid) {
    return new Response('Invalid signature', { status: 400 });
  }

  const event = JSON.parse(payload);

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object;
      const userId = session.client_reference_id;
      if (userId) {
        await supabaseUpdateProfile(env, userId, {
          subscription_tier: 'member',
          stripe_customer_id: session.customer,
          stripe_subscription_id: session.subscription,
        });
      }
      break;
    }
    case 'customer.subscription.deleted':
    case 'customer.subscription.updated': {
      const sub = event.data.object;
      const isActive = sub.status === 'active' || sub.status === 'trialing';
      const userId =
        sub.metadata?.supabase_user_id ||
        (await supabaseFindProfileByCustomerId(env, sub.customer));
      if (userId) {
        await supabaseUpdateProfile(env, userId, {
          subscription_tier: isActive ? 'member' : 'free',
        });
      }
      break;
    }
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders },
  });
}

// ---- Stripe webhook signature verification (Web Crypto — no Node crypto needed) ----
async function verifyStripeSignature(payload, sigHeader, secret) {
  if (!sigHeader) return false;
  const parts = Object.fromEntries(sigHeader.split(',').map((p) => p.split('=')));
  const signedPayload = `${parts.t}.${payload}`;
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sigBytes = await crypto.subtle.sign('HMAC', key, encoder.encode(signedPayload));
  const expected = [...new Uint8Array(sigBytes)].map((b) => b.toString(16).padStart(2, '0')).join('');
  return expected === parts.v1;
}

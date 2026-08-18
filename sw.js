// ROOTED service worker.
//
// Deliberately conservative. The single biggest risk with a service worker on a
// single-file app that deploys several times a day is serving a stale Index.html
// forever — users would stop receiving updates with no obvious symptom and no way
// to self-diagnose. So:
//
//   • Navigations and the app shell are NETWORK-FIRST. A deploy always wins.
//     The cache is only ever consulted when the network actually fails.
//   • Only genuinely static, versioned-by-content assets (icons, fonts) are
//     cache-first, because those don't change between deploys.
//   • API calls, the Cloudflare workers, Supabase, Stripe and map tiles are never
//     cached at all — stale data there would be worse than no data.
//
// Bumping CACHE_VERSION discards every previous cache on activate.

const CACHE_VERSION = 'rooted-v2-redesign';
const SHELL_CACHE = CACHE_VERSION + '-shell';
const ASSET_CACHE = CACHE_VERSION + '-assets';

const PRECACHE_ASSETS = [
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/manifest.webmanifest'
];

// Hosts whose responses must never be cached — live data, auth, payments, tiles.
const NEVER_CACHE = [
  'supabase.co',
  'stripe.com',
  'workers.dev',
  'usdalocalfoodportal.com',
  'nominatim.openstreetmap.org',
  'tile.openstreetmap.org',
  'api.anthropic.com'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(ASSET_CACHE)
      .then(c => c.addAll(PRECACHE_ASSETS))
      .catch(() => {})          // a failed precache must never block installation
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => !k.startsWith(CACHE_VERSION)).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (NEVER_CACHE.some(h => url.hostname.includes(h))) return;

  // App shell / navigations: network first, cache only as an offline fallback.
  if (req.mode === 'navigate' || url.pathname === '/' || /\/index\.html$/i.test(url.pathname)) {
    event.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then(c => c.put('/', copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match('/').then(hit => hit || caches.match(req)))
    );
    return;
  }

  // Static assets we control: cache first, refresh in the background.
  if (url.origin === self.location.origin && /\.(png|svg|ico|webmanifest|woff2?)$/i.test(url.pathname)) {
    event.respondWith(
      caches.match(req).then(hit => {
        const network = fetch(req).then(res => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(ASSET_CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return res;
        }).catch(() => hit);
        return hit || network;
      })
    );
  }
  // Everything else falls through to the network untouched.
});

// Lets the page force an immediate update if it ever needs to.
self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});

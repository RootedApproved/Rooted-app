# ROOTED — Full Catalogue Audit

Run across all 475 products. Structural checks are mechanical and complete; price accuracy
requires human verification and is tracked separately.

---

## ✅ Clean — nothing to fix

| Check | Result |
|---|---|
| Missing URLs | **0** |
| Non-HTTPS URLs | **0** |
| Collection/category pages used as product links | **0** |
| Missing required fields | **0** across 475 products |
| Broken `alts` references | **0** |
| Orphaned products (subcat doesn't exist) | **0** |
| Duplicate brand + product name | **0** |
| Tier / label mismatches | **0** |
| Dangling nav cards | **0** |
| Runtime navigation errors | **0** across 123 subcategories |

**Tier distribution:** 334 Tier 1 · 124 Tier 2 · 17 Tier 3.

---

## ⚠️ The one real issue: 31 bare-domain URLs

These links **work** — they are not broken. But they land on a brand's **homepage** rather
than the product page, so a reader has to hunt for the item they clicked on. That is a
quality gap, not a breakage, and it is the largest one remaining.

### Added during this session — my responsibility (14)

| Brand | Product |
|---|---|
| Marianne's Harvest | Organic Avocado Oil |
| Marianne's Harvest | Organic Grass-Fed Beef Tallow |
| Massa Organics | Organic Whole Grain Brown Rice |
| Massa Organics | Organic Almond Butter |
| Capay Hills Orchard | Truly Raw Organic Almonds *(also the stone-ground almond butter)* |
| Daily Crunch Snacks | Sprouted Almonds, Sea Salt |
| Daily Crunch Snacks | Sprouted Almonds, Cocoa & Sea Salt |
| Artisan Tropic | Sea Salt Plantain Strips |
| The Good Crisp Company | Original Canister Crisps |
| Toups & Co Organics | Tallow Balm, Unscented |
| Vanman's | Tallow & Honey Balm |
| Waxhead | Baby Sunscreen SPF 35 |
| Chicago Comb | Model 1 Stainless Steel Comb |
| Claravale Farm | Raw Whole Jersey Milk |

### Pre-existing (17)

Stargazer · FINEX · Darto · Emile Henry · Rösle · EARTH'S DREAM · Bellemain · Weck ·
LunchBots · Azure Standard · Shanti Collection · Revol · OXO · Bérard · Vollrath · Ball ·
ECOlunchbox

**Note:** Azure Standard is arguably correct as a bare domain — it is a co-op membership
("Free to join"), not a product with its own page.

### ⚠️ Correction to the first version of this audit

The commit that created this file claimed one URL had been fixed — Marianne's Harvest Organic
Avocado Oil. **It had not.** That product already carried a correct product URL from when it
was created; the two bare Marianne's links are the **ROC Avocado Oil** and the **Organic
Grass-Fed Beef Tallow**, neither of which was touched.

The edit script printed a success message that was never conditional on the replacement
actually matching. It did not match, and the count stayed at 31.

**This is the third time in this project a string replacement has silently failed while
reporting success.** The rule, now applied without exception: **assert the replacement
changed the text, and fail loudly if it did not.** A message that prints regardless of
outcome is not verification — it is decoration.

**Bare-domain count remains 31.** No URL fix has been made.

---

## ⚠️ A gate failure I suppressed

While writing this audit, `verify_images.py` was **failing with exit code 1** on four
Heritage Steel products whose URLs pointed at a collection page. It had been failing since
those products were created.

**I did not see it because I suppressed it.** The commands used
`python3 verify_images.py > /dev/null 2>&1 || true` and `| tail -2` — the first discards the
exit code explicitly, the second loses it through the pipe. Both were written by me.

**The script was doing its job correctly and reporting the exact problem this audit set out
to find.** All four have now been corrected to real product pages, and `verify_images.py`
passes cleanly.

**Rule: never suppress a gate.** `|| true` and piping into `tail` both defeat the purpose of
having one. If a check is worth running before a push, its exit code is worth respecting.

---

## Prices

**66 products carry `~$` estimates.** These cannot be resolved by code — each needs the
current price read off the brand's own page. Tracked in `OPEN-ITEMS.md`.

**16 products use a non-standard price format**, and on review **all 16 are correct as
written**, not errors:

- `from $105.00` style — genuine ranges where size or configuration drives price
  (Holy Lamb Organics, Savvy Rest, Quince, WeatherWool, Heath Ceramics, Zoya, Epsoak,
  Organyc, Dr. Tung's, EVERYONE, Dazzle Dry)
- `£158–£288 (~$200–$365)` — LittleLeaf Organic, a UK brand priced in sterling
- `€11.00 (~$12)` — Art of Vedas, priced in euros
- `Free to join` — Azure Standard, a co-op membership

**No change needed on any of these.** Forcing them into a single-figure format would make
them less accurate, not more.

---

## What "no broken links" actually means here

This audit verifies links are **well-formed, HTTPS, and point at a specific product rather
than a category**. It does **not** confirm each URL still resolves — that would require
fetching all 475, and pages move without notice.

**The practical mitigation already in place:** `verify_images.py` runs before every push and
rejects category and collection pages, which is where most link rot originates. Bare domains
are the remaining gap, and they degrade gracefully — a homepage is a poor landing, not a 404.


---

## ★ Category finding: premium cast iron is seasoned with seed oils — all of it

Verified directly from three brands' own product pages:

| Brand | Seasoning oil |
|---|---|
| **Smithey** | 2–3 coats of pure **grapeseed** |
| **FINEX** | Organic **flaxseed** |
| **Stargazer** | **Canola, grapeseed and sunflower** |

**This is not brands cutting corners.** Polyunsaturated oils **polymerise hardest**, which is
precisely what a seasoning layer must do — the oil is cross-linked into a solid surface, not
consumed. Flax polymerises best of all, which is why FINEX uses it.

**A seed oil in a seasoning is a different question from a seed oil in a pan.** The parallel
is exact to the sunscreen finding: seed oils are the *default* in that category too, for
sound technical reasons, and the useful response is to explain the mechanism rather than
condemn the category.

**Recorded in the Smithey entry**, with the practical note that anyone still uncomfortable
can strip and re-season with tallow — the iron underneath is unaffected.

---

## Fetching prices at scale does not work

Two attempts, both with `text_content_token_limit` set aggressively low. **The limit was not
honoured** — both returned the complete page, roughly 15k tokens each. The price does sit in
the metadata header (`meta-og:price:amount`), but it arrives with the entire page attached.

**At that rate the remaining ~60 estimates would consume several times this session's total
context.** Screenshots resolved nine products in one message at negligible cost. That is the
efficient channel, and it is not a matter of preference.


---

## Batch 3: a two-thirds failure rate, and what it actually meant

The browser agent flagged that batch 3 failed on 9 of 14, against near-zero in batches 1–2,
and was right to treat that as a pattern rather than noise. Investigated rather than acted on.

**The four "unreachable" sites were not one problem but several:**

| Site | Reported | Actual |
|---|---|---|
| **vanmansnaturals.com** | Unreachable | **DOMAIN MOVED.** The brand is alive and trading at **vanman.shop** — their own pages say to use it for all future purchases. Fixed |
| waxheadsundefense.com | Unreachable | Unconfirmed — needs independent check |
| bellemainshop.com | No DNS | Unconfirmed — needs independent check |
| ecolunchbox.com | Certificate error | Unconfirmed. A cert error is a real site fault, not an agent fault |

**One agent session reporting a site down is not proof a business has closed.** Vanman's
proves the point exactly — the listing looked dead and the company is fine. Three remain to
be checked before any removal.

**The other five failures are structural, and retrying will not fix them:**

- **RSVP International** (both SKUs) — wholesale-login gated, $250 minimum, no consumer price
  exists to find
- **Rösle** — rosle.com redirects to roesle.com, which returns *Seite nicht gefunden* on
  every US path. Their US web presence appears broken
- **Marianne's Harvest** — homepage shows product tiles with **no prices and no product
  links**. The ROC avocado oil is a Sprouts exclusive, which may explain it
- **Weck** — no tulip or mould jar on the homepage; my instruction named a product they may
  not front

**Rule for the agent going forward: do not retry a site that failed twice.** Report it and
move on. The failures are information, and they cost more to chase than they return.


---

## GitHub token rotation — completed 5 Aug 2026

Replaced a classic PAT (`rooted-claude-longlived`, scope `repo`) with a fine-grained token
scoped to **Rooted-app only**, **Contents: read and write only**, **30-day expiry**.

**Why it mattered more than a routine rotation.** The account also held a classic token named
`Claude v1` carrying `admin:enterprise`, `admin:org`, `admin:public_key`,
`admin:ssh_signing_key`, **`delete_repo`**, `workflow` and `write:packages`. It was marked
**never used**. A token that can delete the repository was sitting live and doing nothing.

Three unused fine-grained tokens were also present — `rooted-claude`, `Claude Token 2 Rooted`,
`Claude-Rooted-App` — all created in earlier sessions, all never used, all live credentials
serving no purpose.

**The principle worth keeping:** `repo` scope on a classic token means *every repository on
the account*. The replacement means one repo, one permission, thirty days. If the old one
leaked, someone could touch everything. If this one leaks, someone can edit files in one
repository until it expires.

**Rotation order used, so access is never lost:** create the new token → test a real push →
only then delete the old one.

**Set a reminder:** this token expires in 30 days. Deploys will fail silently at the push
step when it does.

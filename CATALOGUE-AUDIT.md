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

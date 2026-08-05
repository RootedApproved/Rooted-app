# ROOTED — Open Items

Single tracking file. Everything outstanding across the project lives here.

---

## 1. Needs J — small, blocking

| # | Item | Why it blocks | Effort |
|---|---|---|---|
| 1.1 | **Listing-type decision** (see §2) | Blocks 4+ already-verified farms and mis-files 6 meat operations | One decision |
| 1.2 | **Rotate the GitHub token** | Classic PAT with broad scope, exposed in chat logs | 2 min |
| 1.3 | **Confirm 7 `~$` prices** by screenshot | Tier 3 products show estimates | One shop trip |
| 1.4 | **Workout Tops reclassification** | Wool&Prince, Son of a Tailor, Harvest & Mill are everyday tees, not workout gear. Awaiting a yes | One reply |
| 1.5 | **Stripe Worker source** | Needed to add the annual plan (~$90) and the 21-day trial | Paste the file |
| 1.6 | **Confirm Cloudflare Analytics is recording** | Load the site, check the dashboard after ~5 min | 2 min |

**Closed:** Netlify credit question — J confirmed he is fine for now and will renew when he
hits the limit.

---

## 2. THE TYPE DECISION — highest-leverage single call

The map has five listing types: `grocery`, `farmersmarket`, `restaurant`, `csa`,
`onfarmmarket`. Two gaps have appeared repeatedly:

**A. Direct-order farms** — verified California farms selling by post or online, with no box
subscription and no storefront. Currently unlistable. Blocked and waiting:

| Farm | What it is |
|---|---|
| **Massa Organics** | CCOF certified. Sheep graze the almond orchard; ducks in the rice fields. Organic brown rice, almonds, almond butter |
| **Capay Canyon Ranch** | Fifth generation, organic grapes and raisins, almonds |
| **Outer Aisle Food Hub** | Farmigo buying platform |
| **Heritage Valley Family Orchard** | Listed as CSA, but the model is really a shipped single-crop subscription |

**B. A `meat` type.** Six meat operations are filed as `csa`, which understates them: Da-Le
Ranch, Engler Beef, Stemple Creek, Markegard, Casa Rosa, Talley Ranch. A user looking for
grass-fed beef cannot currently filter for it.

**Recommendation:** add both. `meat` is unambiguous and immediately useful. `directorder`
shifts the map slightly from "places you go" to "places you buy from", which is J's call —
but four verified farms are sitting idle without it.

---

## 3. Next work, in priority order

### 3.1 Bay Area restaurants — DO THIS FIRST
166 listings in the region, **2 restaurants.** Biggest visible imbalance on the map.
Same method that took San Diego from 0 to 4. See §5 for the execution plan.

### 3.2 The four remaining USDA-verified grass-fed ranches
A complete, closed set — five exist in California, one is listed. Contact details and
certificate numbers already in hand.

| Ranch | Certificate | Valid to |
|---|---|---|
| Cahuilla Mountain Ranch (Anza) | GF4214MHA | 1 Aug 2026 |
| Hunt Road Cattle Company (Copperopolis) | GF5041MHA | 10 Feb 2027 |
| Gamble Ranch (Winton) | GF4277MHB | 3 Oct 2026 |
| Delta Diversified Farming (Walnut Grove) | GF4320MHA | 15 Nov 2026 |

### 3.3 Remaining meat leads
Big Bluff Ranch (certified organic pastured chicken, vetted by Stemple Creek) · Pomponio
Ranch · Fogline Farms · SoMar Farms · Silver Springs Beef · Galaxy Farm · Yolo Land &
Cattle · Spreadwing Farm · Farm Lot 59

### 3.4 Dairy and raw milk — currently ZERO on the map
A conspicuous gap given ROOTED's standards. No source identified yet; start with the
Weston A. Price chapter listings and CDFA's raw milk permit register.

### 3.5 The 14 orphan listings — decide: build or remove
- **8 MOM's Organic Market** (DC, MD, VA)
- **6 chain groceries** (Reno, Sparks, Carson City)

All grocery. Zero farm-direct, zero restaurants, zero farmers markets in either region. A
user in DC opens the map and sees eight MOM's and nothing else; a Reno user sees six chain
stores. **That is worse than showing nothing**, because it implies coverage that does not
exist and makes the map look abandoned rather than focused.

Two honest options: build those regions properly (Reno is defensible — Mountain Bounty Farm
already delivers to Reno, Incline Village and Zephyr Cove), or cut them and be cleanly
California-only.

### 3.6 Stop adding chain grocery
482 of 680 listings, 87% of it Trader Joe's, Sprouts and Whole Foods. Every one added makes
the map bigger without making it better.

---

## 4. Farms awaiting a phone call
See `FARMS-HELD-NEEDS-CONTACT.md` — 15 entries, each with the specific question to ask.
The two worth making first:
- **Freewheelin' Farm** (Santa Cruz) — CSA shares hauled six miles by bicycle-drawn trailer
- **The Steward Sustainable Farm** (Crows Landing) — founded by a 14-year-old third-generation farmer

---

## 5. Execution plan for Bay Area restaurants

**Target:** 12–20 verified restaurants across SF, Oakland/Berkeley, Marin, the Peninsula and
the South Bay.

**Sources, in order:** Local Fats (seed-oil-free directory, used for San Diego) → each
restaurant's own site → recent local food press → **recent reviews for closure signals.**

**Batch by city cluster, 4–6 per commit.** One gate and one commit per batch.

**Restaurant-specific rules — these differ from farms:**

1. **Closure risk is far higher than farms.** Tara Firma's CSA closed three weeks before we
   nearly listed it; restaurants close faster still. Check the most recent reviews for
   "closed" or "moved" before writing any entry.
2. **Cooking fats change without announcement.** A tallow fryer can quietly become a canola
   fryer. Every entry must tell readers to verify current fats directly.
3. **Partial compliance is a rejection, not a caveat.** GOODONYA was excluded because its
   pancakes and some tortillas contain safflower oil despite a seed-oil-free reputation.
   Someone trusting the map would order the pancakes.
4. **Name the specific fat.** "Beef tallow", "avocado oil", "ghee" — not "healthy oils".
5. **Note where the category makes it remarkable.** Pichudo earned its listing because
   Mexican kitchens are almost universally soybean or canola based.

**Pace:** roughly 2 clusters per exchange, 4–6 restaurants each.

### Two warnings surfaced while starting this work

**1. "Seed oil free" is often only partly true, and in specific predictable ways.** An
industry source quoted by Fox News named the two most common failures: *"They are using beef
tallow in their fryers, but it is cut with soy and stabilizers"*, and *"they don't examine
the products they bring in, offering burgers on seed oil-laden buns."* Fryer fat is the
visible claim; **the bun and the condiments are where it actually breaks.** Momolicious was
listed specifically because it addresses the sauces.

**2. Restaurants revert.** **sweetgreen went seed oil free for several months and then
reverted to sunflower oil.** That is the clearest possible argument for two things: never
list a chain on a temporary reformulation, and tell every reader to confirm current fats
directly. **sweetgreen is excluded from this map for that reason** despite appearing on
seed-oil-free directories.

### Bay Area candidates identified, not yet verified
Velo City Pizza (San Mateo) · The Park Street Tavern (Alameda) · Manzanita (Milpitas) ·
Estero Cafe (Valley Ford) · Ristorante Allegria (Napa — EVOO, avocado oil, Snake River
tallow, Clover butter) · Walrus Alley · Caffe Central (SF)

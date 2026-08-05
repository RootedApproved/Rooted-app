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

### Bay Area candidates still to verify
Evvia Estiatorio (Palo Alto — Greek) · Eve's Waterfront (Oakland) · Long Bridge Pizza Co.
(SF) · Terun (Palo Alto) · iTalico (Palo Alto) · The Good Salad (Palo Alto) · Hummus
Mediterranean Kitchen (Palo Alto) · Flea Street (Menlo Park) · Stoa (SF) · Calibur Burger
(SF) · GK Pastry (Mountain View) · Rebel Kitchen (Livermore) ·
The Park Street Tavern (Alameda — marked **Chain**, treat with the sweetgreen caution) ·
Manzanita (Milpitas) · Ristorante Allegria (Napa — EVOO, avocado oil, Snake River tallow,
Clover butter) · Musubi Libre (Hayward) · The Green Enchilada (Pacifica) · Long Bridge Pizza
(SF) · Eve's Waterfront (Oakland) · Local Union 271 (Palo Alto) · The Midwife and The Baker
(Mountain View) · Maison Alyzee (Mountain View) · Napoletana Pizzeria (Mountain View) ·
The Press Artisan Cafe (Pleasanton) · 4505 Burgers & BBQ (SF) · Caffe Central (SF)

**Chains appearing on seed-oil-free directories and excluded:** sweetgreen (reverted to
sunflower), Buffalo Wild Wings (cooking oils differ between the US and Canada, so a Canadian
data point does not describe the US kitchens), Five Guys, True Food Kitchen. A chain-wide
claim is only as good as its least careful franchise, and reformulations reverse.

### ⚠️ Local Fats snippet attributes BLEED between adjacent entries

Local Fats search-result pages list restaurants in sequence with tags — `Chain`,
`100% Seed Oil Free`, `Gluten Free Options`, and the oil list — and **those tags do not
reliably stay attached to the right restaurant.** Observed directly:

- **Evvia Estiatorio** shows "Duck Fat, Olive Oil, Avocado Oil" on one page and
  "Chain … Olive Oil, Avocado Oil · 180 El Camino Real Ste 1140" on another — but that
  address belongs to **Local Union 271**, stated explicitly elsewhere.
- **Casey's Pizza** shows "Butter, Olive Oil, Avocado Oil" on one page and
  "Chain … Olive Oil, Coconut Oil, Avocado Oil" on another.
- **Kitava Mission** and **Kitava Oakland** carry markedly different oil lists — which may be
  genuine, or may be bleed.

**CONFIRMED WORSE ON A SECOND PASS.** The identical tag string *"Beef Tallow Butter Ghee
Pork Lard Olive Oil Coconut Oil more"* appears verbatim against **Kitava Oakland** and
**Calibur Burger**, and *"Chain 100% Seed Oil Free Olive Oil Coconut Oil Avocado Oil"*
appears verbatim against both **Eve's Waterfront** and **Long Bridge Pizza Co.** These are
repeating template fragments, not per-restaurant data.

**Rule, hardened: the oil lists in Local Fats search snippets are UNUSABLE.** Do not cite
them at all, even with two matching pages — matching pages are exactly what a repeating
template produces. Only the presence of a restaurant in the directory, its name, and its
city can be taken from a snippet. For fats, fetch the restaurant's own profile page or its
website, or use the Seed Oil Free Alliance below.

**Already corrected:** Casey's Pizza, which had cited a specific fat list.

This is the third instance of the same underlying failure — directory listings merging
adjacent entries — after the CAFF page that put West County Community Farm's address into
Laguna Farm, and the Open Silo snippet that ran ALMA's description into Farm Lot 59's.

### ★ THE SEED OIL FREE ALLIANCE — the certification this category was missing

Founded 2023 by Corey Nelson and Jonathan Rubin, explicitly because **no certification
existed to verify that foods are actually seed-oil free.** They certify restaurants and
packaged products, and they **test the oils**.

Why this matters more than any directory: in certifying their first restaurant, the Alliance
had already **rejected another applicant for oil adulteration** — a supplier's "clean" oil
that turned out not to be. That is precisely the failure the industry source named earlier:
*tallow cut with soy and stabilisers.* A restaurant cannot detect that by trusting its
supplier; only testing catches it.

**This is the restaurant equivalent of CCOF for organic and the USDA SVS register for
grass-fed** — the third source of its kind found in this project, and the pattern holds:
**a directory tells you a claim exists; a certifier tells you it was checked.**

**Directory pulled.** `seedoilfreecertified.com/product-finder`

**For restaurants it is disappointing — and that is worth knowing.** Only four certified
restaurants exist: Just Be Kitchen (Colorado), Garden Butcher (Florida), Motek Cafe and
Frites Street. **None in California.** Restaurant certification is genuinely new, so it
cannot be used to build out the Bay Area. Local Fats remains the discovery source for
restaurants; the Alliance is the standard to check against once a candidate is found.

---

## ★★ THE REAL FIND: this directory unlocks Food & Diet

**Food & Diet was closed at 0 of 11 subcategories** because seed oils are floor and nothing
could be verified to that bar. **This directory is the verification that was missing.**

Roughly **50 brands** are certified under a physician-authored standard with **independent
laboratory testing** and **supply-chain auditing for hidden seed oils in compound
ingredients** — which is exactly the problem that closed the category. It is not a claim; it
is a tested claim, and the Alliance has already rejected an applicant for oil adulteration.

**Certified brands mapping onto ROOTED product categories:**

| Category | Certified brands |
|---|---|
| **Cooking fats & oils** | Kettle & Fire (beef tallow) · Marianne's Harvest (organic avocado oil) · California Olive Ranch · Bono USA · AvoPacific Oils · Gemsa Oils · Daabon Organic · Zero Acre Farms · Algae Cooking Club |
| **Chips & snacks** | The Good Crisp Company · Artisan Tropic · Beefy's Own Tallow Chips · Magos Chips · Sweetpotato Awesome · Crunchmaster |
| **Nuts & nut butters** | Daily Crunch Snacks · Seed & Shell |
| **Plant milks** | Elmhurst · New Barn Organics · Táche Pistachio Milk · Pecana Milk · Vita Coco |
| **Sauces & dips** | Hoboken Farms · Habiza Hummus · Cedar's Foods · Eat Happy Kitchen |
| **Bars & desserts** | TruBar · Patterbar · My Mochi · Everybody Eating |
| **Breakfast & baked** | Purely Elizabeth · Atoria's Baking Company · Maria & Ricardo's Tortillas |
| **Meat & meals** | Good Ranchers · Saffron Road · Little Spoon · Grazly |

**Why this matters more than the next twenty restaurants:** every one of these is a
*product* that can be rated in the catalogue, with a verification standard that already
matches ROOTED's floor exactly. It reopens a category declared complete at zero.

**Recommended next action, ahead of further restaurant work:** work the Seed Oil Free
Certified directory into the Food & Diet product categories. Same discipline as everywhere
else — the certification proves the seed-oil floor is cleared, but ROOTED's other standards
(organic, ingredient quality, packaging) still need checking per product.

### Category-specific questions worth asking

Different cuisines fail in different places. Ask about:
- **Pizza** → the DOUGH, not the finishing oil. Commercial dough very often contains soybean oil.
- **Burgers** → the BUN. Named as one of the two commonest failure points.
- **Anything fried** → whether the tallow is cut with soy or stabilisers.
- **Everything** → the CONDIMENTS. Commercial mayo and ketchup are almost always soybean or canola.

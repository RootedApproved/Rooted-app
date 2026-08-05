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

## 1b. RAW DAIRY — a decision I am not making for you

**The gap is real.** The subcategory is titled **"Grass-Fed & Raw Dairy"** and its standard
explicitly says raw milk needs "its own explicit disclosure and, where legally sold, clear
handling guidance." Both listed products are pasteurized. **There is no raw dairy on ROOTED
at all.** California is one of the few states with legal retail raw milk, so for a
California-focused platform that is a genuine hole.

**The obvious candidate is Raw Farm LLC** (Fresno, formerly Organic Pastures) — the largest
raw dairy producer in the United States, sold in hundreds of California retail outlets.

**I did not add it, because the record needs your judgement rather than mine.**

### What the record shows

| | |
|---|---|
| Since 2006 | **15 recalls** — E. coli, Listeria, Salmonella, Campylobacter |
| Outbreaks | **Seven** — 2006, 2011, 2012, 2016, 2023, 2024, 2026 |
| Dec 2024 | **Bird flu (H5N1) detected** in retail product *and* at the bottling facility. Farm quarantined; CDPH secured a statewide recall of all milk and cream |
| Early 2026 | E. coli outbreak linked to raw cheddar — 9 ill, 3 hospitalised, **one with HUS (kidney failure)**, across CA, FL and TX |
| Reported pattern | **In each outbreak, children were a significant share of those sickened.** In the 2026 cluster, over half the patients were under five |

### What the company's side shows, fairly stated

- Raw Farm ran roughly **14,000 tests** from September to February, all negative for E. coli O157:H7, and published results as they accumulated
- **California, Texas and Florida each tested the implicated batches independently — all negative**
- The FDA could not issue a mandatory recall because FSMA requires demonstrated causation, which it did not have. The April 2026 recall was voluntary
- The **recall was formally closed in May 2026 with no illness confirmed from recalled product**
- Roughly $2M of product destroyed

### Why this is your call

ROOTED's entire premise is that a listing means something was checked. Raw dairy fits the
ancestral philosophy, it is legal here, and plenty of people want it — but a "Rooted
Approved" label on a producer with seven outbreaks and repeated paediatric hospitalisations
is a different kind of claim from approving an olive oil.

**Three honest options:**
1. **List Raw Farm with the full record stated in the entry** — including the outbreak
   history, the bird flu quarantine, and the company's testing response. Trusts the reader
   with the facts.
2. **Research other licensed California raw dairies** and list one with a cleaner record.
   Raw Farm is the largest but not the only licensed producer.
3. **List no raw dairy** and rename the subcategory so it stops promising something it does
   not deliver.

### ✅ RESOLVED — J chose option 2. Claravale Farm listed.

**Claravale Farm** (Paicines, San Benito County) is listed at **Tier 2 / Good Option**,
deliberately not Tier 1. Bottling raw Jersey milk since **1927**, certified organic pasture
and hay, returnable glass bottles, nothing homogenised or standardised.

**The record comparison that decided it:**

| | Raw Farm | Claravale |
|---|---|---|
| Recalls since 2006 | 15 | 2 documented incidents |
| Outbreaks | 7 (2006–2026) | 1 (2015 Campylobacter, 6 ill) |
| Bird flu quarantine | Yes, Dec 2024 | No |
| Paediatric hospitalisations | Repeatedly | None documented |
| Operating since | 1916 (as Organic Pastures 2000) | 1927 |

**Not spotless, and the entry says so** — the 2015 Campylobacter recall and quarantine and a
2021 raw goat milk recall are both named in the listing, in the verdict as well as the flags.

**One open question worth asking Claravale:** their feed includes "occasional non-GMO
grain-based dairy feed" whose composition is not published. Given the seed-oils-in-feed floor
ruling, that is worth a direct question. It is flagged in the entry rather than glossed.

**Raw Farm is NOT listed** and should not be added without a further decision.

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

**B. ✅ DONE — `meat` type added, labelled "Grass-Fed Meat".** J approved. Six operations
moved from `csa`: Da-Le Ranch, Engler Beef, Stemple Creek, Markegard, Casa Rosa, Talley
Ranch. Own filter toggle, own colour (#4A6741) and icon. Free tier, curated-only (never
queried against the USDA API, like grocery and restaurant).

**Still open: whether `directorder` should exist.** Four verified farms remain unlistable
without it — Massa Organics, Capay Canyon Ranch, Outer Aisle Food Hub, and arguably Heritage
Valley Family Orchard, currently filed as a CSA though its model is a shipped single-crop
subscription.

**Remaining recommendation:** `directorder` shifts the map slightly from "places you go" to
"places you buy from", which is J's call — but four verified farms are sitting idle without
it, and the meat type has now proven the pattern works cleanly.

### Grass-Fed Meat: 9 listed. The remaining leads are NOT yet verifiable.

**Added:** Stemple Creek, Markegard, Engler, Da-Le, Casa Rosa, Talley Ranch, Cahuilla
Mountain, Fogline Farms, Pomponio Ranch.

**⚠️ `beefnear.me` is a proven-unreliable source and must not be used alone.** It still
lists **Tara Firma Farms** as running CSA subscriptions — that programme ended 3 July 2026.
Everything below currently rests on that one directory, which is exactly the single-aggregator
failure already documented for `rootseller.app`.

| Lead | Status | What would verify it |
|---|---|---|
| Paicines Ranch | Single source (beefnear.me) | Their own site showing a live store and shipping |
| Hearst Ranch Beef | Single source + a 2018 article | Own site; searches are drowned by Hearst Ranch **Winery**, a different business |
| Morris Grassfed | 2018 article, price likely stale | Own site, current pricing |
| **J&J Grassfed Beef** (Tehachapi) | 2018 article — but **grain-free** and monthly delivery to 50+ SoCal locations | Worth a dedicated lookup; grain-free is directly relevant to the feed floor |
| Richards Grassfed Beef | Single source | Own site |
| Fox Sparrow Farm, Turner Grass Fed | Single source | Own sites |
| Big Bluff Ranch | Red Bluff — likely outside core California scope | Confirm scope first |
| SoMar, Silver Springs, Galaxy, Yolo Land & Cattle, Spreadwing, Farm Lot 59 | Single Weston A. Price chapter listing | Dedicated lookups |

**USDA-verified but held on direct sales:** Gamble Ranch (Winton) and Hunt Road Cattle
(Copperopolis) hold federal grass-fed certificates but no evidence they sell to the public.
Delta Diversified (Walnut Grove) is unchecked. **Federal verification proves the claim, not
that anyone can buy the meat** — the Love Apple lesson.

### ✅ CDFA Certified Producer register pulled and cross-checked (edition: 1 May 2026)

**It independently confirmed 12 farms already on ROOTED**, each holding a live state
certificate to sell direct — the strongest validation of existing work available:

Borba Farms · Mountain Bounty Farm · The Natural Trading Company · Sage Mountain Farm ·
Huerta del Valle · Huarache Farms · J.R. Organics · Frog Hollow Farm · Knoll Farms ·
Da-Le Ranch · Alexandre Family Farm · Serendipity Farms

**⚠️ Three show certificates that had lapsed by the register date:**

| Farm | Expired | Note |
|---|---|---|
| **Da-Le Ranch** | 4 May 2026 | On the map. Register is a 1 May snapshot, so a later renewal would not appear |
| Serendipity Farms | 9 Jun 2026 | On the map |
| Alexandre Family Farm | 1 May 2026 | Product listing, not a map pin |

Not an emergency and not evidence of a problem — small farms renew late routinely. Worth a
check before anyone drives out, which the entries already advise.

**Resolves a standing hold:** *Feed and Be Fed* (Los Angeles, Linda O'Brien-Rothe) IS a
certified producer, expired 20 May 2026. It exists and sells direct; the entry needs only
current-season detail.

### New protein leads WITH confirmed direct-sale certification

These carry the proof the beefnear.me leads lacked. Each still needs its practices
researched — the certificate proves they sell to the public, not how they farm.

| Farm | County | Valid to | What |
|---|---|---|---|
| ~~Sunrise Pasture-Poultry Farm~~ | Monterey | 26 Feb 2027 | **ADDED** — CCOF certified organic livestock since 2015 |
| **Hog Wild Holding Co.** | Monterey | 10 Apr 2027 | Pork |
| **Hilliker's Egg Ranch** | San Diego | 7 Jan 2027 | Eggs |
| **Mariposa Ranch Eggs** | Los Angeles | 11 Mar 2027 | Eggs |
| ~~Metzer Farms~~ | Monterey | 25 Feb 2027 | **REJECTED** — see below |
| **Fallon Hills Ranch** | Marin | 14 Jan 2027 | Kevin Maloney |
| **Bloom Ranch** | Los Angeles | 4 Mar 2027 | Bill Releford |
| **Monkey Flower Ranch** | Monterey | 19 Aug 2026 | Rebecca King — sheep |
| **The Woolly Egg Ranch** | Marin | 21 Jul 2026 | Eggs |
| **True Grass Farms** | Marin | 3 Jul 2026 (lapsed) | Guido Frosini — grass-fed |
| Heart T Hogs | Modoc | 27 Jun 2026 | Pork — far north, check scope |

### ❌ Metzer Farms rejected — certificate ≠ standard

Metzer holds a valid CDFA certificate to sell direct. What it sells does not meet the
standard. A supplier who stocks their duck eggs states plainly: *"These are NOT organic
fed/certified organic or pasture-raised… They ARE CAGE-FREE, raised in open sided… layer
buildings… They are local, but they are conventionally raised."* They moved the flock
indoors permanently as avian-flu biosecurity.

The egg subcategory standard explicitly red-flags **"cage-free alone"**. Metzer is also
primarily a **hatchery** selling day-old ducklings, not a food producer. Duck eggs now sell
under the separate **Olinday Farms** brand.

**This is the cleanest demonstration yet that a state certificate proves a farm sells to the
public — nothing more.** It is necessary, not sufficient.

### Rich new protein leads found alongside (all corn/soy-free or equivalent)

| Farm | Where | Why |
|---|---|---|
| **Tomales Bay Pastures** | Pt. Reyes | Pasture-raised eggs, **corn & soy free**. Only source is UC Cooperative Extension's Grown in Marin — authoritative but a single line. Needs their own site |
| **Rossotti Ranch** | Petaluma | Pasture-raised, **grain-free**. Same single-source position as above |
| **Chino Valley Ranchers** | Colton | Organic **soy-free corn-free** eggs, flax-fed, 225mg ALA each, 70+ year family business, widely stocked in stores. ⚠️ Housing is *free-roaming/cage-free*, NOT pasture-raised — would fail the egg standard's red flag on cage-free alone. Accessible but a weaker standard; worth listing only with that stated |
| **Rossotti Ranch** | Petaluma | Pasture-raised, **grain-free** |
| ~~True Grass Farms~~ | Valley Ford | **ADDED** — Animal Welfare Approved, farm store, cabins on site |
| **Honest Fish Farm** | CA Delta | Pigs on pasture moved every 3–5 days, **soy-free**, organically fed |
| **Rainbow Ranch Farms** | Southern California | **STRICTEST FEED STANDARD FOUND ANYWHERE.** States: no grains at all — no rice, soy, corn, wheat, barley, oats, rye — no legumes, nuts or seed oils. Heritage breeds on species-specific diets. Also states vaccine-free, antibiotic-free, drug-free. ⚠️ **HELD: no street address published.** Cannot map a farm without one — same reason LADS Home Ranch is held. Needs a call or a better source |
| ~~Marin Sun Farms~~ | Pt. Reyes + Oakland | **ADDED (2 pins)** — operates the last USDA-inspected slaughterhouse in the Bay Area |
| **Pasture Fresh Eggs** | Tomales | Organic pasture-raised eggs |
| **SonRise Ranch** | — | Hogs on pasture fed raw milk from their own cows |
| Pajaro Pastures / Your Family Farm | Paicines | Eggs and pasture-raised Berkshire hogs |

**These are a better lead pool than the beefnear.me set** — most name a specific feed
standard, which is the thing that actually separates pastured operations.

**On Bounty of the Valley:** it appears here as a certified direct-sale producer valid to
21 Jan 2027. That does **not** overturn its rejection. It was rejected for **suspended
organic certification**, not for whether it sells direct. Both are true at once, and the
organic claim is the one that failed.

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

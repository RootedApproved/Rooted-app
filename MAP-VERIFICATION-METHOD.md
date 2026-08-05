# Local Food Map — Faster Verification Method

Written after 57 farms from the Localize app list were checked one at a time. That approach
worked but was slow, and the slowness was **structural, not effort**.

---

## The problem with the old method

Of 57 farms checked from the Localize list:

| Outcome | Count |
|---|---|
| Added | 35 |
| Defunct / rejected | 5 |
| Unverifiable, held | 15 |
| Miscategorised (fixed) | 3 |
| Suspended certification | 1 |

**About a third of the effort produced a rejection note rather than a listing.** The list
was unvalidated, so most of the work was answering *"is this farm real?"* — and the answer
was often no.

---

## The fix: start from registers, not directories

Every strong discovery this session came from a source where **presence is already
verification**. Start there and the question flips from *"is this real?"* (mostly no) to
*"which of these verified farms fit ROOTED?"* (mostly yes).

### Source ranking — use in this order

**1. CDFA CSA Paid Listing** — `cdfa.ca.gov/is/pdfs/MonthlyCSA-PaidListing.pdf`
Registration is a **legal requirement** to operate a CSA in California. A farm cannot remain
on a paid state register after closing. Currently dated **1 May 2026**. One fetch returns
the entire state.

**2. CDFA Certified Producer Certificates** — `cdfa.ca.gov/is/i_&_c/pdfs/CFM-CertifiedProducersByCounty.pdf`
Updated more often than the CSA list; covers any farm selling at certified farmers markets,
so it catches direct-sale farms with no CSA. Organised by county.

**3. Real Organic Project directory** — `realorganicproject.org/directory`
Every farm clears a **higher** bar than USDA organic: produce must be grown in soil, not
hydroponically. Entries carry structured fields — sells CSA / wholesale / farmers market /
on-farm store — **plus exact coordinates**, which no other source provides.

**4. CCOF directory** — `ccof.org/directory-member/<slug>/`
Not for discovery but for **status checking**. Carries certification type, status and date.

**5. CAFF directory** — `caff.org/directory/`
Region-filterable, with practice descriptions written by the farms themselves.

---

## The per-farm check, now that the traps are known

For a farm already on a register, only these remain:

1. **Does the website load, and is it the farm's?** A site serving gambling or pharma spam
   means the domain lapsed and was resold — a fast, reliable death signal.
2. **Any current-season signal?** Instagram bios and farm-trail directories are often the
   freshest source. "Farm share 2026 sign-up now open" beats any directory entry.
3. **If it claims certification, open the record and read the STATUS line.** Certified /
   Suspended / Surrendered / Withdrawn — only *Certified* supports the claim.
   If no record is found, search the **legal entity** name (Blosser → TKP Farms Inc;
   Massa Organics → CGD Farms).
4. **What is it actually?** CSA, farm stand, nursery, or direct-order. Directories get this
   wrong constantly.
5. **Find the one distinguishing fact.** This is the irreducible part and the whole point —
   see below.

---

## What cannot be sped up, and shouldn't be

The distinguishing facts are what make this map better than a directory:

- Shumei uses **no fertiliser at all**, not even organic
- Knoll Farms **dropped its organic certification in protest** in 2002
- Hidden Villa donates **25% of its harvest** to a food bank
- Massa Organics grazes **sheep in the almond orchard** and raises **ducks in the rice fields**
- Huerta del Valle prices its CSA **by household income**
- Gospel Flat runs a **24/7 honour-system stand**
- Mountain Bounty offers **unlimited vacation holds**
- Eatwell discloses it grows **90%+** of each box

None of these appear in any directory. They come from reading about each farm, and no
process change removes that. **Speed up the filtering; protect the reading.**

---

## Working queue — CDFA-verified, May 2026

Every farm below is a **legally registered California CSA producer as of 1 May 2026**. None
is on ROOTED yet. Existence is already established; only fit, category and the
distinguishing fact remain.

- [x] Alma Backyard Farms — **ADDED** (re-entry employment urban farm, Compton)
- [ ] Black Urban Farmers Association
- [x] Borba Farms — **ADDED** as Borba Family Farms (4 generations, Blenheim apricots, certified organic)
- [x] Brown Girl Farms — **ADDED** (African American heritage crops; detail thin, CDFA-verified)
- [~] Capay Canyon Ranch — **HELD**: almond growing, handling and marketing for a worldwide market, plus a Davis Farmers Market stall selling almonds, organic grapes and raisins. CDFA-registered but no consumer CSA found. Same direct-order question as Massa Organics.
- [x] Christine's Garden — **ADDED** (Modesto; Mediterranean varietals; detail thin)
- [x] City of Cotati Farm Share — **ADDED** as Cotati Farm Box (city-run, on permanently protected open space, ~half-share price)
- [x] The Cloverleaf Farm CSA — **ADDED** (fruit-only CSA; Ugly Fruit Club; stated living wage)
- [x] Da-Le Ranch — **ADDED** (first meat CSA on the map; pork/poultry feed undisclosed, flagged)
- [~] Deepseeded Farm — **OUT OF SCOPE**: serves the Humboldt Bay area, which J deprioritised when choosing core California only. Revisit if the map expands north.
- [~] Donald J. Crouch — **HELD** — registered under an individual's name; no farm identity findable
- [ ] Eat! By Food Access Los Angeles *(multiple registered producers)*
- [~] Feed and be Fed — **HELD**: nothing verifiable surfaced beyond the CDFA registration. Needs a dedicated lookup or a call.
- [~] Girl and Her Dog Farm — **HELD** — no California presence findable. Searches return out-of-state farms with similar names (Four Dog Farm NC, Two Dog Farms MS, Red Dog Farm WA)
- [x] Grub CSA Farm — **ADDED** (Chico; members gather their own share from tables, not pre-boxed)
- [x] Heritage Valley Family Orchard — **ADDED** (single-crop heirloom avocado CSA, shipped)
- [~] Kimberley Wine Vinegars — **NOT A FARM LISTING** — a vinegar producer. Belongs in the product catalogue if anywhere, not the food map
- [~] Lads Home Ranch — **HELD**: site is live and states regenerative practice, organic seed and organic compost, plus handcrafted spice blends. But NO LOCATION is published anywhere found, and a farm cannot go on a map without one. Needs a call.
- [~] Mellor Ranch — **HELD** — nothing verifiable beyond the CDFA registration
- [x] Old Grove Orange — **ADDED** (5th-gen farm + food hub supplying 50+ school districts)
- [~] Outer Aisle Food Hub — **HELD**: operates as a Farmigo-based buying platform ("ditch the supermarket, buy from local farmers") rather than a farm. Aggregator, not a producer — same direct-order question as Massa.
- [x] Talley Farms — **ADDED** as Talley Farms Fresh Harvest (large grower; CSA on its ~100 certified organic acres)
- [~] Tami Lyon — **HELD** — registered under an individual's name; no farm identity findable
- [x] Tanaka Farms — **ADDED** (4th-gen family farm; 10% of each box funds the host school/church)
- [x] Three Sisters Farm — **ADDED** (certified organic 2008; only 2 of 20 acres cultivated, rest habitat)
- [ ] UC Davis Student Farm — Market Garden
- [x] Urban Tilth — Farm to Table CSA — **ADDED** (sliding-scale CSA, 5 free farm stands, free harvest access)
- [x] West County Community Farm — **ADDED** (free-choice harvest model; also corrected a Laguna Farm data mix-up)

### Strong leads surfaced during the queue (not from J's list)

| Farm | Why it matters |
|---|---|
| ~~Engler Beef~~ | **ADDED** — Sonora (not Sonoma). Selectively bred for grass finishing; California start to finish; no-corn-no-soy chicken flagged as needing confirmation |
| ~~Casa Rosa Farms~~ | **ADDED** — 1840s olive grove, livestock grazed inside the orchards, beef bacon |
| Cloverfield Organic Farm (El Sobrante) | U-pick, online store, tours |
| Massa Natural Meats (N. California) | Grass-fed beef and lamb, pasture-raised heritage pork and chicken |
| Yolo Land & Cattle Co (Woodland) | 100% grass-fed Angus beef |
| ~~Tara Firma Farms~~ | **REJECTED — CSA ended 3 July 2026.** Farm open for events; store status unconfirmed. Owners recommend Stemple Creek Ranch instead |
| ~~Stemple Creek Ranch~~ | **ADDED** — Marin Carbon Project demo farm, national stewardship award Jan 2026, discloses pork feed and partner-sourced chicken |
| SoMar Farms (W. Petaluma) | Grass-fed beef and lamb, pickup at farm or Oakland |
| Silver Springs Beef / Alhambra Valley (Martinez) | 100% grass-fed beef and lamb, heritage pork, bulk or cuts |
| **Big Bluff Ranch** | **Certified organic pasture-raised chicken** — Stemple Creek's own chicken partner, so already vetted by a ranch that discloses carefully |
| Galaxy Farm (Woodland) | Organic-fed lamb |
| Hole-In-One Ranch (Janesville) | Grass-fed beef, lamb and pork |
| Dare 2 Dream Farms (Lompoc) | Free-range eggs, organic produce, backyard chickens — CSA currently sold out |
| ~~Tara Firma Farms~~ | **REJECTED — CSA ended 3 July 2026** |
| **Farm to My Neighborhood** | Nonprofit tech platform letting very small organic farmers sell direct — no weekly commitment, neighbourhood drop sites. Described as a top recommendation by Edible East Bay |
| South Central Farmers (LA / Bakersfield) | CSA boxes into greater LA with UCLA drop points |
| Esperanza's 7 Plus Organics Co-op | Co-op of small farmers of colour in the Pajaro/Salinas Valleys |
| Twisted Fields | Pasture-raised rainbow hen eggs, rotational grazing |
| Front Porch Farm (Sonoma) | 110 acres — heritage vegetables, olives, heirloom polenta corn, flowers |

**The meat leads are now the largest gap-filling opportunity on the map.** There is one meat
CSA listed (Da-Le Ranch) against 63 produce CSAs, and seven credible grass-fed operations
are captured above.
| Santa Cruz Permaculture | Organic fruit, vegetables, flowers, herbs |

### CDFA queue: CLOSED

**Resolved 28 of 28.** Outcome:

| Result | Count |
|---|---|
| **Added to the map** | 13 |
| Already on ROOTED | 1 |
| Held — real but unverifiable, or no published location | 8 |
| Held — aggregator or direct-order, pending the type decision | 3 |
| Not a farm listing | 1 |
| Out of scope (Humboldt) | 1 |
| Duplicate registrations of farms already added | 1 |

**13 additions from 28 candidates — 46%.** Lower than it looks in one respect and better in
another: nothing on this list turned out to be *defunct*. Every hold was an information gap,
not a dead business. That is the difference between working from a state register and
working from an app directory, where a third of entries were closed or wrong.

The remaining holds cluster into two kinds, and neither is worth more searching:
- **Registered under an individual's name** (Tami Lyon, Donald J. Crouch) with no farm
  identity to find.
- **No published location** (LADS Home Ranch), which makes a map listing impossible.

Both need a phone call, not another lookup.

**28 pre-validated farms from a single fetch**, against roughly 1–2 leads per search under
the old method.

The register also confirmed 10 of 11 ROOTED farms it lists, which is independent
corroboration of work already done.

---

## Batching: the ceremony was the bottleneck, not the research

Through the first 60 farms, each one got its own verify → gate → commit → push cycle. That
overhead is identical whether one farm is added or eight, and it was most of the elapsed
time.

**From here:**

1. **Batch commits — 6–8 farms per gate/commit cycle.** Per-farm verification is unchanged;
   only the ceremony is amortised.
2. **Fetch directory and register pages, not farm pages.** A regional directory returns
   15–25 farms with practice text written by the farms themselves. One lookup, many farms.
3. **Tier the depth.** A farm that is CDFA-registered, has a live site and states its own
   practices does not need dedicated research — the register already proved existence.
   Reserve deep digging for ambiguity, certification claims, or anything that will be
   asserted as fact in an entry.
4. **Check local news for anything high-value.** A regional newspaper caught Tara Firma's
   CSA closing within two weeks; no directory had updated a month later. For any lead that
   would become a flagship listing, search the local paper before writing the entry.
5. **Shorter commit messages.** Reasoning belongs in the entry and the standards docs, which
   are what get read. A commit message does not need to restate them.

**Batching by region also improves accuracy.** The Laguna / West County conflation was
caught precisely because the two were worked adjacently. Density surfaces errors that
isolated checking misses.

**Honest limit:** searching several farm names at once does not work — results collapse onto
whichever farm has the strongest web presence. Batch by *source*, not by query.

## Directory snippets can merge two farms — read for the seam

Twice now a search snippet has blended two different farms' details:

- A CAFF page under the slug `green-valley-community-farm` carried **West County Community
  Farm's** address and description while appearing beside **Laguna Farm's** text. West
  County's 1720 Cooper Rd and its "200+ varieties" ended up in the Laguna Farm entry and had
  to be corrected.
- An Open Silo directory snippet ran **ALMA Backyard Farms'** description straight into
  **Farm Lot 59's** — the "22-member CSA" and "60 animal-welfare approved hens" in that block
  belong to Farm Lot, not ALMA. Caught before it reached the entry.

**Watch for the seam.** A sentence that switches subject without naming the new one — "Farm
Lot is a proud advocate…" mid-paragraph — means the snippet has moved on. Any number that
appears without the farm being named alongside it should be traced to the farm's own source
before use.

## Recommended split with the parallel session

Two chats have been working this list concurrently and collided once. Suggested division:

- **This session:** the CDFA-verified queue above
- **Other session:** the remaining Localize entries
- **Always** `git pull` first and check `FARMS-HELD-NEEDS-CONTACT.md` before researching

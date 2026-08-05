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
- [ ] Borba Farms
- [x] Brown Girl Farms — **ADDED** (African American heritage crops; detail thin, CDFA-verified)
- [ ] Capay Canyon Ranch
- [ ] Christine's Garden
- [ ] City of Cotati Farm Share (Veronda-Falletti Ranch)
- [x] The Cloverleaf Farm CSA — **ADDED** (fruit-only CSA; Ugly Fruit Club; stated living wage)
- [ ] Da-Le Ranch
- [ ] Deepseeded Farm
- [ ] Donald J. Crouch
- [ ] Eat! By Food Access Los Angeles *(multiple registered producers)*
- [ ] Feed and be Fed
- [ ] Girl and Her Dog Farm
- [ ] Grub CSA Farm
- [ ] Heritage Valley Family Orchard
- [ ] Kimberley Wine Vinegars
- [ ] Lads Home Ranch
- [ ] Mellor Ranch
- [x] Old Grove Orange — **ADDED** (5th-gen farm + food hub supplying 50+ school districts)
- [ ] Outer Aisle Food Hub
- [x] Talley Farms — **ADDED** as Talley Farms Fresh Harvest (large grower; CSA on its ~100 certified organic acres)
- [ ] Tami Lyon
- [x] Tanaka Farms — **ADDED** (4th-gen family farm; 10% of each box funds the host school/church)
- [ ] Three Sisters Farm
- [ ] UC Davis Student Farm — Market Garden
- [x] Urban Tilth — Farm to Table CSA — **ADDED** (sliding-scale CSA, 5 free farm stands, free harvest access)
- [x] West County Community Farm — **ADDED** (free-choice harvest model; also corrected a Laguna Farm data mix-up)

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
4. **Shorter commit messages.** Reasoning belongs in the entry and the standards docs, which
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

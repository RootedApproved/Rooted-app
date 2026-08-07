# Los Angeles farmers markets — collision map

Built before any LA import, from the 1 July 2026 register.

- LA register rows (hospital-campus already excluded): **156**
- Rows that are markets ALREADY on the map under a different name: **29**
- **Genuinely new LA markets to add: 127**

> **Corrected 6 Aug 2026 — the first figures here were 35 and 121, and both were wrong.**
> The table listed 35 register-row *mentions* but only 32 *distinct* rows: three rows were
> claimed by two map listings each. Three more were false collisions on name overlap. See
> "Two counting errors" below before using any number on this page.

`scripts/checks.js` catches these automatically now — token overlap, singularised,
LA/Los Angeles aliased, scoped to within one mile and to non-chain listing types.
This table is the human-readable version. Check it before adding any LA entry.

| Already on the map | Register row(s) | Note |
|---|---|---|
| Brentwood Farmers' Market | `Brentwood Farmers Market` — Sun. 9am - 2pm, Year Round |  |
| Century City Certified Farmers Market | `Century City Certified Farmers Market` — Thu 10am - 2pm, Year Round |  |
| Culver City Farmers Market | `Culver City Farmers Market` — Tue 2 - 7pm, Year Round |  |
| Hermosa Beach Farmers Market | `Hermosa Beach Certified Farmers Market` — Fri 12pm - 4pm, Year Round |  |
| Historic Downtown Farmers Market | `Historic Downtown LA Farmers' Market` — Sun 10am - 3pm, Year- Round |  |
| Hollywood Farmers' Market | `Hollywood Farmer's Market` — Sun 8am - 1pm, Year Round | Matches 1600 Ivar Ave. East/North Hollywood are NOT this market — see below |
| LA City Hall Farmers Market | `Los Angeles City Hall CFM` — Wed 10am - 2pm, Year Round |  |
| LA Rivers Farmers' Market | `LA River Farmers' Market (LARFM)` — Thu 3 - 7:30pm, Year Round |  |
| Malibu Farmers Market | `Malibu Farmers Market` — Sun 9am - 2pm, Year Round |  |
| Manhattan Beach Certified Farmers' Market | `Manhattan Beach Farmers' Market` — Tues 11am - 3pm, Year Round |  |
| Mar Vista Farmers' Market | `Mar Vista Farmers Market` — Sun 9am - 2pm, Year Round |  |
| Marina Del Rey Farmers Market | `Marina del Rey Farmers' Market` — Sat 9am - 2pm, Year- Round |  |
| Miracle Mile Certified Farmers Market | `Miracle Mile Farmers Market` — Wed. 11am - 2pm, Year Round |  |
| Motor Avenue Farmers Market (Palms) | `Motor Avenue Farmers Market` — Sun 9am - 2pm, Year Round |  |
| Pacific Palisades Farmers Market | `Pacific Palisades Certified Farmers Market` — Sun. 8am - 2pm, Year Round |  |
| Pasadena Certified Farmers' Market at Villa Parke | `Pasadena Villa Parke Farmers Market` — Tue 8am - 12pm, Year Round |  |
| Pasadena Victory Park Farmer's Market | `Pasadena Victory Park Farmers' Market` — Sat 8am - 12pm, Year Round |  |
| Playa Vista Farmers' Market | `Playa Vista Farmers' Market` — Sat/W ed 9am - 2pm/4p m-8pm, Year Round |  |
| Santa Monica Farmers Market — Downtown | `Santa Monica Farmers Market - Saturday Downtown` — Sat 8am - 1pm, Year Round <br> `Santa Monica Farmers Market - Wednesday Downtown` — Wed 8am - 1pm, Year Round | **2 sessions, one place** (Arizona Ave) |
| Santa Monica Farmers Market — Main Street (Sunday) | `Santa Monica Farmers Market - Sunday Main St.` — Sun 8:30am - 1:30pm, Year Round |  |
| Santa Monica Farmers Market — Pico (Saturday) | `Santa Monica Farmers Market - Saturday Pico` — Sat 8am - 1pm, Year Round | Virginia Avenue Park, distinct from Downtown |
| Silver Lake Farmers Market | `Silver Lake Certified Farmers' Market Sat` — Sat 8am - 1:30pm, Year Round <br> `Silver Lake Certified Farmers' Market Tues` — Tue 1:30 - 7pm, Year Round | **2 rows, one place** |
| Social District Farmers' Market | `Social Districts Farmers' Market` — Sat 9am - 2pm, Year Round |  |
| South Pasadena Farmer's Market | `South Pasadena Certified Farmers' Market` — Thu 4pm - 8pm, Year Round | Matches 920 Meridian Ave. `South Lake Pasadena CFM` is a different market — see below |
| Venice Farmers' Market | `Venice Farmers' Market` — Fri 7 - 11am, Year Round |  |
| West LA Farmers' Market | `West LA Farmers Market` — Sunda y 9am - 2pm, Year Round |  |
| Westwood Village Farmers' Market | `Westwood Village Farmers' Market` — Thu 12pm - 5pm, Year Round |  |

## Two counting errors — found 6 Aug 2026

**Error 1: three rows were counted twice.** The table listed 35 register-row mentions but
only 32 distinct rows. `South Pasadena Certified Farmers' Market` was claimed by both the
Victory Park and the South Pasadena listings; `Santa Monica Saturday Downtown` and
`Saturday Pico` were each claimed by both the Downtown and the Pico listings. A row can
only belong to one place.

**Error 2: three rows were suppressed by name overlap, and they are real markets.**
Checked against the live catalogue, not against this file:

| Register row | Why it was suppressed | Reality |
|---|---|---|
| `East Hollywood Certified Farmers Market` | token match on "Hollywood" | No East Hollywood market on the map. Only Hollywood Farmers' Market, 1600 Ivar Ave |
| `North Hollywood Farmers Market` | token match on "Hollywood" | NoHo is ~10 miles from Hollywood, over the hill in the Valley. Not on the map |
| `South Lake Pasadena CFM` | token match on "South…Pasadena" | South Lake Ave in Pasadena, not the city of South Pasadena. Not on the map |

**These three go back into the add queue** — but as candidates, not as confirmed adds. The
register is stale roughly 25% of the time, so each still needs its operator's own page
before it goes on the map.

**Why this happened, so the next collision map avoids it.** This table was built by hand
and is looser than `scripts/checks.js`, which it claims to mirror. checks.js scopes a
collision to within one mile; North Hollywood would never have passed that. A hand-built
table that says "the script catches these automatically" invites everyone to trust the
table instead of running the script. **Run checks.js. Then check its hits against the live
catalogue.** Name similarity is a prompt to look, never a finding.

## The register can be more than a year out of date

**Pacific Palisades is the proof.** The July 2026 register still lists it as Sunday
8am–2pm year-round. That market has not run on a Sunday since the January 2025
Palisades Fire closed the village business district. The map already records it as
returning Wednesdays from 19 August 2026 — over a year ahead of the state.

**So the LA import must never overwrite an existing entry.** Where the register and
an existing entry disagree, the existing entry wins unless an operator page settles
it. Add only rows with no counterpart in the table above.

## One pin per place, not per session

The register lists one row per market *session*. Santa Monica is four rows across
three locations; Silver Lake is two rows at one corner; Larchmont is two rows in one
car park. Two pins at the same coordinates is a map defect, so sessions get combined
into a single entry's `schedules` field. The map already does this for Silver Lake.

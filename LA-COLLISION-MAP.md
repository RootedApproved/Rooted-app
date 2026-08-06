# Los Angeles farmers markets — collision map

Built before any LA import, from the 1 July 2026 register.

- LA register rows (hospital-campus already excluded): **156**
- Rows that are markets ALREADY on the map under a different name: **35**
- **Genuinely new LA markets to add: 121**

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
| Hollywood Farmers' Market | `East Hollywood Certified Farmers Market` — Mon/T hu 3:30pm - 7:30pm, Year- Round <br> `Hollywood Farmer's Market` — Sun 8am - 1pm, Year Round <br> `North Hollywood Farmers Market` — Sat 8:30am - 1:30pm, Year Round | **3 rows, one place** |
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
| Pasadena Victory Park Farmer's Market | `Pasadena Victory Park Farmers' Market` — Sat 8am - 12pm, Year Round <br> `South Pasadena Certified Farmers' Market` — Thu 4pm - 8pm, Year Round | **2 rows, one place** |
| Playa Vista Farmers' Market | `Playa Vista Farmers' Market` — Sat/W ed 9am - 2pm/4p m-8pm, Year Round |  |
| Santa Monica Farmers Market — Downtown | `Santa Monica Farmers Market - Saturday Downtown` — Sat 8am - 1pm, Year Round <br> `Santa Monica Farmers Market - Saturday Pico` — Sat 8am - 1pm, Year Round <br> `Santa Monica Farmers Market - Wednesday Downtown` — Wed 8am - 1pm, Year Round | **3 rows, one place** |
| Santa Monica Farmers Market — Main Street (Sunday) | `Santa Monica Farmers Market - Sunday Main St.` — Sun 8:30am - 1:30pm, Year Round |  |
| Santa Monica Farmers Market — Pico (Saturday) | `Santa Monica Farmers Market - Saturday Downtown` — Sat 8am - 1pm, Year Round <br> `Santa Monica Farmers Market - Saturday Pico` — Sat 8am - 1pm, Year Round | **2 rows, one place** |
| Silver Lake Farmers Market | `Silver Lake Certified Farmers' Market Sat` — Sat 8am - 1:30pm, Year Round <br> `Silver Lake Certified Farmers' Market Tues` — Tue 1:30 - 7pm, Year Round | **2 rows, one place** |
| Social District Farmers' Market | `Social Districts Farmers' Market` — Sat 9am - 2pm, Year Round |  |
| South Pasadena Farmer's Market | `South Lake Pasadena CFM` — Tue 10am - 2pm, Year- Round <br> `South Pasadena Certified Farmers' Market` — Thu 4pm - 8pm, Year Round | **2 rows, one place** |
| Venice Farmers' Market | `Venice Farmers' Market` — Fri 7 - 11am, Year Round |  |
| West LA Farmers' Market | `West LA Farmers Market` — Sunda y 9am - 2pm, Year Round |  |
| Westwood Village Farmers' Market | `Westwood Village Farmers' Market` — Thu 12pm - 5pm, Year Round |  |

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

#!/usr/bin/env python3
"""
One-shot backfill: record the coordinate audit's results as DATA, not as digit count.

Background. Verified coordinates used to be marked by padding them to 4 decimal places.
That marker was unusable within days: padding is silent, reproducible by accident, and
was applied to entries nobody had checked. 68 listings ended up stored at 4dp carrying
3dp or less of real information, including the two explicitly flagged as unverified.

Replacement: two explicit fields.

  coord_verified  true  — the pin was geocoded from the address the listing displays,
                          and the returned address matched it. Absent means unverified.
                          Boolean, never a string; it cannot be produced by rounding.
  coord_scope     'address' — a specific street address point.
                  'block'   — a block range or corner; no single true point exists.
                  'region'  — deliberately coarse; the listing names an area, not an address.

Sources for this backfill are the git diffs of the audit commits, not the prose summary
in OPEN-ITEMS.md. Two entries the prose implies were verified are deliberately excluded;
see EXCLUDED below.
"""
import re
import sys

INDEX = 'Index.html'

# Coordinates changed by an audit commit after an address-matched geocode.
VERIFIED_ADDRESS = [
    "APC Farm2Market",
    "Blosser Urban Garden",
    "Carmel Valley Certified Farmers Market",
    "Del Monte Shopping Center Friday Market",
    "Dig Deep Farms",
    "Downtown Novato Community Farmers' Market",
    "Eatwell Farm",
    "Farm Fresh To You (Capay Organic)",
    "Fifth Crow Farm",
    "Fox Sparrow Farm",
    "Gospel Flat Farm Stand",
    "Huarache Farms",
    "Huerta del Valle Harvest Box",
    "Knoll Farms (Tairwa Produce)",
    "LADS Home Ranch",
    "Live Earth Farm CSA",
    "Los Osos Valley Organic Farm (formerly Clark Valley Organic Farm)",
    "Monterey Bay Certified Farmers Market",
    "Petaluma Bounty Farm",
    "Pichudo Mexican Grill",
    "Pie Ranch Farmstand",
    "Route One Farmers Market",
    "SLO Tuesday Farmers Market at Farm Supply",
    "San Luis Obispo Saturday Farmers Market",
    "Sarvodaya Farms & Nursery",
    "Singing Frogs Farm",
    "Something Good Organics (John Givens Farm)",
    "Spade & Plow Organics",
    "St. Helena Farmers Market",
    "Stemple Creek Ranch",
    "Sunday Turtle Bay Market",
    "Talley Farms Fresh Harvest",
    "The River Park Farmers Market",
    "Thorne Family Farm",
    "Three Sisters Farm",
    "Thursday Marin Market",
    "Tierra Vegetables",
    "Trader Joe's (Cerritos)",
    "Trader Joe's (San Diego - Carmel Mountain Rd)",
    "Urban Tilth \\u2014 Farm to Table CSA",
    "West County Community Farm",
    # Checked and found already accurate, so no coordinate changed and no diff records
    # them. Verification is exactly what the new field exists to state.
    "Jimbo's...Naturally! (4S Ranch)",
    "Whole Foods Market (Santa Rosa - Coddingtown Mall)",
    "Erewhon (Hollywood)",
    "Yountville Certified Farmers' Market",
]

VERIFIED_BLOCK = [
    "Carpinteria Farmers Market",   # "800 block of Linden Ave" — no single point exists
]

# Re-geocoded now, because they were verified accurate but STORED at the padded 3dp
# value, which the new 'address' scope assertion rightly refuses. Confirms the original
# finding in each case rather than moving the pin anywhere new.
RECOORD = {
    "Trader Joe's (Cerritos)":                (33.868967, -118.058037),   # 5 m
    "Jimbo's...Naturally! (4S Ranch)":        (33.019000, -117.113841),   # 15 m
    "Yountville Certified Farmers' Market":   (38.401066, -122.359990),   # 136 m
}

# EXCLUDED, deliberately, with reasons — do not "fix" by adding these.
#
#   Old Town Salinas Farmers Market — its coordinate DID change in f8fb36c, but as a
#     merge artefact: two register rows describing one market were collapsed and the
#     survivor inherited the deleted row's 3dp value. Nothing was geocoded. It belongs
#     in the queue, not the verified set.
#
#   Trader Joe's (San Jose) — the Tier C sample records "Trader Joe's San Jose 0m" but
#     the catalogue holds four San Jose Trader Joe's and the note does not say which.
#     Marking the wrong one verified is worse than leaving all four unmarked.
#
#   Erewhon (Santa Monica) — sampled in Tier C and found 638 m out. It was measured,
#     not corrected. Still unverified; needs working like any other queue entry.
#
#   GRUB CSA Farm, Serendipity Farms — both resolved as still-trading with mailing-address
#     conflicts, but neither received an address-matched geocode. Still unverified.


def main():
    src = open(INDEX, encoding='utf-8').read()
    original = src
    edits = 0
    failures = []

    def locate(name):
        needle = 'listing_name:"' + name + '"'
        idx = src.index(needle) if needle in src else -1
        if idx == -1:
            return None
        if src.count(needle) != 1:
            return 'AMBIGUOUS'
        line_start = src.rindex('\n', 0, idx) + 1
        line_end = src.index('\n', idx)
        return (line_start, line_end)

    # Step 1 — apply the three re-geocodes.
    for name, (lat, lon) in RECOORD.items():
        pos = locate(name)
        if pos in (None, 'AMBIGUOUS'):
            failures.append(f'RECOORD: cannot uniquely locate {name!r} ({pos})')
            continue
        s, e = pos
        line = src[s:e]
        new = re.sub(r'location_x:-?\d+(?:\.\d+)?', f'location_x:{lon:.6f}', line)
        new = re.sub(r'location_y:-?\d+(?:\.\d+)?', f'location_y:{lat:.6f}', new)
        if new == line:
            failures.append(f'RECOORD: no-op on {name!r}')
            continue
        src = src[:s] + new + src[e:]
        edits += 1

    # Step 2 — stamp the schema fields.
    for names, scope in ((VERIFIED_ADDRESS, 'address'), (VERIFIED_BLOCK, 'block')):
        for name in names:
            pos = locate(name)
            if pos in (None, 'AMBIGUOUS'):
                failures.append(f'STAMP: cannot uniquely locate {name!r} ({pos})')
                continue
            s, e = pos
            line = src[s:e]
            if 'coord_verified' in line:
                failures.append(f'STAMP: {name!r} already carries coord_verified')
                continue
            m = re.search(r'location_y:-?\d+(?:\.\d+)?', line)
            if not m:
                failures.append(f'STAMP: {name!r} has no location_y')
                continue
            ins = m.end()
            new = (line[:ins] + f",coord_verified:true,coord_scope:'{scope}'"
                   + line[ins:])
            # The assertion that matters: a print statement is not verification.
            assert new != line, f'string replacement was a no-op for {name!r}'
            src = src[:s] + new + src[e:]
            edits += 1

    if failures:
        print('FAILURES — nothing written:')
        for f in failures:
            print('  ' + f)
        sys.exit(1)

    assert src != original, 'FATAL: file unchanged after all edits'
    expected = len(VERIFIED_ADDRESS) + len(VERIFIED_BLOCK) + len(RECOORD)
    assert edits == expected, f'expected {expected} edits, made {edits}'

    open(INDEX, 'w', encoding='utf-8').write(src)
    print(f'edits applied: {edits}')
    print(f'  re-geocoded : {len(RECOORD)}')
    print(f'  scope address: {len(VERIFIED_ADDRESS)}')
    print(f'  scope block  : {len(VERIFIED_BLOCK)}')
    print(f'coord_verified now present on: {src.count("coord_verified:true")} listings')


if __name__ == '__main__':
    main()

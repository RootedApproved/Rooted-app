#!/usr/bin/env python3
"""
Regenerate the coordinate audit queue from the LIVE catalogue in Index.html.

Why this exists: OPEN-ITEMS.md carried a hand-maintained tally that was wrong every
time it was checked, because parallel sessions kept adding listings. Never quote a
queue size from a document. Run this.

    python3 scripts/coord-queue.py            # summary
    python3 scripts/coord-queue.py --list     # full queue, ready to work through

Two precisions matter:
  stored    - decimal places as written in the file
  effective - decimal places after stripping trailing zeros

They differ because coordinates have been padded to 4dp by hand. A padded value looks
verified and is not. Effective precision is the honest signal; sort by it.
"""
import re
import sys
import json

INDEX = 'Index.html'
STREET = re.compile(
    r'\b(st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|ln|lane|way|hwy|highway'
    r'|pkwy|parkway|ct|court|pl|place|ter|terrace|cir|circle|sq|square|row|trail|trl'
    r'|loop|alley)\b\.?', re.I)
HOUSE_NUMBER = re.compile(r'^\s*\d')


def load(path=INDEX):
    src = open(path, encoding='utf-8').read()
    start = src.index('const CURATED_LISTINGS = [')
    block = src[start:src.index('\n];', start)]
    out = []
    for line in block.split('\n'):
        if '_type:' not in line:
            continue

        def s(key):
            m = re.search(key + r':"((?:[^"\\]|\\.)*)"', line)
            return m.group(1) if m else ''

        def n(key):
            m = re.search(key + r':(-?\d+(?:\.\d+)?)', line)
            return m.group(1) if m else None

        x, y = n('location_x'), n('location_y')
        if x is None or y is None:
            continue
        t = re.search(r"_type:'([^']*)'", line)
        out.append(dict(name=s('listing_name'), addr=s('location_address'),
                        city=s('location_city'), state=s('location_state'),
                        zipc=s('location_zipcode'), typ=t.group(1) if t else '?',
                        x=x, y=y))
    return out


def stored_dp(v):
    return len(v.split('.')[1]) if '.' in v else 0


def effective_dp(v):
    return len(v.split('.')[1].rstrip('0')) if '.' in v else 0


def geocodable(addr):
    """Has an address specific enough to geocode and compare against what's displayed."""
    if not addr.strip():
        return False
    return bool(HOUSE_NUMBER.search(addr) or STREET.search(addr))


def main():
    rows = load()
    for r in rows:
        r['stored'] = max(stored_dp(r['x']), stored_dp(r['y']))
        r['eff'] = max(effective_dp(r['x']), effective_dp(r['y']))
        r['geo'] = geocodable(r['addr'])

    queue = sorted((r for r in rows if r['eff'] <= 3 and r['geo']),
                   key=lambda r: (r['eff'], r['name']))
    region = [r for r in rows if r['eff'] <= 3 and not r['geo']]
    padded = [r for r in rows if r['stored'] >= 4 > r['eff']]

    print(f"catalogue: {len(rows)} listings")
    print(f"QUEUE  (effective <=3dp, has a street address): {len(queue)}")
    print(f"  of which stored at 4dp+ and therefore currently invisible: "
          f"{sum(1 for r in queue if r['stored'] >= 4)}")
    print(f"region-only at <=3dp (a coarse pin is honest here): {len(region)}")
    print(f"padded (stored 4dp+, effectively <=3dp): {len(padded)}")
    print("\nnote: the address test is deliberately loose — it accepts a street suffix")
    print("without a house number, so a handful of queue entries ('Lichau Road,")
    print("Penngrove', 'Highway 1, Valley Ford') will turn out to be region")
    print("descriptions and should be held, not geocoded. Over-including and holding")
    print("is the safe direction; the reverse hides unverified pins.")

    if '--list' in sys.argv:
        print("\n-- QUEUE --")
        for r in queue:
            flag = '  <-- PADDED, looks verified and is not' if r['stored'] >= 4 else ''
            print(f"[eff {r['eff']}dp / stored {r['stored']}dp] {r['name']}{flag}\n"
                  f"    {r['addr']}, {r['city']}, {r['state']} {r['zipc']}\n"
                  f"    pinned {r['y']}, {r['x']}")
    if '--json' in sys.argv:
        json.dump(queue, open('coord-queue.json', 'w'), indent=1)
        print("\nwrote coord-queue.json")


if __name__ == '__main__':
    main()

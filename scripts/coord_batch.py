#!/usr/bin/env python3
"""
Work a slice of the coordinate queue.

    python3 scripts/coord_batch.py 0 12          # report only, writes /tmp/batch.json
    python3 scripts/coord_batch.py 0 12 --apply  # apply the OK rows to Index.html

Classification, and the bias is deliberate — holding is cheap, a moved pin is not:

  OK     the returned address matched the displayed address. Safe to apply.
  FAR    matched, but lands >25 km from the current pin. Never auto-applied. A jump
         that large is the Serendipity failure shape (a Carmel farm nearly relocated
         400 km to Shasta County) and gets read by a human before it moves.
  HOLD   no match, no result, or an address the listing does not display.

Applying only ever writes a coordinate whose address matched. Everything else is
reported and left alone.
"""
import json
import re
import sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geocode import geocode_listing, haversine_km, house_number, is_block_or_intersection

sys.path.insert(0, '.')
import importlib.util
_spec = importlib.util.spec_from_file_location('cq', 'scripts/coord-queue.py')
cq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cq)

FAR_KM = 25.0
# A match with no house number is the ROAD's representative point, so the road's own
# extent is the error bar. East Castle St, Mount Shasta spans 140 m and its centroid is
# the address to within that; El Camino Real, Atascadero spans 11 km and its centroid
# means nothing. Measure the geocode's uncertainty rather than guessing from how far the
# current pin sits — distance-from-pin conflates "geocode is vague" with "pin is wrong".
STREET_EXTENT_MAX_KM = 0.8


def build_queue():
    rows = cq.load()
    for r in rows:
        r['stored'] = max(cq.stored_dp(r['x']), cq.stored_dp(r['y']))
        r['eff'] = max(cq.effective_dp(r['x']), cq.effective_dp(r['y']))
        r['geo'] = cq.geocodable(r['addr'])
    return sorted((r for r in rows if not r['verified'] and r['eff'] <= 3 and r['geo']),
                  key=lambda r: (r['eff'], r['name']))


def scope_for(addr):
    """A block range or a bare corner has no single true point; say so rather than
    pretending to address precision."""
    if is_block_or_intersection(addr) or not re.search(r'\d', addr or ''):
        return 'block'
    return 'address'


def main():
    start = int(sys.argv[1])
    count = int(sys.argv[2])
    apply_ = '--apply' in sys.argv

    queue = build_queue()
    # Applied entries leave the queue but HOLD and REVIEW entries stay in it, so a plain
    # offset would re-geocode them every batch. Skip anything already worked; the evidence
    # files are the record of what that is.
    import glob
    worked = set()
    for f in glob.glob('/home/claude/audit-results/batch_*.json'):
        for r in json.load(open(f)):
            worked.add(r['name'])
    remaining = [r for r in queue if r['name'] not in worked]
    batch = remaining[:count] if start < 0 else remaining[start:start + count]
    print(f'queue {len(queue)} | already worked {len(worked)} | '
          f'remaining {len(remaining)} | this batch {len(batch)}\n')

    results = []
    for i, r in enumerate(batch, max(start, 0)):
        cur_y, cur_x = float(r['y']), float(r['x'])
        g = geocode_listing(r)
        rec = dict(idx=i, name=r['name'], addr=r['addr'], city=r['city'],
                   zipc=r['zipc'], typ=r['typ'], cur=(cur_y, cur_x))
        if g['status'] == 'ok':
            km = haversine_km(cur_y, cur_x, g['lat'], g['lon'])
            street_only = g.get('street_only')
            rec.update(new=(g['lat'], g['lon']), km=km, display=g['display'],
                       via=g['via'], street_only=street_only,
                       extent_km=g.get('extent_km'),
                       scope='block' if street_only else scope_for(r['addr']))
            if km > FAR_KM:
                rec['status'] = 'FAR'
            elif street_only and (g.get('extent_km') is None
                                  or g['extent_km'] > STREET_EXTENT_MAX_KM):
                # Road too long for its centroid to locate anything. Atascadero's pin sits
                # on the right junction already; this is what stops it being moved 7.9 km
                # to the middle of an 11 km road.
                rec['status'] = 'REVIEW'
            else:
                rec['status'] = 'OK'
        else:
            rec.update(status='HOLD', reasons=g['reasons'])
        results.append(rec)

        tag = rec['status']
        print(f"[{i}] {tag}  {r['name']}")
        print(f"     {r['addr']}, {r['city']} {r['zipc']}")
        if tag in ('OK', 'FAR', 'REVIEW'):
            d = rec['km']
            dtxt = f'{d * 1000:.0f} m' if d < 1 else f'{d:.2f} km'
            print(f"     {cur_y},{cur_x}  ->  {rec['new'][0]:.6f},{rec['new'][1]:.6f}"
                  f"   drift {dtxt}  [{rec['scope']}]")
            print(f"     matched: {rec['display'][:105]}")
        else:
            for x in rec['reasons']:
                print(f"     - {x[:130]}")
        print()

    ok = [r for r in results if r['status'] == 'OK']
    far = [r for r in results if r['status'] == 'FAR']
    review = [r for r in results if r['status'] == 'REVIEW']
    hold = [r for r in results if r['status'] == 'HOLD']
    print(f'OK {len(ok)} | REVIEW {len(review)} | FAR {len(far)} | HOLD {len(hold)}')
    json.dump(results, open('/tmp/batch.json', 'w'), indent=1)
    # Persist per-batch so the review/hold log can be regenerated from evidence rather
    # than retyped, which is how tallies drift.
    import os
    os.makedirs('/home/claude/audit-results', exist_ok=True)
    json.dump(results, open(f'/home/claude/audit-results/batch_{start:03d}.json', 'w'),
              indent=1)

    if not apply_:
        print('\n(report only — rerun with --apply to write)')
        return

    src = open('Index.html', encoding='utf-8').read()
    written = 0
    for r in ok:
        needle = 'listing_name:"' + r['name'] + '"'
        if src.count(needle) != 1:
            print(f'SKIP (not unique): {r["name"]}')
            continue
        idx = src.index(needle)
        s = src.rindex('\n', 0, idx) + 1
        e = src.index('\n', idx)
        line = src[s:e]
        assert 'coord_verified' not in line, f'{r["name"]} already verified'
        new = re.sub(r'location_x:-?\d+(?:\.\d+)?',
                     f'location_x:{r["new"][1]:.6f}', line)
        new = re.sub(r'location_y:-?\d+(?:\.\d+)?',
                     f'location_y:{r["new"][0]:.6f}', new)
        m = re.search(r'location_y:-?\d+(?:\.\d+)?', new)
        new = (new[:m.end()] + f",coord_verified:true,coord_scope:'{r['scope']}'"
               + new[m.end():])
        assert new != line, f'string replacement was a no-op for {r["name"]}'
        src = src[:s] + new + src[e:]
        written += 1
    open('Index.html', 'w', encoding='utf-8').write(src)
    print(f'\napplied: {written}')


if __name__ == '__main__':
    main()

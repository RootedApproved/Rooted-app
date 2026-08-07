#!/usr/bin/env python3
"""
Work the entries Nominatim held, using Census (addresses) and Overpass (corners).

    python3 scripts/coord_batch2.py 12                 # report, writes a run file
    python3 scripts/coord_batch2.py --apply <runfile>   # apply the OK rows of THAT file

Same separation as coord_batch.py, for the same reason: applying must not re-resolve, or
what gets written is not what was reviewed.

Order of attempt per listing:
  1. If the address names a corner, resolve the corner via Overpass. A corner has no
     address, so this is the only correct question for it.
  2. Otherwise try Census, and confirm the point by reverse geocoding it through
     Nominatim against the displayed address.

Scope recorded honestly: 'address' for a confirmed street address, 'block' for a corner
or a block between two cross streets.
"""
import json
import re
import sys
import importlib.util
import glob
import os
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geocode import haversine_km, house_number
from geocode2 import (census_point, confirm_by_reverse, corner_point,
                      parse_corner, OverpassUnavailable)

_spec = importlib.util.spec_from_file_location('cq', 'scripts/coord-queue.py')
cq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cq)

FAR_KM = 25.0
WORKED = '/home/claude/audit-results2'


def build_queue():
    rows = cq.load()
    for r in rows:
        r['eff'] = max(cq.effective_dp(r['x']), cq.effective_dp(r['y']))
        r['geo'] = cq.geocodable(r['addr'])
    return sorted((r for r in rows if not r['verified'] and r['eff'] <= 3 and r['geo']),
                  key=lambda r: (r['eff'], r['name']))


def resolve(r):
    """Returns rec fields for one listing."""
    cur_y, cur_x = float(r['y']), float(r['x'])
    if parse_corner(r['addr']):
        try:
            c = corner_point(r)
        except OverpassUnavailable as e:
            # Distinct from a miss, and NOT recorded as worked — the listing must come
            # back round rather than be filed as "no crossing node found".
            return dict(status='error', reasons=[f'overpass unavailable: {e}'])
        if c:
            return dict(status='ok', lat=c['lat'], lon=c['lon'], via='overpass-corner',
                        detail=c['detail'], scope='block', span_km=c.get('span_km'))
        # Not every parse that LOOKS like a corner is one. "100 Corte Madera Town Center
        # at Hwy 101" is an address beside a highway, not two crossing streets, and
        # holding it on a failed crossing query wastes a perfectly good address. Fall
        # through to Census rather than treating a mis-parse as an unresolvable corner.
        corner_failed = 'overpass: no crossing node for the named streets'
    else:
        corner_failed = None
    got = census_point(r)
    if not got:
        rs = ['census: no match']
        if corner_failed:
            rs.insert(0, corner_failed)
        return dict(status='hold', reasons=rs)
    lat, lon, matched = got
    ok, why = confirm_by_reverse(lat, lon, r)
    if not ok:
        rs = [f'census matched "{matched}" but {why}']
        if corner_failed:
            rs.insert(0, corner_failed)
        return dict(status='hold', reasons=rs)
    return dict(status='ok', lat=lat, lon=lon, via='census+reverse',
                detail=f'census: {matched} | {why}',
                scope='address' if house_number(r['addr']) else 'block')


def main():
    os.makedirs(WORKED, exist_ok=True)
    if sys.argv[1] == '--apply':
        apply_run(sys.argv[2])
        return
    count = int(sys.argv[1])
    census_only = '--census-only' in sys.argv

    worked = set()
    for f in glob.glob(WORKED + '/run_*.json'):
        for x in json.load(open(f)):
            worked.add(x['name'])
    queue = [r for r in build_queue() if r['name'] not in worked]
    batch = queue[:count]
    print(f'held queue {len(queue) + len(worked)} | worked {len(worked)} | '
          f'this batch {len(batch)}\n')

    results = []
    for i, r in enumerate(batch):
        cur_y, cur_x = float(r['y']), float(r['x'])
        if census_only and parse_corner(r['addr']):
            continue  # corner entries need Overpass; leave them queued
        g = resolve(r)
        rec = dict(idx=i, name=r['name'], addr=r['addr'], city=r['city'],
                   zipc=r['zipc'], typ=r['typ'], cur=(cur_y, cur_x))
        if g['status'] == 'ok':
            km = haversine_km(cur_y, cur_x, g['lat'], g['lon'])
            rec.update(new=(g['lat'], g['lon']), km=km, via=g['via'],
                       detail=g['detail'], scope=g['scope'])
            rec['status'] = 'FAR' if km > FAR_KM else 'OK'
        elif g['status'] == 'error':
            rec.update(status='ERROR', reasons=g['reasons'])
        else:
            rec.update(status='HOLD', reasons=g['reasons'])
        results.append(rec)

        print(f"[{i}] {rec['status']}  {r['name']}")
        print(f"     {r['addr'][:95]}, {r['city']} {r['zipc']}")
        if rec['status'] in ('OK', 'FAR'):
            d = rec['km']
            print(f"     {cur_y},{cur_x} -> {rec['new'][0]:.6f},{rec['new'][1]:.6f}"
                  f"   drift {d * 1000:.0f} m [{rec['scope']}] via {rec['via']}")
            print(f"     {rec['detail'][:120]}")
        else:
            for x in rec['reasons']:
                print(f"     - {x[:140]}")
        print()

    ok = [x for x in results if x['status'] == 'OK']
    print(f"OK {len(ok)} | FAR {sum(1 for x in results if x['status'] == 'FAR')} | "
          f"HOLD {sum(1 for x in results if x['status'] == 'HOLD')}")
    err = [x for x in results if x['status'] == 'ERROR']
    if err:
        print(f'ERROR {len(err)} — resolver unavailable; NOT recorded as worked')
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    path = f'{WORKED}/run_{stamp}.json'
    # Errors are excluded from the evidence file so they re-enter the queue. A listing
    # nobody could REACH must not be filed alongside one nobody could resolve.
    json.dump([x for x in results if x['status'] != 'ERROR'], open(path, 'w'), indent=1)
    print(f'\nrun file: {path}')
    print(f'apply with: python3 scripts/coord_batch2.py --apply {path}')


def apply_run(path):
    results = json.load(open(path))
    ok = [r for r in results if r['status'] == 'OK']
    print(f'{path}: {len(results)} rows, {len(ok)} OK')
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
        new = re.sub(r'location_x:-?\d+(?:\.\d+)?', f'location_x:{r["new"][1]:.6f}', line)
        new = re.sub(r'location_y:-?\d+(?:\.\d+)?', f'location_y:{r["new"][0]:.6f}', new)
        m = re.search(r'location_y:-?\d+(?:\.\d+)?', new)
        new = new[:m.end()] + f",coord_verified:true,coord_scope:'{r['scope']}'" + new[m.end():]
        assert new != line, f'string replacement was a no-op for {r["name"]}'
        src = src[:s] + new + src[e:]
        written += 1
    open('Index.html', 'w', encoding='utf-8').write(src)
    print(f'\napplied: {written}')


if __name__ == '__main__':
    main()

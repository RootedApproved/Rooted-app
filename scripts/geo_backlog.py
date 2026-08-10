#!/usr/bin/env python3
"""
Geocode every CDFA register market not yet on the map, using the rules the audit
established. Writes evidence per market; applies nothing.

Order of attempt, all held to "the returned address must match the displayed address":
  1. Nominatim on the address (structured then freeform, via the query normaliser)
  2. Census + Nominatim reverse confirmation
  3. Overpass crossing, where the location names a corner rather than a building

Register locations are written for humans and carry venue prefixes, cross streets,
parcel numbers and block ranges, so the normaliser matters more here than anywhere.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from geocode import geocode_listing, haversine_km, house_number
from geocode2 import (census_point, confirm_by_reverse, corner_point, parse_corner,
                      OverpassUnavailable)

OUT = '/home/claude/market-geo'


def split_loc(loc):
    """Register 'Market Location' -> (street part, city, zip)."""
    m = re.search(r'^(.*?),\s*([A-Za-z .\'-]+?)[, ]+(?:CA[, ]*)?(\d{5})\s*$', loc)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    m = re.search(r'^(.*?)\s+([A-Za-z .\'-]+?)\s+CA\s+(\d{5})\s*$', loc)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    return loc.strip(), None, None


def resolve(rec):
    street, city, z = split_loc(rec['loc'])
    if not city:
        return dict(status='hold', reasons=['register location has no parseable city/zip'])
    L = dict(name=rec['name'], addr=street, city=city, state='CA', zipc=z,
             x='0', y='0')
    # 1. Nominatim
    g = geocode_listing(L)
    if g['status'] == 'ok' and not g.get('street_only'):
        return dict(status='ok', lat=g['lat'], lon=g['lon'], via='nominatim',
                    detail=g['display'], street=street, city=city, zipc=z,
                    scope='address' if house_number(street) else 'block')
    nomi = g
    # 2. Census + reverse
    c = census_point(L)
    if c:
        ok, why = confirm_by_reverse(c[0], c[1], L)
        if ok:
            corner = '&' in c[2]
            return dict(status='ok', lat=c[0], lon=c[1], via='census+reverse',
                        detail=f'census: {c[2]} | {why}', street=street, city=city,
                        zipc=z,
                        scope='address' if (house_number(street) and not corner) else 'block')
    # 3. Overpass corner
    if parse_corner(street):
        L2 = dict(L, y='0', x='0')
        try:
            # anchor on the Nominatim street-only hit if there was one, else city centre
            if nomi['status'] == 'ok':
                L2['y'], L2['x'] = str(nomi['lat']), str(nomi['lon'])
                cp = corner_point(L2)
                if cp:
                    return dict(status='ok', lat=cp['lat'], lon=cp['lon'],
                                via='overpass-corner', detail=cp['detail'],
                                street=street, city=city, zipc=z, scope='block')
        except OverpassUnavailable as e:
            return dict(status='error', reasons=[f'overpass unavailable: {e}'])
    # 4. Street-only Nominatim hit, admitted only if the road is short enough
    if nomi['status'] == 'ok' and nomi.get('street_only'):
        ex = nomi.get('extent_km')
        if ex is not None and ex <= 0.8:
            return dict(status='ok', lat=nomi['lat'], lon=nomi['lon'],
                        via='nominatim-street', detail=f'{nomi["display"]} (road spans '
                                                       f'{ex * 1000:.0f} m)',
                        street=street, city=city, zipc=z, scope='block')
        return dict(status='hold', reasons=[
            f'only a street-level match, road spans '
            f'{"unknown" if ex is None else "%.1f km" % ex} — centroid locates nothing'])
    return dict(status='hold', reasons=['no address-matched result from Nominatim, '
                                        'Census or Overpass'])


def main():
    os.makedirs(OUT, exist_ok=True)
    todo = json.load(open('/home/claude/todo_markets.json'))
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(todo)
    batch = todo[start:start + count]
    results = []
    t0 = time.time()
    for i, rec in enumerate(batch):
        try:
            g = resolve(rec)
        except Exception as e:
            g = dict(status='error', reasons=[f'{type(e).__name__}: {e}'])
        out = dict(rec)
        out.update(g)
        out['idx'] = start + i
        results.append(out)
        if (i + 1) % 10 == 0:
            ok = sum(1 for r in results if r['status'] == 'ok')
            print(f'{i + 1}/{len(batch)}  ok={ok}  '
                  f'{(time.time() - t0) / (i + 1):.1f}s/market', flush=True)
            json.dump(results, open(f'{OUT}/geo_{start:04d}.json', 'w'), indent=1)
    json.dump(results, open(f'{OUT}/geo_{start:04d}.json', 'w'), indent=1)
    ok = sum(1 for r in results if r['status'] == 'ok')
    print(f'DONE {len(results)} | ok {ok} | hold '
          f'{sum(1 for r in results if r["status"] == "hold")} | err '
          f'{sum(1 for r in results if r["status"] == "error")}', flush=True)


if __name__ == '__main__':
    main()

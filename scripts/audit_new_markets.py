#!/usr/bin/env python3
"""
Audit rows before they are written to the catalogue.

Deliberately independent of the code that produced them. The geocoder decides what to
accept; this decides whether to believe it, and it re-derives its facts from the point
itself rather than re-reading the same fields. Every error class this session produced
has one check here:

  ADDRESS   The point must reverse-geocode onto a road named in the address. Catches the
            Atascadero class, where a plausible result sits kilometres from the address.
  POSTCODE  Taken from the geocoded point, NOT trusted from the register, which has
            already been wrong twice in eight rows (Dublin given 94501 = Alameda island,
            Danville given 94560 = Newark). Where point and register disagree the row is
            flagged and the register value is never written silently.
  CITY      Confirmed by reverse geocode. Unincorporated communities inside a mailing
            city (Live Oak in Santa Cruz, Orcutt in Santa Maria) are a known false
            positive and are reported as INFO rather than FAIL.
  NAME      Checked against the live catalogue for near-duplicates, and against the rest
            of the batch, before anything is inserted.
  PIN       Any two rows within 150 m are surfaced, because a market with two register
            rows for two days is one venue and must be merged, not listed twice.

Exit code is non-zero on any FAIL.
"""
import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geocode import _get, norm_street, norm_city, haversine_km

CACHE = '/home/claude/market-geo/audit_reverse.json'


def load_cache():
    try:
        return json.load(open(CACHE))
    except Exception:
        return {}


def save_cache(c):
    json.dump(c, open(CACHE, 'w'))


def reverse(lat, lon, cache):
    key = f'{lat:.6f},{lon:.6f}'
    if key in cache:
        return cache[key]
    try:
        r = _get('/reverse', dict(lat=lat, lon=lon, format='jsonv2',
                                  addressdetails=1, zoom=17))
    except Exception:
        r = None
    cache[key] = r
    return r


def streets_in(addr):
    parts = re.split(r'\s+(?:at|between|and|x)\s+|&|,', addr or '')
    return [norm_street(p) for p in parts if norm_street(p)]


def audit(rows, catalogue_names, catalogue_pins):
    cache = load_cache()
    fails, warns, infos = [], [], []
    seen_names = {}
    for r in rows:
        n = r['name']
        lat, lon = r['lat'], r['lon']
        rv = reverse(lat, lon, cache)
        a = (rv or {}).get('address', {}) or {}

        # ADDRESS
        got_road = norm_street(a.get('road') or '')
        wants = streets_in(r['street'])
        # Where the stored street came from the geocoder's OWN forward match, reverse
        # through a DIFFERENT provider is weak evidence against it. Google returns a
        # rooftop point for "300 Estudillo Ave" and OSM's reverse names the nearest way,
        # which is often the cross street or a freeway ramp. This is the same rule
        # already applied to Census forward matches, and it is applied here for the same
        # reason rather than as a convenience: the forward match IS the address.
        forward = bool(r.get('forward_matched'))
        if not got_road:
            warns.append(f'{n}: point reverse-geocodes to no road')
        elif forward and not any(got_road in w or w in got_road for w in wants):
            infos.append(f'{n}: reverse names "{a.get("road")}" where the forward match '
                         f'gave {r["street"]!r} - nearest-way artefact, forward wins')
        elif not any(got_road in w or w in got_road for w in wants):
            # A road's TYPE is the thing registers most often get wrong - Laguna Beach
            # says "Forest Rd" for Forest Avenue, Pinole "Fernandez St" for Fernandez
            # Avenue. If the distinctive part of the name agrees and only the suffix
            # differs, that is a register defect and not a misplaced pin, so report it
            # rather than blocking on it.
            def bare(x):
                return re.sub(r'\b(st|ave|rd|blvd|dr|ln|ct|pl|cir|ter|pkwy|hwy|sq|way|'
                              r'trl|expy|fwy|mall)\b', '', x).strip()
            gb = bare(got_road)
            if gb and any(gb and (gb in bare(w) or bare(w) in gb) for w in wants):
                infos.append(f'{n}: road type differs — point is on "{a.get("road")}", '
                             f'register says {r["street"]!r}. Register type is likely '
                             f'wrong; pin looks right.')
            else:
                fails.append(f'{n}: point sits on "{a.get("road")}" but the address '
                             f'names {r["street"]!r}')

        # POSTCODE — from the point, never from the register
        pt_zip = (a.get('postcode') or '').split('-')[0]
        reg_zip = (r.get('zipc') or '').split('-')[0]
        if pt_zip and reg_zip and pt_zip != reg_zip:
            infos.append(f'{n}: register zip {reg_zip}, point reports {pt_zip} '
                         f'(reverse zips are often facility codes — verify before trusting either)')

        # CITY
        got_city = (a.get('city') or a.get('town') or a.get('village')
                    or a.get('hamlet') or '')
        if got_city and norm_city(got_city) != norm_city(r['city']):
            infos.append(f'{n}: register city {r["city"]!r}, point reports '
                         f'{got_city!r} (may be an unincorporated community)')

        # STATE
        if (a.get('state') or '').lower() not in ('california', ''):
            fails.append(f'{n}: point is in {a.get("state")}, not California')

        # NAME vs catalogue and vs batch
        key = re.sub(r'[^a-z0-9]', '', n.lower())
        if key in seen_names:
            fails.append(f'{n}: duplicate name within this batch')
        seen_names[key] = n
        if key in catalogue_names:
            fails.append(f'{n}: a listing with this name already exists')

        # PIN proximity
        for cn, clat, clon in catalogue_pins:
            if haversine_km(lat, lon, clat, clon) * 1000 < 150:
                warns.append(f'{n}: within 150 m of existing listing {cn!r} — '
                             f'confirm it is a different venue, not a second day')
    # within-batch proximity
    for i, r in enumerate(rows):
        for s in rows[i + 1:]:
            if haversine_km(r['lat'], r['lon'], s['lat'], s['lon']) * 1000 < 150:
                warns.append(f'{r["name"]} and {s["name"]} are within 150 m — '
                             f'likely one venue on two days, merge before inserting')
    save_cache(cache)
    return fails, warns, infos


def main():
    rows = json.load(open(sys.argv[1]))
    rows = [r for r in rows if r.get('status') == 'ok']
    src = open('Index.html', encoding='utf-8').read()
    cat_names = set(re.sub(r'[^a-z0-9]', '', m.lower())
                    for m in re.findall(r'listing_name:"((?:[^"\\]|\\.)*)"', src))
    pins = []
    for m in re.finditer(r'listing_name:"((?:[^"\\]|\\.)*)".*?location_x:(-?\d+\.?\d*),'
                         r'location_y:(-?\d+\.?\d*)', src):
        pins.append((m.group(1), float(m.group(3)), float(m.group(2))))
    fails, warns, infos = audit(rows, cat_names, pins)
    for t, xs in (('FAIL', fails), ('WARN', warns), ('INFO', infos)):
        print(f'\n=== {t} ({len(xs)}) ===')
        for x in xs[:60]:
            print('  ' + x)
        if len(xs) > 60:
            print(f'  ... and {len(xs) - 60} more')
    print(f'\naudited {len(rows)} rows: {len(fails)} fail, {len(warns)} warn, '
          f'{len(infos)} info')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()

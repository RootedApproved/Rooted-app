#!/usr/bin/env python3
"""
Resolve register locations that name a VENUE rather than a street.

About 129 California markets give a location no street geocoder can use: "North Valley
Plaza, Chico", "Alex Thomas Plaza, Ukiah", "Devendorf Park", "Market Street, Chico".
Census and Nominatim index streets and addresses; these are points of interest, and the
two are different indexes. Photon searches OSM by name and finds them.

THE OBVIOUS OBJECTION, ANSWERED
The standing rule is "geocode the address, never the business name" - a name query once
returned a farm 400 km from the one being audited. That rule is not broken here, but it
is close enough to deserve care. What is being sent is the VENUE the register itself
names as the location, not the market's business name, and never the market's name. So
"Alex Thomas Plaza" is sent, "Ukiah Certified Farmers' Market" is not.

The Serendipity failure was a name resolving to a same-named thing in the wrong county,
so three guards apply:
  1. the result's city must match the register's city, or
  2. the result must sit within 12 km of the register city's own centre, and
  3. the returned feature's NAME must overlap the venue named, so that a query for
     "Devendorf Park" cannot be satisfied by an unrelated park that merely ranked first.
A result failing any guard is held, not applied.
"""
import json
import re
import time
import urllib.parse
import urllib.request

UA = 'ROOTED-market-verify/1.0 (team@rootedapproved.com)'
_last = [0.0]


def _get(url):
    w = 1.1 - (time.time() - _last[0])
    if w > 0:
        time.sleep(w)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        _last[0] = time.time()
        return json.loads(r.read().decode())


def photon(q, lat=None, lon=None, limit=5):
    p = {'q': q, 'limit': limit}
    if lat is not None:
        p.update({'lat': lat, 'lon': lon})
    return _get('https://photon.komoot.io/api/?' + urllib.parse.urlencode(p))


def venue_candidates(loc):
    """
    Pull the venue-ish phrases out of a register location string.

    "Fruitvale BART Station, 3301 E 12th St" -> ["Fruitvale BART Station"]
    "North Valley Plaza, Chico, 95927, East Ave" -> ["North Valley Plaza"]
    Segments that are plainly a street address or a bare postcode are skipped: those are
    the street geocoder's job and it has already failed on them.
    """
    a = re.sub(r'\s+', ' ', (loc or '')).strip()
    a = re.split(r'[\u2014\u2013]', a.replace('\\u2014', '\u2014'))[0]
    out = []
    for seg in a.split(','):
        s = seg.strip(' .')
        if not s or len(s) < 4:
            continue
        if re.fullmatch(r'\d{5}(-\d{4})?', s):
            continue
        if re.match(r'^\d+\s', s):          # starts with a house number
            continue
        if re.search(r'\b(x|at|between|&)\b', s, re.I) and not re.search(
                r'\b(plaza|park|square|center|centre|mall|station|library|college|'
                r'school|hall|church|museum|fairground|campus|lot)\b', s, re.I):
            continue
        out.append(s)
    # prefer segments that actually look like a named place
    named = [s for s in out if re.search(
        r'\b(plaza|park|square|center|centre|mall|station|library|college|school|hall|'
        r'church|museum|fairground|campus|commons|village|marketplace|depot)\b', s, re.I)]
    return (named + [s for s in out if s not in named])[:3]


def norm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', (s or '').lower()).strip()


def name_overlap(a, b):
    ta = {w for w in norm(a).split() if len(w) > 2}
    tb = {w for w in norm(b).split() if len(w) > 2}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def resolve_venue(name, loc, city, anchor=None, city_centre=None):
    """Returns dict(status, lat, lon, detail) - never applies anything itself."""
    cands = venue_candidates(loc)
    if not cands:
        return dict(status='hold', why='no venue-like phrase in the register location')
    tried = []
    for v in cands:
        q = f'{v}, {city}, California' if city else f'{v}, California'
        try:
            d = photon(q, *(anchor if anchor else (None, None)))
        except Exception as e:
            tried.append(f'{v}: request failed ({type(e).__name__})')
            continue
        for f in (d.get('features') or []):
            pr = f.get('properties') or {}
            c = f['geometry']['coordinates']
            lat, lon = c[1], c[0]
            got_city = pr.get('city') or pr.get('town') or pr.get('village') or ''
            # guard 1/2 - locality
            ok_city = bool(city and got_city and norm(got_city) == norm(city))
            ok_near = False
            if city_centre:
                from math import radians, sin, cos, asin, sqrt
                dla = radians(lat - city_centre[0])
                dlo = radians(lon - city_centre[1])
                h = (sin(dla / 2) ** 2 + cos(radians(city_centre[0]))
                     * cos(radians(lat)) * sin(dlo / 2) ** 2)
                ok_near = 2 * 6371.0088 * asin(sqrt(h)) <= 12.0
            if not (ok_city or ok_near):
                tried.append(f'{v}: "{pr.get("name")}" is in {got_city or "?"}, not {city}')
                continue
            # guard 3 - the feature must actually be the venue named
            ov = name_overlap(v, pr.get('name'))
            if ov < 0.5:
                tried.append(f'{v}: top hit "{pr.get("name")}" does not match the venue named')
                continue
            return dict(status='ok', lat=lat, lon=lon, venue=v,
                        detail=f'photon: {pr.get("name")} ({pr.get("osm_key")}='
                               f'{pr.get("osm_value")}) in {got_city or city}',
                        overlap=round(ov, 2))
    return dict(status='hold', why='; '.join(tried[:3]) or 'no acceptable venue match')

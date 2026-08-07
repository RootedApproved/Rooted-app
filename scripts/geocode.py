#!/usr/bin/env python3
"""
Geocode a listing's DISPLAYED ADDRESS and decide whether the result may be applied.

Two rules are enforced in code because both have already been broken by hand:

  1. Query the address, never the business name. A name query returned a farm 400 km
     from the one being audited (Serendipity Farms, Carmel -> Anderson). The business
     name is never sent to the geocoder here. It is used only to report.

  2. Accept only a result whose RETURNED address matches the address the listing
     DISPLAYS. A geocoder answers the query it was given, not the question you meant.
     `100 W 1st St, Los Angeles` returns a house in Long Beach; the match test is the
     only thing standing between that and a moved pin.

Anything that fails the match test is returned as HOLD, never as a correction.
"""
import json
import re
import time
import urllib.parse
import urllib.request

UA = 'ROOTED-coord-audit/1.0 (team@rootedapproved.com)'
BASE = 'https://nominatim.openstreetmap.org'
_last_call = [0.0]
MIN_INTERVAL = 1.1  # Nominatim usage policy: max 1 request/second


def _get(path, params):
    """Rate-limited GET against Nominatim."""
    wait = MIN_INTERVAL - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    url = BASE + path + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA,
                                               'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                _last_call[0] = time.time()
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 + attempt * 3)
    return None


# ---------------------------------------------------------------- normalising

SUFFIX = {
    'street': 'st', 'avenue': 'ave', 'road': 'rd', 'boulevard': 'blvd',
    'drive': 'dr', 'lane': 'ln', 'court': 'ct', 'place': 'pl', 'circle': 'cir',
    'terrace': 'ter', 'parkway': 'pkwy', 'highway': 'hwy', 'square': 'sq',
    'trail': 'trl', 'expressway': 'expy', 'freeway': 'fwy',
}
DIRECTION = {'north': 'n', 'south': 's', 'east': 'e', 'west': 'w',
             'northeast': 'ne', 'northwest': 'nw',
             'southeast': 'se', 'southwest': 'sw'}


def norm_street(s):
    """Reduce a street string to comparable tokens: '1720 Cooper Road' -> 'cooper rd'."""
    s = (s or '').lower()
    s = re.sub(r'#.*$', '', s)                 # unit numbers
    s = re.sub(r'\bsuite\b.*$', '', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    out = []
    for t in s.split():
        if t.isdigit():
            continue                            # house numbers compared separately
        t = DIRECTION.get(t, t)
        t = SUFFIX.get(t, t)
        out.append(t)
    return ' '.join(out).strip()


def house_number(s):
    m = re.match(r'\s*(\d+)', s or '')
    return m.group(1) if m else None


def norm_city(s):
    s = (s or '').lower().strip()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return {'la': 'los angeles', 'sf': 'san francisco'}.get(s, s)


def is_block_or_intersection(addr):
    """Block ranges and corners have no single true point; they geocode to the street."""
    a = (addr or '').lower()
    return bool(re.search(r'\bblocks?\b', a) or ' x ' in a
                or re.search(r'\b(at|and|&|between)\b', a) and not house_number(addr))


# ---------------------------------------------------------------- the check

def match_verdict(listing, result):
    """
    Return (ok: bool, reason: str). ok=True only when the returned address agrees
    with what the listing displays.
    """
    addr = result.get('address', {}) or {}
    got_city = norm_city(addr.get('city') or addr.get('town') or addr.get('village')
                         or addr.get('hamlet') or addr.get('suburb') or '')
    want_city = norm_city(listing['city'])
    got_road = norm_street(addr.get('road') or '')
    want_road = norm_street(listing['addr'])
    got_hn = addr.get('house_number')
    want_hn = house_number(listing['addr'])
    got_pc = (addr.get('postcode') or '').split('-')[0]
    want_pc = (listing.get('zipc') or '').split('-')[0]
    got_state = (addr.get('state') or '').lower()

    if got_state and got_state != 'california':
        return False, f'returned {addr.get("state")}, not California'

    # Locality test. City alone is NOT sufficient: Nominatim reports San Pedro's city
    # as "Los Angeles", so `100 W 1st St, Los Angeles 90012` matched a San Pedro house
    # 34 km away on city agreement alone. Where both sides carry a postcode it is the
    # discriminator and must agree. City is the fallback only when a postcode is missing.
    city_ok = bool(got_city and want_city and got_city == want_city)
    pc_ok = bool(got_pc and want_pc and got_pc == want_pc)
    if got_pc and want_pc:
        if not pc_ok:
            return False, (f'postcode mismatch: got {got_pc} '
                           f'({addr.get("city") or addr.get("town") or "?"}) '
                           f'vs displayed {want_pc} ({listing["city"]})')
    elif not city_ok:
        return False, (f'city mismatch and no postcode to fall back on: got '
                       f'"{addr.get("city") or addr.get("town") or "?"}" '
                       f'vs displayed "{listing["city"]}"')

    if not want_road:
        return False, 'listing has no street to match against'
    if not got_road:
        return False, 'result carries no road'

    # Street must agree. Substring both ways covers "Cooper Rd" vs "Cooper Road N".
    if not (got_road == want_road or got_road in want_road or want_road in got_road):
        return False, f'street mismatch: got "{addr.get("road")}" vs displayed "{listing["addr"]}"'

    if want_hn:
        if not got_hn:
            return False, f'displayed house number {want_hn} but result has none (street-level only)'
        if got_hn != want_hn:
            return False, f'house number mismatch: got {got_hn} vs displayed {want_hn}'

    return True, 'address matches'


def geocode_listing(listing, limit=5):
    """
    listing: dict with addr, city, state, zipc (name is NOT sent to the geocoder).
    Returns dict(status='ok'|'hold', ...).
    """
    tried = []
    # Structured query first — it is the least ambiguous form available.
    queries = [
        ('structured', dict(street=listing['addr'], city=listing['city'],
                            state=listing.get('state') or 'CA', country='USA')),
        ('freeform', dict(q=f"{listing['addr']}, {listing['city']}, "
                            f"{listing.get('state') or 'CA'} {listing.get('zipc') or ''}".strip())),
    ]
    for label, params in queries:
        p = dict(params, format='jsonv2', addressdetails=1, limit=limit,
                 countrycodes='us')
        try:
            res = _get('/search', p)
        except Exception as e:
            tried.append(f'{label}: request failed ({e})')
            continue
        if not res:
            tried.append(f'{label}: no results')
            continue
        for r in res:
            ok, reason = match_verdict(listing, r)
            if ok:
                return dict(status='ok', lat=float(r['lat']), lon=float(r['lon']),
                            display=r.get('display_name', ''), via=label,
                            osm=f"{r.get('osm_type')}/{r.get('osm_id')}")
        tried.append(f'{label}: {len(res)} results, best rejected — '
                     + match_verdict(listing, res[0])[1])
    return dict(status='hold', reasons=tried)


def haversine_km(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, asin, sqrt
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat / 2) ** 2
         + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2)
    return 2 * 6371.0088 * asin(sqrt(a))

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


ORDINAL = {'first': '1st', 'second': '2nd', 'third': '3rd', 'fourth': '4th',
           'fifth': '5th', 'sixth': '6th', 'seventh': '7th', 'eighth': '8th',
           'ninth': '9th', 'tenth': '10th', 'eleventh': '11th', 'twelfth': '12th',
           'thirteenth': '13th', 'fourteenth': '14th', 'fifteenth': '15th',
           'sixteenth': '16th', 'seventeenth': '17th', 'eighteenth': '18th',
           'nineteenth': '19th', 'twentieth': '20th'}
# Registers abbreviate directionals inconsistently: "So." for South, "No." for North.
DIR_ABBR = {'so': 's', 'no': 'n', 'ea': 'e', 'we': 'w'}


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
        # "100 S SECOND St" and "South 2ND Street" are the same road, and comparing them
        # as written produced a wall of false failures — 10 of 14 in the first audit run.
        t = ORDINAL.get(t, t)
        t = DIR_ABBR.get(t, t)
        t = DIRECTION.get(t, t)
        t = SUFFIX.get(t, t)
        out.append(t)
    return ' '.join(out).strip()


def house_number(s):
    """
    The house number, wherever it sits in the string.

    Anchoring this to the start of the string was a silent hole. Listings routinely lead
    with the venue — "Truckee River Regional Park, 10500 Brockway Rd" — so the anchored
    version returned None, the "displayed house number must match" test was skipped
    entirely, and a street-only match was accepted for an address that names a specific
    building. Prefer the number in the comma-segment that actually looks like a street.
    """
    s = s or ''
    for seg in s.split(','):
        if STREET_WORD.search(seg):
            m = re.search(r'\b(\d+)\b(?=\s+\S)', seg)
            if m:
                return m.group(1)
    m = re.match(r'\s*(\d+)', s)
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


STREET_WORD = re.compile(
    r'\b(st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|ln|lane|way|hwy|highway'
    r'|pkwy|parkway|ct|court|pl|place|ter|terrace|cir|circle|sq|square|row|trail|trl'
    r'|loop|alley|expy|expressway|fwy|freeway|mall)\b\.?', re.I)


def query_forms(addr):
    """
    Progressively cleaner query strings for one displayed address.

    Listing addresses are written for humans and carry things a geocoder takes literally:
    cross streets ("632 East Alisal St AT PEARL ST"), block ranges ("800 BLOCK OF Linden
    Ave"), venue prefixes ("Crane Park, 360 Crane Ave"), lot descriptors ("East Castle St
    PARKING LOT"), and prose after an em-dash ("Lichau Road, Penngrove — AT THE FOOT OF
    SONOMA MOUNTAIN"). Every one of those returned zero results when sent verbatim.

    Cleaning only ever affects the QUERY. The match test still compares the result against
    the address the listing displays, so a looser query cannot loosen the acceptance rule.
    """
    a = (addr or '').replace('\\u2014', '\u2014').replace('\\u2013', '\u2013')
    # Prose after a dash describes pickup/delivery, never the location.
    a = re.split(r'[\u2014\u2013]|(?<=\s)--(?=\s)', a)[0]
    a = re.sub(r'\([^)]*\)', ' ', a)
    a = re.sub(r'\s+', ' ', a).strip().strip(',')

    forms = []

    def add(s):
        s = re.sub(r'\s+', ' ', (s or '')).strip().strip(',').strip()
        if s and s.lower() not in {f.lower() for f in forms}:
            forms.append(s)

    add(a)

    # Keep only the comma-segment that actually looks like a street, dropping venue
    # prefixes ("Crane Park") and trailing locality repeats.
    segs = [s.strip() for s in a.split(',') if s.strip()]
    street_segs = [s for s in segs if STREET_WORD.search(s) or re.match(r'^\s*\d+\s', s)]
    if street_segs:
        add(street_segs[0])

    base = street_segs[0] if street_segs else a
    # Drop cross-street and block-range language.
    cleaned = re.sub(r'\b(\d+)\s*(?:00)?\s*block of\b', '', base, flags=re.I)
    # '&' is not a word character, so \b&\b does not behave — strip it separately.
    cleaned = re.sub(r'\s*&.*$', '', cleaned)
    cleaned = re.sub(r'\s+\b(?:at|x|between|and)\b\s+.*$', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\b(parking lot|parking structure|lot|car park|plaza level)\b', '',
                     cleaned, flags=re.I)
    cleaned = re.sub(r'#\s*\S+|\bsuite\b\s*\S+|\bste\b\s*\S+', '', cleaned, flags=re.I)
    add(cleaned)

    # House number + street only.
    m = re.match(r'\s*(\d+)\s+(.+)$', cleaned)
    if m:
        m2 = STREET_WORD.search(m.group(2))
        if m2:
            add(f'{m.group(1)} {m.group(2)[:m2.end()]}')
    # "800 block of Linden Ave" MEANS the 800 house numbers on Linden Ave, so ask for
    # exactly that. It resolves to a building on the correct block where the bare street
    # name resolves to the whole road or to nothing.
    mb = re.search(r'\b(\d+)\s*block of\s+(.+)$', base, flags=re.I)
    if mb:
        add(f'{mb.group(1)} {mb.group(2)}')

    # Street without a house number — the right form for a block range or a corner.
    if cleaned:
        nohn = re.sub(r'^\s*\d+\s+', '', cleaned)
        m3 = STREET_WORD.search(nohn)
        if m3:
            add(nohn[:m3.end()])
    return forms


def has_street(addr):
    """Is there anything here a geocoder could resolve, or is it a region description?"""
    for f in query_forms(addr):
        if STREET_WORD.search(f) or re.match(r'^\s*\d+\s', f):
            return True
    return False


def geocode_listing(listing, limit=5):
    """
    listing: dict with addr, city, state, zipc (name is NOT sent to the geocoder).
    Returns dict(status='ok'|'hold', ...).
    """
    tried = []
    queries = []
    for form in query_forms(listing['addr']):
        # Structured first — it is the least ambiguous form available.
        queries.append((f'structured[{form}]',
                        dict(street=form, city=listing['city'],
                             state=listing.get('state') or 'CA', country='USA')))
        queries.append((f'freeform[{form}]',
                        dict(q=f"{form}, {listing['city']}, "
                               f"{listing.get('state') or 'CA'} "
                               f"{listing.get('zipc') or ''}".strip())))
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
                # Did this land on a building, or merely on the road?
                # A result with no house number is the road's representative point. For a
                # long road that point is arbitrary: "El Camino Real, Atascadero" resolves
                # 7.9 km from the El Camino Real / East Mall junction the listing means.
                # Callers must treat street_only results as confirmation, not correction.
                got_hn = (r.get('address') or {}).get('house_number')
                extent = None
                bb = r.get('boundingbox')
                if bb and len(bb) == 4:
                    try:
                        s_, n_, w_, e_ = (float(v) for v in bb)
                        extent = haversine_km(s_, w_, n_, e_)
                    except (TypeError, ValueError):
                        extent = None
                return dict(status='ok', lat=float(r['lat']), lon=float(r['lon']),
                            display=r.get('display_name', ''), via=label,
                            street_only=not bool(got_hn), extent_km=extent,
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

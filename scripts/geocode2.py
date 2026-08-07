#!/usr/bin/env python3
"""
Second and third sources for the coordinate audit, for the entries Nominatim cannot do.

Nominatim held 48 listings. They fail for three different reasons and only one of them is
a geocoding problem, so there are two additional resolvers here, each aimed at one shape:

  census_point()   US Census TIGER geocoder. Independent of OpenStreetMap and far better
                   on rural roads, new developments and shopping-centre addresses, which
                   is most of what OSM was missing.

  corner_point()   Overpass. For an address that names a CORNER rather than a building
                   ("Central Ave between 6th St and 9th St") there is no address to
                   resolve; the right question is where two named streets actually cross,
                   and Overpass can answer that where a geocoder cannot.

Both are held to the same rule as Nominatim: a result is only usable if it agrees with
the address the listing DISPLAYS. Neither is trusted on its own say-so.

The Census check needs one extra step. Census normalises away directionals — it answered
"777 W Cypress Ave, Redding" with "777 CYPRESS AVE". Redding has both, and a dropped
directional can silently mean a different street. So a Census point is confirmed by
REVERSE geocoding it through Nominatim and requiring the road actually at that point to
match what the listing displays. Two independent sources agreeing on one address is a
stronger claim than either alone, and it closes the normalisation hole rather than
hoping it does not bite.
"""
import json
import re
import time
import urllib.parse
import urllib.request

from geocode import (UA, _get, match_verdict, norm_street, house_number,
                     haversine_km)

CENSUS = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress'
OVERPASS = ['https://overpass-api.de/api/interpreter',
            'https://overpass.kumi.systems/api/interpreter']

_last = [0.0]


def _throttle(gap=1.0):
    w = gap - (time.time() - _last[0])
    if w > 0:
        time.sleep(w)
    _last[0] = time.time()


# ------------------------------------------------------------------ Census

def census_point(listing, addr_form=None):
    """Geocode via Census. Returns (lat, lon, matched_address) or None."""
    street = addr_form or listing['addr']
    one = f"{street}, {listing['city']}, {listing.get('state') or 'CA'} " \
          f"{listing.get('zipc') or ''}".strip()
    _throttle(0.4)
    url = CENSUS + '?' + urllib.parse.urlencode(
        dict(address=one, benchmark='Public_AR_Current', format='json'))
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.loads(r.read().decode())
            break
        except Exception:
            if attempt == 2:
                return None
            time.sleep(2 + attempt * 3)
    m = (d.get('result') or {}).get('addressMatches') or []
    if not m:
        return None
    a = m[0]
    c = a['coordinates']
    matched = a.get('matchedAddress', '')
    # Census normalises directionals away — it answered "777 W Cypress Ave, Redding
    # 96003" with "777 CYPRESS AVE, REDDING, CA, 96001". The dropped "W" is invisible,
    # but the postcode it matched is not, and here it is the postcode OF THE MATCHED
    # ADDRESS rather than of a surrounding area, so a disagreement is real.
    want = (listing.get('zipc') or '').split('-')[0].strip()
    got = re.search(r'\b(\d{5})\b\s*$', matched.strip())
    if want and got and got.group(1) != want:
        return None
    return (c['y'], c['x'], matched)


def confirm_by_reverse(lat, lon, listing):
    """
    Reverse the point through Nominatim and require the road there to match the address
    the listing displays. This is what catches a dropped directional: Census can answer
    "777 CYPRESS AVE" for a query naming W Cypress, and only asking what is actually at
    the returned point will say which street it landed on.
    """
    try:
        r = _get('/reverse', dict(lat=lat, lon=lon, format='jsonv2',
                                  addressdetails=1, zoom=18))
    except Exception as e:
        return False, f'reverse failed ({e})'
    if not r or 'address' not in r:
        return False, 'reverse returned nothing'
    ok, reason = match_verdict(listing, r)
    if ok:
        return True, f'reverse confirms: {r.get("display_name", "")[:100]}'
    # Reverse lands on the nearest mapped feature, which for a large parcel can be the
    # access road rather than the street named, so a road-name agreement is allowed to
    # rescue a verdict that failed on street DETAIL. It must never rescue one that failed
    # on LOCALITY. Saturday Redding Market displays "777 W Cypress Ave, Redding 96003";
    # Census answered "777 CYPRESS AVE, REDDING, CA, 96001" — directional dropped and a
    # different postcode — and the road "Cypress Avenue" agreed, which would have waved
    # through a pin in the wrong part of Redding. Locality disagreement is exactly the
    # failure this confirmation step exists to catch, so it is terminal.
    # POSTCODE IS NOT REVERSE'S TO JUDGE. Reverse returns the ZIP of the area polygon it
    # lands in, which is routinely a post-office facility code: 95061 for Santa Cruz,
    # 93102 for Santa Barbara, 92163 for San Diego, 95929 for Chico. Eight of seventeen
    # corner results threw a "postcode mismatch" that way and every one was spurious.
    # The Redding guard is real but belongs at the FORWARD layer, where Census reports
    # the postcode of the address it actually matched — see census_point. Here, city and
    # road are the signal.
    if any(k in reason for k in ('city mismatch', 'not California')):
        return False, f'reverse disagrees on locality — {reason}'
    got = norm_street((r.get('address') or {}).get('road') or '')
    # An address that names a CORNER names two streets, and reverse will land on whichever
    # is nearer. "700-789 Cedar St at Lincoln St" was held because reverse returned Lincoln
    # Street and only Cedar was compared — reverse was corroborating the address by naming
    # the other half of the corner it displays. Compare against every street mentioned.
    want_parts = [p for p in re.split(r'\s+(?:at|between|and|x)\s+|&|,',
                                      listing['addr'] or '') if p.strip()]
    wants = [norm_street(p) for p in want_parts]
    wants.append(norm_street(listing['addr']))
    for want in [w for w in wants if w]:
        if got and (got in want or want in got):
            return True, f'reverse road agrees ({r["address"].get("road")})'
    return False, f'reverse disagrees — {reason}'


# ------------------------------------------------------------------ Overpass

ABBR = {'st': 'Street', 'ave': 'Avenue', 'av': 'Avenue', 'rd': 'Road',
        'blvd': 'Boulevard', 'dr': 'Drive', 'ln': 'Lane', 'pl': 'Place',
        'ct': 'Court', 'cir': 'Circle', 'pkwy': 'Parkway', 'hwy': 'Highway',
        'sq': 'Square', 'ter': 'Terrace', 'expy': 'Expressway', 'trl': 'Trail',
        'n': 'North', 's': 'South', 'e': 'East', 'w': 'West',
        'sts': 'Streets', 'aves': 'Avenues'}


def expand(name):
    """'E Olive Ave' -> 'East Olive Avenue'. OSM stores names in full."""
    out = []
    for t in re.split(r'\s+', (name or '').strip()):
        bare = t.strip('.').lower()
        out.append(ABBR.get(bare, t.strip('.')))
    s = ' '.join(out)
    s = re.sub(r'\bStreets\b', 'Street', s)
    s = re.sub(r'\bAvenues\b', 'Avenue', s)
    return s.strip()


def _osm_name_regex(name):
    """Match the full name, tolerating a missing or present street-type suffix."""
    e = expand(name)
    core = re.sub(r'\s+(Street|Avenue|Road|Boulevard|Drive|Lane|Place|Court|Circle|'
                  r'Parkway|Highway|Square|Terrace|Way)$', '', e, flags=re.I).strip()
    # A DIRECTIONAL PREFIX must be optional too. Listings write "2nd St" where OSM stores
    # "West 2nd Street", so a suffix-only pattern missed the road entirely and the crossing
    # query returned nothing — reported, of course, as "these streets do not cross".
    core = re.sub(r'^(North|South|East|West|N|S|E|W)\s+', '', core, flags=re.I).strip()
    return (r'^(North |South |East |West )?' + re.escape(core)
            + r'( (Street|Avenue|Road|Boulevard|Drive|Lane|Place|'
              r'Court|Circle|Parkway|Highway|Square|Terrace|Way))?$')


class OverpassUnavailable(Exception):
    """Transport failure, NOT an empty result.

    These used to be the same value. _overpass returned None when the API rate-limited
    us and None when it answered honestly that two streets do not cross, so a 503 storm
    was recorded as "no crossing node found" for five listings in a row. A failure that
    reports itself as a negative result is the same defect as the anchored house-number
    regex: the check did not fail, it did not run, and the output looked identical."""


def _overpass(query):
    last = None
    for url in OVERPASS:
        for attempt in range(3):
            _throttle(3.0)
            req = urllib.request.Request(
                url, data=urllib.parse.urlencode({'data': query}).encode(),
                headers={'User-Agent': UA})
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    return json.loads(r.read().decode())
            except Exception as e:
                last = e
                time.sleep(5 + attempt * 6)
    raise OverpassUnavailable(str(last))


_health = [None]


def overpass_healthy():
    """
    Confirm Overpass answers a query whose answer is KNOWN before trusting an empty
    result from it.

    Necessary because Overpass returns HTTP 200 with an empty element list when its
    own internal timeout fires, which is indistinguishable from an honest "these two
    streets do not cross". During an outage that silently converts every corner listing
    into a false hold - the listing gets filed as unresolvable and never revisited. A
    probe with a guaranteed answer separates "down" from "no".
    """
    if _health[0] is not None:
        return _health[0]
    # The probe must have the SHAPE of a real query, not merely be a query. A trivial
    # way-lookup passed while every actual crossing query timed out, so the first probe
    # certified a degraded service as healthy. This asks for a crossing whose answer is
    # known — 1st St and Spring St, downtown Los Angeles — so it fails when the service
    # is too slow to answer the kind of question being asked of it.
    q = ('[out:json][timeout:40];'
         '(way(around:900,34.0537,-118.2468)["highway"]["name"="West 1st Street"];)->.A;'
         '(way(around:900,34.0537,-118.2468)["highway"]["name"="North Spring Street"];)->.B;'
         'node(w.A)->.na;node(w.B)->.nb;node.na.nb;out 3;')
    try:
        d = _overpass(q)
        _health[0] = bool(d and d.get('elements'))
    except OverpassUnavailable:
        _health[0] = False
    return _health[0]


def crossing(street_a, street_b, lat, lon, radius=8000):
    """The node where two named streets cross, nearest the given anchor."""
    q = (f'[out:json][timeout:60];'
         f'(way(around:{radius},{lat},{lon})["name"~"{_osm_name_regex(street_a)}",i]'
         f'["highway"];)->.A;'
         f'(way(around:{radius},{lat},{lon})["name"~"{_osm_name_regex(street_b)}",i]'
         f'["highway"];)->.B;'
         f'node(w.A)->.na;node(w.B)->.nb;node.na.nb;out 10;')
    d = _overpass(q)
    if not d:
        return None
    els = d.get('elements') or []
    if not els:
        return None
    els.sort(key=lambda e: haversine_km(lat, lon, e['lat'], e['lon']))
    return (els[0]['lat'], els[0]['lon'])


# ------------------------------------------------------------------ parsing corners

CORNER_PATTERNS = [
    # "Central Ave between 6th St and 9th St"  -> primary + two crosses (midpoint)
    (re.compile(r'^(?P<a>.+?)\s+between\s+(?P<b>.+?)\s+(?:and|&)\s+(?P<c>.+?)$', re.I), 3),
    # "Corner of Clark Ave and Bradley Rd"
    (re.compile(r'^(?:corner of\s+)(?P<a>.+?)\s+(?:and|&|at)\s+(?P<b>.+?)$', re.I), 2),
    # "Main St and Morro Bay Blvd" / "El Camino Real & East Mall Ave" / "16th St at Canal St"
    (re.compile(r'^(?P<a>.+?)\s+(?:and|&|at|x)\s+(?P<b>.+?)$', re.I), 2),
]
NOISE = re.compile(r'\b(municipal lot.*|lot #?\d+|downtown|parking.*|near .*|west side.*)\b',
                   re.I)


def parse_corner(addr):
    """
    Pull street names out of an address that describes a corner or a block between two
    cross streets. Returns (primary, [cross...]) or None.
    """
    a = (addr or '').replace('\\u2014', '\u2014').replace('\\u2013', '\u2013')
    a = a.split('\u2014')[0].split('\u2013')[0] if '\u2014' in a else a
    a = re.sub(r'\([^)]*\)', ' ', a)
    # Drop a leading venue segment: "Devendorf Park, Ocean Ave & Sixth Ave"
    segs = [s.strip() for s in a.split(',') if s.strip()]
    cand = None
    for s in segs:
        # '&' is not a word character, so \b&\b never fires. Same blind spot that hid
        # in the query normaliser; test any pattern containing '&' explicitly.
        if '&' in s or re.search(r'\b(and|at|between|x)\b', s, re.I):
            cand = s
            break
    if cand is None:
        return None
    cand = NOISE.sub('', cand).strip(' ,')
    # Block ranges: "900-1000 blocks of State Street at Cota St" -> "State Street at Cota St"
    cand = re.sub(r'^[\d\u2013\u2014\-\s]*blocks?\s+of\s+', '', cand, flags=re.I)
    for rx, n in CORNER_PATTERNS:
        m = rx.match(cand)
        if not m:
            continue
        g = m.groupdict()
        if n == 3:
            return (g['a'].strip(), [g['b'].strip(), g['c'].strip()])
        return (g['a'].strip(), [g['b'].strip()])
    return None


def corner_point(listing):
    """
    Resolve a corner address to a point. Where the listing names a block BETWEEN two cross
    streets, the midpoint of the two junctions is the block itself, which is what the
    market occupies — better than either end.
    Returns dict(lat, lon, detail) or None.
    """
    parsed = parse_corner(listing['addr'])
    if not parsed:
        return None
    if not overpass_healthy():
        raise OverpassUnavailable('probe query returned nothing — service degraded, so '
                                  'an empty result cannot be read as "no crossing"')
    primary, crosses = parsed
    lat0, lon0 = float(listing['y']), float(listing['x'])
    pts, named = [], []
    for c in crosses:
        p = crossing(primary, c, lat0, lon0)
        if p:
            pts.append(p)
            named.append(f'{expand(primary)} x {expand(c)}')
    if not pts:
        return None
    if len(pts) == 2:
        lat = (pts[0][0] + pts[1][0]) / 2
        lon = (pts[0][1] + pts[1][1]) / 2
        span = haversine_km(*pts[0], *pts[1])
        return dict(lat=lat, lon=lon, detail=f'midpoint of {" and ".join(named)} '
                                             f'(block spans {span * 1000:.0f} m)',
                    span_km=span)
    return dict(lat=pts[0][0], lon=pts[0][1], detail=named[0], span_km=0.0)

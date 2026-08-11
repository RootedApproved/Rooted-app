#!/usr/bin/env python3
"""
Resolve a market location through Google Places (New) and the Geocoding API.

Google indexes PLACES, which is what every remaining failure needs: "North Valley
Plaza", "Alex Thomas Plaza", "Tesoro Viejo Town Center" are venues, not street
addresses, and Census, Nominatim and Photon all index streets or thin OSM POI data.
Google returns a real postal address for them - North Valley Plaza resolves to
801 East Ave, Chico 95926.

The verification discipline does NOT relax because the source got better. Google is
confident and wrong in the same ways as anything else, so:

  * the query carries the CITY, and the returned address must be in that city
  * a result more than 25 km from the register's city centre is refused outright
  * the returned address must contain a house number to be recorded as 'address'
    scope; a place centroid without one is 'block', the same rule applied to Photon
  * the market's OWN NAME is never sent alone. Where a venue is named in the
    register that venue is queried; the market name is only ever added as context
    alongside the city, never as the whole query, because a bare name query is what
    once returned a farm 400 km from the one being audited.
"""
import json
import re
import time
import urllib.parse
import urllib.request

KEY = None          # set by the caller
_last = [0.0]


def _throttle(gap=0.06):
    w = gap - (time.time() - _last[0])
    if w > 0:
        time.sleep(w)
    _last[0] = time.time()


def places_text(q, bias=None):
    body = {'textQuery': q, 'maxResultCount': 5}
    if bias:
        body['locationBias'] = {'circle': {
            'center': {'latitude': bias[0], 'longitude': bias[1]}, 'radius': 20000.0}}
    req = urllib.request.Request(
        'https://places.googleapis.com/v1/places:searchText',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'X-Goog-Api-Key': KEY,
                 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,'
                                     'places.location,places.addressComponents,'
                                     'places.businessStatus'})
    _throttle()
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def geocode(address):
    u = ('https://maps.googleapis.com/maps/api/geocode/json?'
         + urllib.parse.urlencode({'address': address, 'key': KEY}))
    _throttle()
    with urllib.request.urlopen(u, timeout=30) as r:
        return json.loads(r.read().decode())


def haversine_km(a, b, c, d):
    from math import radians, sin, cos, asin, sqrt
    dla, dlo = radians(c - a), radians(d - b)
    h = sin(dla / 2) ** 2 + cos(radians(a)) * cos(radians(c)) * sin(dlo / 2) ** 2
    return 2 * 6371.0088 * asin(sqrt(h))


def norm_city(s):
    return re.sub(r'[^a-z ]', '', (s or '').lower()).strip()


def parse_formatted(fa):
    """'801 East Ave, Chico, CA 95926, USA' -> (street, city, zip)"""
    parts = [p.strip() for p in (fa or '').split(',')]
    if len(parts) < 3:
        return fa, None, None
    street = parts[0]
    city = parts[1]
    m = re.search(r'\b([A-Z]{2})\s+(\d{5})', parts[2])
    return street, city, (m.group(2) if m else None)


def resolve(name, location_text, city, city_centre=None):
    """
    Returns dict(status='ok'|'hold', ...). Applies nothing.
    location_text is the register's own location string.
    """
    tried = []
    queries = []
    loc = re.sub(r'\s+', ' ', (location_text or '')).strip()
    loc = re.split(r'[\u2014\u2013]', loc.replace('\\u2014', '\u2014'))[0]
    if loc:
        queries.append(f'{loc}, {city}, CA' if city else f'{loc}, CA')
    # market name WITH the city as context - never the bare name
    if name and city:
        queries.append(f'{name}, {city}, CA')

    for q in queries:
        try:
            d = places_text(q, city_centre)
        except Exception as e:
            tried.append(f'{q[:40]}: request failed ({type(e).__name__})')
            continue
        for pl in (d.get('places') or []):
            fa = pl.get('formattedAddress', '')
            lat = pl['location']['latitude']
            lon = pl['location']['longitude']
            street, got_city, zipc = parse_formatted(fa)
            if city and got_city and norm_city(got_city) != norm_city(city):
                tried.append(f'"{pl["displayName"]["text"]}" is in {got_city}, not {city}')
                continue
            if city_centre and haversine_km(city_centre[0], city_centre[1], lat, lon) > 25:
                tried.append(f'"{pl["displayName"]["text"]}" is over 25 km from {city}')
                continue
            if pl.get('businessStatus') == 'CLOSED_PERMANENTLY':
                tried.append(f'"{pl["displayName"]["text"]}" is marked permanently closed')
                continue
            # A SUITE NUMBER means the match landed on a tenant of a building rather
            # than on the place. Google returned "735 State St Ste 600" for a street
            # market and "350 6th St Suite 102" for another - both in roughly the right
            # area, so no distance check catches them. Refuse them outright.
            if re.search(r'\b(ste|suite|unit|#)\s*\w+', street or '', re.I):
                tried.append(f'"{pl["displayName"]["text"]}" resolved to a suite '
                             f'({street}) - a building tenant, not the venue')
                continue
            has_number = bool(re.match(r'^\s*\d', street or ''))
            return dict(status='ok', lat=lat, lon=lon, street=street, city=got_city or city,
                        zipc=zipc, formatted=fa, place=pl['displayName']['text'],
                        scope='address' if has_number else 'block', via='google-places')
    return dict(status='hold', reasons=tried[:4] or ['no acceptable Google result'])

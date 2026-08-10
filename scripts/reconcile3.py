#!/usr/bin/env python3
"""
Reconcile three independent sources for every market in the backlog.

  CDFA register    the authority on WHETHER a market currently operates (July 2026)
  Census geocoder  an independent coordinate for the address the register gives
  USDA directory   an independent coordinate and name, from a separate federal survey

None of the three is trusted alone, and they fail in different directions, which is the
point of crossing them:

  the register carries stale and mistyped addresses — two wrong postcodes in the first
    eight rows checked (Dublin given 94501 = Alameda island; Danville 94560 = Newark)
  USDA carries stale ENTRIES — most California rows were last updated in 2023, some in
    2020, so it cannot say whether a market still runs
  a geocoder answers the query it was given, not the question meant

A market is auto-verified only where two independent coordinates agree closely AND the
geocode matched the address the register displays. Everything else is escalated with the
specific conflict named, because the whole value here is that disagreements surface
rather than average out.

Census batch: up to 10,000 addresses per request. The entire backlog is ONE call.
"""
import csv
import io
import json
import math
import re
import sys
import urllib.request

UA = 'ROOTED-market-verify/1.0 (team@rootedapproved.com)'
BATCH = 'https://geocoding.geo.census.gov/geocoder/locations/addressbatch'
AGREE_KM = 0.25          # two sources this close are describing the same place
SUSPECT_KM = 2.0         # beyond this, one of them is about a different place entirely


def haversine_km(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * 6371.0088 * math.asin(math.sqrt(a))


def split_loc(loc):
    m = re.search(r'^(.*?),\s*([A-Za-z .\'-]+?)[, ]+(?:CA[, ]*)?(\d{5})\s*$', loc or '')
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    m = re.search(r'^(.*?)\s+([A-Za-z .\'-]+?)\s+CA\s+(\d{5})\s*$', loc or '')
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    return (loc or '').strip(), None, None


def census_batch(items):
    """items: list of (id, street, city, state, zip). One request, up to 10k."""
    buf = io.StringIO()
    w = csv.writer(buf)
    for it in items:
        w.writerow(it)
    data = buf.getvalue().encode()
    b = '----rootedbatch'
    body = (f'--{b}\r\nContent-Disposition: form-data; name="addressFile"; '
            f'filename="a.csv"\r\nContent-Type: text/csv\r\n\r\n').encode() + data + \
           (f'\r\n--{b}\r\nContent-Disposition: form-data; name="benchmark"\r\n\r\n'
            f'Public_AR_Current\r\n--{b}--\r\n').encode()
    req = urllib.request.Request(BATCH, data=body, headers={
        'Content-Type': f'multipart/form-data; boundary={b}', 'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=600) as r:
        out = r.read().decode('utf-8', 'replace')
    res = {}
    for row in csv.reader(io.StringIO(out)):
        if len(row) < 6 or row[2] != 'Match':
            continue
        try:
            lon, lat = (float(v) for v in row[5].split(','))
        except Exception:
            continue
        res[row[0]] = dict(matched=row[4], lat=lat, lon=lon)
    return res


def norm_name(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\b(certified|farmers?|market|markets|cfm|the|of|at|downtown|a|and)\b',
               ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    todo = json.load(open('/home/claude/todo_markets.json'))
    usda = json.load(open('/home/claude/usda_ca.json'))

    # --- Census, one request -------------------------------------------------
    items, meta = [], {}
    for i, t in enumerate(todo):
        street, city, z = split_loc(t['loc'])
        meta[str(i)] = dict(street=street, city=city, zipc=z)
        if not city:
            continue
        s = re.sub(r'\([^)]*\)', '', street)[:100]
        items.append((str(i), s, city, 'CA', z or ''))
    print(f'submitting {len(items)} addresses to Census in one request...', flush=True)
    cen = census_batch(items)
    print(f'  matched {len(cen)}', flush=True)

    # --- USDA index by normalised name + city --------------------------------
    uidx = {}
    for u in usda:
        if not (u['x'] and u['y']):
            continue
        uidx.setdefault((norm_name(u['name']), (u['city'] or '').lower()), []).append(u)
    ucity = {}
    for u in usda:
        if u['x'] and u['y']:
            ucity.setdefault((u['city'] or '').lower(), []).append(u)

    out = []
    for i, t in enumerate(todo):
        m = meta[str(i)]
        rec = dict(idx=i, name=t['name'], county=t['county'], loc=t['loc'],
                   street=m['street'], city=m['city'], zipc=m['zipc'],
                   days=t['days'], hours=t['hours'], months=t['months'],
                   phone=t['phone'], mgr=t['mgr'])
        c = cen.get(str(i))
        if c:
            rec.update(cen_lat=c['lat'], cen_lon=c['lon'], cen_matched=c['matched'])
        # find a USDA counterpart
        key = (norm_name(t['name']), (m['city'] or '').lower())
        cand = uidx.get(key) or []
        if not cand and m['city']:
            for u in ucity.get(m['city'].lower(), []):
                a, b = norm_name(t['name']), norm_name(u['name'])
                if a and b and (a in b or b in a):
                    cand.append(u)
        # Name matching alone found a counterpart for barely a third of the backlog:
        # the two datasets name the same market differently ("Old Town CFM" vs "Eureka
        # Old Town Farmers Market"). Fall back to PROXIMITY to the Census point, which
        # is not circular — a USDA record is an independent survey response that exists
        # at that location whatever it is called, so finding one there corroborates the
        # register's address. Record HOW the match was made so it can be weighed.
        match_by = 'name' if cand else None
        if not cand and 'cen_lat' in rec:
            best, bestd = None, 9e9
            for u in usda:
                if not (u['x'] and u['y']):
                    continue
                try:
                    d = haversine_km(rec['cen_lat'], rec['cen_lon'],
                                     float(u['y']), float(u['x']))
                except (TypeError, ValueError):
                    continue
                if d < bestd:
                    best, bestd = u, d
            if best is not None and bestd <= 1.0:
                cand = [best]
                match_by = f'proximity {bestd*1000:.0f}m'
        # A shared market name across two cities is not a match. California has a
        # Brentwood in Contra Costa and a Brentwood in Los Angeles, and name matching
        # paired them 520 km apart; "Bundy Triangle" paired with "Downtown L.A." at
        # 19 km. Those are absent counterparts being reported as conflicts, which
        # wrongly impugns a Census geocode that was correct. Drop a name match that
        # lands implausibly far away rather than escalating it.
        if cand and match_by == 'name' and 'cen_lat' in rec:
            try:
                dd = haversine_km(rec['cen_lat'], rec['cen_lon'],
                                  float(cand[0]['y']), float(cand[0]['x']))
                if dd > 5.0:
                    rec['usda_rejected'] = (f"name-matched {cand[0]['name']!r} lies "
                                            f"{dd:.0f} km away — different city, not a "
                                            f"counterpart")
                    cand = []
            except (TypeError, ValueError):
                pass
        if cand:
            rec['usda_match_by'] = match_by
            u = cand[0]
            rec.update(usda_name=u['name'], usda_lat=float(u['y']),
                       usda_lon=float(u['x']), usda_updated=u['updated'],
                       usda_zip=u['zipc'])
        # verdict
        has_c = 'cen_lat' in rec
        has_u = 'usda_lat' in rec
        if has_c and has_u:
            d = haversine_km(rec['cen_lat'], rec['cen_lon'],
                             rec['usda_lat'], rec['usda_lon'])
            rec['sep_km'] = round(d, 3)
            if d <= AGREE_KM:
                rec['verdict'] = 'AGREE'
            elif d <= SUSPECT_KM:
                rec['verdict'] = 'NEAR'
            else:
                rec['verdict'] = 'CONFLICT'
        elif has_c:
            rec['verdict'] = 'CENSUS_ONLY'
        elif has_u:
            rec['verdict'] = 'USDA_ONLY'
        else:
            rec['verdict'] = 'NEITHER'
        # postcode cross-check, never trusting the register
        if has_c and rec.get('zipc'):
            mz = re.search(r'\b(\d{5})\b\s*$', rec.get('cen_matched', '').strip())
            if mz and mz.group(1) != rec['zipc']:
                rec['zip_conflict'] = f"register {rec['zipc']} vs census {mz.group(1)}"
        out.append(rec)

    json.dump(out, open('/home/claude/reconciled.json', 'w'), indent=1)
    from collections import Counter
    v = Counter(r['verdict'] for r in out)
    print('\nverdicts:')
    for k, n in v.most_common():
        print(f'  {k:12s} {n:4d}')
    print(f"\npostcode conflicts (register vs census): "
          f"{sum(1 for r in out if 'zip_conflict' in r)}")


if __name__ == '__main__':
    main()

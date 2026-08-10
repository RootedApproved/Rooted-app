#!/usr/bin/env python3
"""
Turn reconciled markets into catalogue rows.

Only rows where two independent coordinates agree within 250 m and the CDFA register
(July 2026) confirms the market currently operates. The register says WHETHER it runs;
the two geocodes say WHERE.

Postcode is taken from the CENSUS match, never from the register, which has been wrong
in about 8% of everything checked — Orinda given a Pleasant Hill code, Pinole given a
Pittsburg code, Dublin given Alameda island, Danville given Newark.

The pin written is the Census point: it is the coordinate produced from the address the
register displays, and the USDA record's agreement corroborates it. Averaging two
sources would invent a third point that neither source asserts.
"""
import json
import re
import sys

DAYMAP = {'mon': 'Mon', 'tue': 'Tue', 'wed': 'Wed', 'thu': 'Thu', 'fri': 'Fri',
          'sat': 'Sat', 'sun': 'Sun'}


def clean(s):
    s = re.sub(r'\s+', ' ', (s or '')).strip()
    return s.replace('"', "'").replace('\\', '')


def tidy_days(d):
    d = clean(d)
    d = re.sub(r'\s*/\s*', '/', d)
    return d


def schedule(r):
    parts = []
    d, h, m = tidy_days(r['days']), clean(r['hours']), clean(r['months'])
    h = re.sub(r'\s*-\s*', '-', h).replace(' ', '')
    if d and h:
        parts.append(f'{d} {h}')
    elif d:
        parts.append(d)
    if m:
        m = re.sub(r'Year\s*-?\s*Round', 'year-round', m, flags=re.I)
        parts.append(m)
    return ', '.join(parts) or 'See operator for current hours'


def practices(r):
    bits = ['CDFA Certified Farmers\' Market, listed on the state register current to '
            'July 2026']
    mgr = clean(r.get('mgr'))
    if mgr and not re.match(r'^[\d\W]+$', mgr):
        bits.append(f'market manager {mgr}')
    bits.append('coordinates independently confirmed by two sources')
    return '; '.join(bits)


def address_for_display(r):
    a = clean(r['street'])
    a = re.sub(r'^\d{3}-\d{2}-\d{2},\s*', '', a)   # stray parcel numbers
    return a


def main():
    rows = json.load(open('/home/claude/reconciled.json'))
    agree = [r for r in rows if r['verdict'] == 'AGREE']
    src = open('Index.html', encoding='utf-8').read()

    built, skipped = [], []
    for r in agree:
        name = clean(r['name'])
        if f'listing_name:"{name}"' in src:
            skipped.append((name, 'name already in catalogue'))
            continue
        # postcode: census wins over the register
        zipc = r.get('zipc') or ''
        mz = re.search(r'\b(\d{5})\b\s*$', (r.get('cen_matched') or '').strip())
        if mz:
            zipc = mz.group(1)
        if not zipc:
            skipped.append((name, 'no postcode from either source'))
            continue
        addr = address_for_display(r)
        if not addr:
            skipped.append((name, 'no usable street address'))
            continue
        built.append(dict(
            name=name, addr=addr, city=clean(r['city']), zipc=zipc,
            lat=r['cen_lat'], lon=r['cen_lon'],
            scope='address' if re.match(r'^\s*\d', addr) else 'block',
            sched=schedule(r), prac=practices(r),
            sep=r.get('sep_km'), county=r['county'],
            zip_changed=(mz.group(1) != (r.get('zipc') or '')) if mz else False))
    # MERGE one venue listed once per trading day. The register has a row per day, so
    # Fruitvale appears three times and Alameda and Concord twice, all at one address.
    # Three pins on one spot is not three markets; it is one market and two errors. The
    # 150m duplicate gate would reject them anyway, and answering the gate by merging is
    # the correct answer rather than suppressing it.
    import math

    def near(a, b):
        dlat = math.radians(b['lat'] - a['lat'])
        dlon = math.radians(b['lon'] - a['lon'])
        h = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(a['lat']))
             * math.cos(math.radians(b['lat'])) * math.sin(dlon / 2) ** 2)
        return 2 * 6371.0088 * math.asin(math.sqrt(h)) * 1000 < 150

    def base(n):
        # A day appears in these names two ways: trailing "(Thursday)" and embedded
        # "Concord TUESDAY Farmers' Market". Stripping only the first left a merged
        # listing named for one of the several days it now covers, which is worse than
        # not merging - it asserts something false rather than merely duplicating.
        n = re.sub(r'\s*\((mon|tues|wednes|thurs|fri|satur|sun)day\)\s*$', '', n,
                   flags=re.I)
        n = re.sub(r'\s+(mon|tues|wednes|thurs|fri|satur|sun)day(s)?\s+', ' ', n,
                   flags=re.I)
        return re.sub(r'\s+', ' ', n).strip()

    groups = []
    for b in built:
        for g in groups:
            if near(g[0], b) and (base(g[0]['name']).lower() == base(b['name']).lower()
                                  or g[0]['city'] == b['city']):
                g.append(b)
                break
        else:
            groups.append([b])
    merged = []
    for g in groups:
        if len(g) == 1:
            merged.append(g[0])
            continue
        g.sort(key=lambda x: len(x['name']))
        head = dict(g[0])
        head['name'] = base(head['name'])
        ORDER = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

        def daykey(sc):
            m = re.match(r'\s*([A-Za-z]{3})', sc)
            t = (m.group(1).lower() if m else '')
            return ORDER.index(t) if t in ORDER else 99
        scheds = []
        for x in sorted(g, key=lambda x: daykey(x['sched'])):
            sc = x['sched']
            if sc not in scheds:
                scheds.append(sc)
        head['sched'] = '; '.join(scheds)
        head['merged_from'] = [x['name'] for x in g]
        merged.append(head)
    dropped = len(built) - len(merged)
    built = merged
    print(f'merged {dropped} duplicate-venue rows into their siblings')

    print(f'built {len(built)}, skipped {len(skipped)}')
    for n, why in skipped[:15]:
        print(f'   skip: {n} — {why}')
    print(f'postcodes corrected away from the register: '
          f'{sum(1 for b in built if b["zip_changed"])}')
    json.dump(built, open('/home/claude/to_insert.json', 'w'), indent=1)


if __name__ == '__main__':
    main()

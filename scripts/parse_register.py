#!/usr/bin/env python3
"""Parse the CDFA register into structured rows and diff against CURATED_LISTINGS."""
import pdfplumber, json, re, subprocess, sys

PDF = '/mnt/user-data/uploads/CurrentMrktsCounty.pdf'


def clean(c):
    if not c:
        return ''
    return re.sub(r'\s+', ' ', c.replace('\n', ' ')).strip()


rows = []
with pdfplumber.open(PDF) as pdf:
    npages = len(pdf.pages)
    for page in pdf.pages:
        t = page.extract_table()
        if not t:
            continue
        for r in t:
            if len(r) < 8:
                continue
            county = clean(r[0])
            name = clean(r[1])
            if not county or not name:
                continue
            if county.startswith('County') or name == 'Market Name':
                continue
            rows.append({
                'county': county, 'name': name, 'location': clean(r[2]),
                'manager': clean(r[3]), 'days': clean(r[4]),
                'hours': clean(r[5]), 'months': clean(r[6]), 'phone': clean(r[7]),
            })

print('pages parsed: %d' % npages)
print('rows parsed:  %d' % len(rows))

# Duplicate rows within the register itself
seen = {}
dupes = []
for r in rows:
    k = (r['county'], r['name'].lower())
    if k in seen:
        dupes.append(r['county'] + ' :: ' + r['name'])
    seen[k] = True
print('exact duplicate county+name rows in register: %d' % len(dupes))
for d in dupes:
    print('   ', d)

# Hospital-campus exclusions per the standing rule
HOSP = re.compile(r'kaiser|hospital|medical cent|medical plaza|health med|arrowhead regional'
                  r'|adventist health|city of hope|sutter (davis|roseville|faith|medical)'
                  r'|kaweah health|iehp|salinas valley health|pomona valley hospital'
                  r'|henry mayo|st\.? louise|st\.? bernardine|harbor ucla|olive view'
                  r'|lac\+usc|rancho los amigos|natividad', re.I)
hosp = [r for r in rows if HOSP.search(r['name']) or HOSP.search(r['location'])]
eligible = [r for r in rows if r not in hosp]
print('\nhospital-campus rows (excluded per rule): %d' % len(hosp))
print('eligible rows: %d' % len(eligible))

by_county = {}
for r in eligible:
    by_county[r['county']] = by_county.get(r['county'], 0) + 1

print('\neligible markets by county (desc):')
for c, n in sorted(by_county.items(), key=lambda x: -x[1]):
    print('  %-16s %3d' % (c, n))

json.dump(rows, open('/home/claude/register.json', 'w'), indent=1)
json.dump(eligible, open('/home/claude/register_eligible.json', 'w'), indent=1)
print('\nwrote register.json and register_eligible.json')

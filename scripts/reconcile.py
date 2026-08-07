#!/usr/bin/env python3
"""
Reconcile coord_verified in the live catalogue against the evidence for each one.

Exists because a fix went missing without anything reporting a failure: a run file was
discarded when a bug was fixed, but the listings in it stayed marked "worked", so every
later batch skipped them and one verified correction was never written. Counting applied
rows would not have found it. Only comparing the FILE against the EVIDENCE did.
"""
import re, json, glob, subprocess, sys

src = open('Index.html', encoding='utf-8').read()
start = src.index('const CURATED_LISTINGS = [')
block = src[start:src.index('\n];', start)]
verified = set()
for l in block.split('\n'):
    if 'coord_verified:true' in l:
        m = re.search(r'listing_name:"((?:[^"\\]|\\.)*)"', l)
        if m:
            verified.add(m.group(1))

bf = subprocess.run(['git', 'show', '60b7933:scripts/backfill_coord_schema.py'],
                    capture_output=True, text=True).stdout
bf_names = {n for n in re.findall(r'^\s+"((?:[^"\\]|\\.)*)",', bf, re.M) if n in verified}

runs = {}
for f in sorted(glob.glob('/home/claude/audit-results/run_*.json')):
    for r in json.load(open(f)):
        runs[r['name']] = r
run_ok = {n for n, r in runs.items() if r['status'] == 'OK'}

lost = run_ok - verified
print(f'verified in catalogue : {len(verified)}')
print(f'backfilled (60b7933)  : {len(bf_names)}')
print(f'OK in run evidence    : {len(run_ok)}')
print(f'\nOK in evidence but NOT written to the file: {len(lost)}')
for n in sorted(lost):
    r = runs[n]
    print(f'  {n}  ({r["km"]:.2f} km drift) — never applied')
sys.exit(1 if lost else 0)

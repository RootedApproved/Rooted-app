#!/usr/bin/env python3
"""
Verify SCHEDULES against an independent source.

Coordinates in this catalogue now carry two or three independent sources each. Opening
hours carry one: the CDFA register, transcribed once and never checked. A market moving
from 9am to 10am, or from Saturday to Sunday, produces no signal anywhere - which makes
hours the least trustworthy field on a listing that otherwise looks well verified.

Google Places publishes regularOpeningHours and businessStatus. That is a genuinely
independent record, so the register and Google can be crossed the same way two geocoders
were.

WHAT THIS DOES NOT DO
It does not overwrite. Google's hours are crowd-sourced and owner-edited, and for a
SEASONAL market they usually describe whatever season is current - a market listed
"Thu 4-8pm, June-August" will show as closed all winter, which is not a disagreement.
So this reports:

  CONFIRM   the day and times agree; the register's hours are now corroborated
  DAY_DIFF  Google trades on a day the listing does not mention, or vice versa
  TIME_DIFF same day, different times
  CLOSED    Google reports the business permanently closed
  NO_HOURS  Google has no hours for it, which is common for seasonal markets

A disagreement is a question, not a correction. Seasonal markets and multi-day merges
both produce false disagreements, and only reading them tells you which is which.
"""
import json
import re
import time
import urllib.request

KEY = None
_last = [0.0]

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
ABBR = {'mon': 'monday', 'tue': 'tuesday', 'tues': 'tuesday', 'wed': 'wednesday',
        'weds': 'wednesday', 'thu': 'thursday', 'thur': 'thursday', 'thurs': 'thursday',
        'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'}


def _throttle(gap=0.06):
    w = gap - (time.time() - _last[0])
    if w > 0:
        time.sleep(w)
    _last[0] = time.time()


def lookup(query, bias=None):
    body = {'textQuery': query, 'maxResultCount': 1}
    if bias:
        body['locationBias'] = {'circle': {
            'center': {'latitude': bias[0], 'longitude': bias[1]}, 'radius': 5000.0}}
    req = urllib.request.Request(
        'https://places.googleapis.com/v1/places:searchText',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'X-Goog-Api-Key': KEY,
                 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,'
                                     'places.businessStatus,places.regularOpeningHours,'
                                     'places.location'})
    _throttle()
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def to_minutes(h, m, ap):
    h = int(h)
    m = int(m or 0)
    if ap == 'pm' and h != 12:
        h += 12
    if ap == 'am' and h == 12:
        h = 0
    return h * 60 + m


def parse_stored(text):
    """
    Freeform listing schedule -> {day: (start_min, end_min)}.

    Handles "Sat 9am-1pm, year-round", "Tues 10am-2pm; Thur. 4-8pm, Jun - Sep",
    "Saturdays 7:30am-1pm year-round." An unclosed time like "4-8pm" takes its meridiem
    from the end of the range, which is how people write it and how the register does.
    """
    out = {}
    for seg in re.split(r'[;]', text or ''):
        s = seg.strip().lower()
        if not s:
            continue
        day = None
        for k in sorted(ABBR, key=len, reverse=True):
            if re.search(r'\b' + k, s):
                day = ABBR[k]
                break
        for d in DAYS:
            if d[:-1] in s or d in s:
                day = d
                break
        if not day:
            continue
        m = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*[-–—]\s*'
                      r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', s)
        if not m:
            out.setdefault(day, None)
            continue
        h1, m1, ap1, h2, m2, ap2 = m.groups()
        ap2 = ap2 or ap1
        ap1 = ap1 or ap2
        if not ap1 and not ap2:
            continue
        out[day] = (to_minutes(h1, m1, ap1), to_minutes(h2, m2, ap2))
    return out


def parse_google(descriptions):
    """['Saturday: 9:00 AM – 1:00 PM', 'Sunday: Closed'] -> {day: (start,end)}"""
    out = {}
    for line in descriptions or []:
        mm = re.match(r'\s*([A-Za-z]+):\s*(.+)$', line)
        if not mm:
            continue
        day = mm.group(1).lower()
        if day not in DAYS:
            continue
        body = mm.group(2)
        if 'closed' in body.lower():
            continue
        t = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)\s*[-–—]\s*'
                      r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)', body, re.I)
        if not t:
            out[day] = None
            continue
        h1, m1, ap1, h2, m2, ap2 = t.groups()
        out[day] = (to_minutes(h1, m1, ap1.lower()), to_minutes(h2, m2, ap2.lower()))
    return out


def compare(stored, google, tolerance=30):
    """Returns (verdict, detail). tolerance in minutes."""
    if not google:
        return 'NO_HOURS', 'Google publishes no hours'
    if not stored:
        return 'NO_STORED', 'the listing has no parseable schedule'
    shared = set(stored) & set(google)
    if not shared:
        return ('DAY_DIFF',
                f"listing says {', '.join(sorted(stored))}; "
                f"Google says {', '.join(sorted(google))}")
    diffs = []
    for d in sorted(shared):
        a, b = stored[d], google[d]
        if not a or not b:
            continue
        if abs(a[0] - b[0]) > tolerance or abs(a[1] - b[1]) > tolerance:
            diffs.append(f"{d}: listing {a[0]//60}:{a[0]%60:02d}-{a[1]//60}:{a[1]%60:02d}, "
                         f"Google {b[0]//60}:{b[0]%60:02d}-{b[1]//60}:{b[1]%60:02d}")
    extra_g = set(google) - set(stored)
    if diffs:
        return 'TIME_DIFF', '; '.join(diffs)
    if extra_g:
        return 'DAY_EXTRA', f"Google also lists {', '.join(sorted(extra_g))}"
    return 'CONFIRM', f"{', '.join(sorted(shared))} agree"

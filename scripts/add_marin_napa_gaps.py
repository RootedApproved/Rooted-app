#!/usr/bin/env python3
"""
Fills the four verified gaps between the CDFA register and the committed Marin/Napa
entries. Every replacement is asserted to have changed the file; a silent no-op is a
hard failure, not a warning.
"""
import sys, io

PATH = 'Index.html'
CERT = ("CERTIFIED FARMERS MARKET \\u2014 every produce seller is a CDFA-registered "
        "California grower selling what they grew themselves, verified against the "
        "state register current to 1 April 2026.")
PRODUCTS = ("Certified California-grown produce direct from the farmer, plus prepared "
            "food and local goods")
SITE = "https://www.cdfa.ca.gov/is/i_&_c/cfm.html"


def entry(name, addr, city, zipc, x, y, sched, practices):
    return ('  {_type:\'farmersmarket\',listing_name:"%s",location_address:"%s",'
            'location_city:"%s",location_state:"CA",location_zipcode:"%s",'
            'location_x:%s,location_y:%s,schedules:"%s",products:"%s",'
            'practices:"%s %s",media_website:"%s"},\n'
            % (name, addr, city, zipc, x, y, sched, PRODUCTS, practices, CERT, SITE))


MARIN = [
    entry(
        "Downtown San Rafael Summer Market",
        "4th St between A St and Lootens Pl, near Court Street Plaza",
        "San Rafael", "94901", "-122.527", "37.974",
        "One Friday evening a month, 5\\u20139pm, June through August.",
        "SEASONAL and MONTHLY, not weekly. The state register still lists this as a "
        "Thursday evening market; the Agricultural Institute of Marin relaunched it in "
        "2026 as a once-a-month Friday night market timed to the 2nd Friday Art Walk, "
        "and the operator's own listing supersedes the April register. Produce, honey "
        "and baked goods share the street with makers and street food, so this is a "
        "thinner produce market than the Civic Center pair AIM also runs \\u2014 go to "
        "Thursday or Sunday at the Civic Center if produce is the point."),
    entry(
        "Novato Hamilton Landing Farmers' Market",
        "6 Hangar Ave, between Hangar 6 and Hangar 7",
        "Novato", "94949", "-122.514", "38.058",
        "Tuesdays 10am\\u20132pm, June through November.",
        "SEASONAL, June to November. The state register lists Thursday; Marin County's "
        "own agriculture department and the market operator both list Tuesday mornings, "
        "so Tuesday is correct. Held among the restored hangars of the former Hamilton "
        "Air Force Base. This is Novato's second market and the daytime counterpart to "
        "the downtown Tuesday evening market \\u2014 same day, opposite ends of town, so "
        "the town effectively has a morning and an evening option on one day."),
    entry(
        "Strawberry Village Farmers Market",
        "800 Redwood Hwy Frontage Rd, Strawberry Village",
        "Mill Valley", "94941", "-122.515", "37.898",
        "Tuesdays 10am\\u20132:30pm year-round.",
        "The operator advertises this one as all-local and all-organic, which is worth "
        "confirming vendor by vendor: certified-market status guarantees the grower grew "
        "it, not how they grew it, so organic is a separate claim on top. Started June "
        "2023 in the frontage-road lot between West Elm and Starbucks, and run by Marin "
        "Community Farmers Markets \\u2014 the same operator as the Mill Valley Friday and "
        "Corte Madera Wednesday markets, so the three share vendors."),
]

NAPA = [
    entry(
        "Farmstead Farmers' Market",
        "738 Main St at Charter Oak Ave, Farmstead at Long Meadow Ranch",
        "St. Helena", "94574", "-122.463", "38.501",
        "Fridays 8am\\u201312pm, November through April.",
        "SEASONAL, November to April, and it exists precisely to cover the months Crane "
        "Park does not. Same market manager and largely the same vendors as the St. "
        "Helena Farmers Market, which runs May to October \\u2014 between the two, St. "
        "Helena has a Friday market every week of the year. Smaller and more intimate "
        "than Crane Park, held in the Long Meadow Ranch lot beside the Farmstead cafe, "
        "with organic produce, pastured eggs and grass-fed beef off the ranch's own "
        "Rutherford farm."),
]

src = open(PATH, encoding='utf-8').read()
original = src

ANCHORS = [
    ('listing_name:"Sausalito Certified Farmers Market"', MARIN),
    ('listing_name:"Yountville Certified Farmers\' Market"', NAPA),
]

for anchor, block in ANCHORS:
    i = src.find(anchor)
    assert i != -1, 'ANCHOR NOT FOUND: %s' % anchor
    assert src.find(anchor, i + 1) == -1, 'ANCHOR NOT UNIQUE: %s' % anchor
    end = src.find('},\n', i)
    assert end != -1, 'could not find end of anchor entry: %s' % anchor
    end += len('},\n')
    before = src
    src = src[:end] + ''.join(block) + src[end:]
    assert src != before, 'INSERT WAS A NO-OP at %s' % anchor
    assert len(src) > len(before), 'insert did not grow the file at %s' % anchor

# Hard assertions: every new listing_name must now be present exactly once.
new_names = ["Downtown San Rafael Summer Market", "Novato Hamilton Landing Farmers' Market",
             "Strawberry Village Farmers Market", "Farmstead Farmers' Market"]
for n in new_names:
    needle = 'listing_name:"%s"' % n
    c = src.count(needle)
    assert c == 1, 'EXPECTED EXACTLY 1 OCCURRENCE OF %r, GOT %d' % (n, c)
    assert original.count(needle) == 0, 'ALREADY PRESENT BEFORE EDIT: %r' % n

assert src.count("_type:'farmersmarket'") == original.count("_type:'farmersmarket'") + 4, \
    'farmersmarket count did not increase by exactly 4'

open(PATH, 'w', encoding='utf-8').write(src)
print('OK: inserted 4 entries; farmersmarket lines %d -> %d'
      % (original.count("_type:'farmersmarket'"), src.count("_type:'farmersmarket'")))

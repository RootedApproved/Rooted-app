#!/usr/bin/env python3
"""Mendocino (4), Lake (2) and San Joaquin (6). Every replacement asserted."""
PATH = 'Index.html'
CERT = ("CERTIFIED FARMERS MARKET \\u2014 every produce seller is a CDFA-registered "
        "California grower selling what they grew themselves, verified against the "
        "state register current to 1 April 2026.")
PRODUCTS = ("Certified California-grown produce direct from the farmer, plus prepared "
            "food and local goods")
SITE = "https://www.cdfa.ca.gov/is/i_&_c/cfm.html"


def e(name, addr, city, zipc, x, y, sched, prac):
    return ('  {_type:\'farmersmarket\',listing_name:"%s",location_address:"%s",'
            'location_city:"%s",location_state:"CA",location_zipcode:"%s",'
            'location_x:%s,location_y:%s,schedules:"%s",products:"%s",'
            'practices:"%s %s",media_website:"%s"},\n'
            % (name, addr, city, zipc, x, y, sched, PRODUCTS, prac, CERT, SITE))


ENTRIES = [
    e("Mendocino Certified Farmers Market", "Howard St at Main St", "Mendocino", "95460",
      "-123.797", "39.305",
      "Fridays noon\\u20132pm, May through October.",
      "SEASONAL, May to October \\u2014 some listings run it to November, so check late in "
      "the year. Two hours only, on the headland in the middle of the village, and one of "
      "seven markets run by MCFARM, a grower-run non-profit founded in 1977 as the Redwood "
      "Empire Farmers Market. That co-operative structure is the thing worth knowing here: "
      "the growers set the rules rather than a promoter renting them stalls."),
    e("Redwood Valley Farmers Market", "Redwood Valley Lions Club Park, 8920 East Rd",
      "Redwood Valley", "95470", "-123.206", "39.271",
      "Sundays 9:30am\\u201312:30pm, June to October. The 2026 season runs 7 June to 11 October.",
      "SEASONAL. 2026 is its 22nd season, which for a market of five to fifteen vendors in a "
      "valley of a few thousand people is the real signal \\u2014 it has outlasted most of the "
      "farms that started it. Run by MCFARM. The season opens with a farm-to-table fundraiser "
      "cooked from Mendocino County farms, which is how the market funds its nutrition-match "
      "programme for the year."),
    e("Laytonville Certified Farmers' Market", "Harwood Hall, 44400 Willis Ave",
      "Laytonville", "95454", "-123.483", "39.681",
      "Mondays 2:30\\u20135:30pm year-round.",
      "Year-round in a town of about a thousand people, an hour north of Ukiah on the 101 "
      "with nothing much either side \\u2014 this is the closest thing to a grocery run for "
      "growers up here. Moves indoors to the Grange hall in winter, which is why it can stay "
      "open all year. MCFARM market. One directory lists it as Tuesday; the state register "
      "and Visit Mendocino both say Monday."),
    e("Willits Certified Farmers Market",
      "Willits City Park, Humboldt & State St (May\\u2013Nov); Little Lake Grange, 291 School St (Dec\\u2013Apr)",
      "Willits", "95490", "-123.353", "39.413",
      "Thursdays 3\\u20135:30pm year-round.",
      "Year-round, but it MOVES \\u2014 outdoors at the city park from May to November, indoors "
      "at the Little Lake Grange from December to April. The state register lists only the "
      "summer corner, so anyone using the register in January would find an empty park. Ten "
      "to fifteen vendors, run by MCFARM and managed by Michael Foley, who farms and has "
      "written on small-farm economics."),
    e("Tuesday Market at Library Park", "Library Park, Park St between 2nd and 3rd Sts",
      "Lakeport", "95453", "-122.914", "39.043",
      "Tuesdays 10am\\u20131pm, May through September. Rain or shine.",
      "SEASONAL, May to September, on the Clear Lake shore in downtown Lakeport. Run by Lake "
      "County Farmers' Finest, the same operator as the year-round Saturday market at the "
      "Mercantile already on this map \\u2014 between the two, Lake County growers have a "
      "midweek and a weekend outlet without leaving the lake."),
    e("Clearlake Certified Farmers Market", "Austin Park, 14077 Lakeshore Dr at Division",
      "Clearlake", "95422", "-122.648", "38.960",
      "Saturdays 10am\\u20131pm and Wednesday evenings 4:30\\u20137:30pm, April through October.",
      "SEASONAL, April to October, in the lakefront park. Twice a week with a morning and an "
      "evening slot, which is unusual for a market this size and suggests it is serving "
      "shoppers who work. Details here come from the state register only \\u2014 unlike the "
      "rest of this batch, no current operator page was found to confirm the split hours, so "
      "ring ahead before making a trip for the Wednesday session."),
    e("Lodi Certified Farmers Market", "35 S School St, between Oak St and Pine St",
      "Lodi", "95240", "-121.274", "38.133",
      "Thursdays 5\\u20138pm, mid-May to late August.",
      "SEASONAL and short \\u2014 about fifteen Thursdays, ending in August, so it is running "
      "now and will not be by September. An evening street-fair format through downtown Lodi "
      "with music and craft stalls alongside the growers. Note the state register gives 15 May "
      "to 28 August, but both dates fall on a Friday in 2026; the operator's Thursday-aligned "
      "dates are the ones to trust."),
    e("Downtown Tracy Farmers Market", "Central Ave between 6th St and 9th St",
      "Tracy", "95376", "-121.426", "37.737",
      "Saturdays 8am\\u20131pm year-round.",
      "Year-round and outdoors through the Central Valley winter, which is a fair test of a "
      "market. Run by San Joaquin Certified Farmers Markets, the county's main operator. This "
      "is the one to use if you are crossing the Altamont \\u2014 it is the closest year-round "
      "certified market to the Bay Area on the I-580 corridor."),
    e("Mountain House Certified Farmers Market", "251 E Main St at Central Pkwy",
      "Mountain House", "95391", "-121.540", "37.779",
      "Sundays 9am\\u20131pm year-round.",
      "Year-round. Mountain House is a planned community built from nothing in the late 1990s "
      "and incorporated only in 2024, so a weekly certified market here is newer than most of "
      "the housing around it. Worth knowing if you are in the Tri-Valley: it is closer than "
      "Tracy or Stockton coming from the west."),
    e("Weberstown Farmers Market", "4950 Pacific Ave, at March Ln, by Weberstown Mall",
      "Stockton", "95207", "-121.312", "37.995",
      "Sundays 8am\\u20131pm year-round; Thursdays 8am\\u20131pm, May through November.",
      "The Sunday market runs all year; the Thursday one is SEASONAL, May to November. The "
      "state register lists both as year-round, which would send someone to an empty car park "
      "on a Thursday in February. Stockton's main market, run by San Joaquin Certified Farmers "
      "Markets, in the mall car park off March Lane."),
    e("Golden Villa Farmers Market", "255 S Sutter St at Washington St",
      "Stockton", "95203", "-121.286", "37.951",
      "Saturdays 5am\\u201311am year-round.",
      "Opens at FIVE IN THE MORNING and is finished by eleven \\u2014 not a leisurely weekend "
      "market but a genuine early-morning produce market, and the earliest opening of any "
      "market on this map. Year-round, in south Stockton. Come at six for the selection; by "
      "ten it is winding down."),
    e("Manteca Farmers Market", "1000 Lifestyle St, Promenade Shops at Orchard Valley",
      "Manteca", "95337", "-121.229", "37.781",
      "Saturdays 9am\\u20131pm, June through September.",
      "SEASONAL and the shortest run in the county \\u2014 four months, summer only, which "
      "tracks the Central Valley stone-fruit season it exists to sell. Run by San Joaquin "
      "Certified Farmers Markets at the Promenade Shops. Peaches, nectarines and melons are "
      "the point here; go in July or August or do not bother."),
]

src = open(PATH, encoding='utf-8').read()
original = src

anchor = 'listing_name:"Ukiah Certified Farmers\' Market"'
i = src.find(anchor)
assert i != -1, 'ANCHOR NOT FOUND: %s' % anchor
assert src.find(anchor, i + 1) == -1, 'ANCHOR NOT UNIQUE'
end = src.find('},\n', i)
assert end != -1, 'no end of anchor entry'
end += 3
src = src[:end] + ''.join(ENTRIES) + src[end:]
assert src != original, 'INSERT WAS A NO-OP'

names = ["Mendocino Certified Farmers Market", "Redwood Valley Farmers Market",
         "Laytonville Certified Farmers' Market", "Willits Certified Farmers Market",
         "Tuesday Market at Library Park", "Clearlake Certified Farmers Market",
         "Lodi Certified Farmers Market", "Downtown Tracy Farmers Market",
         "Mountain House Certified Farmers Market", "Weberstown Farmers Market",
         "Golden Villa Farmers Market", "Manteca Farmers Market"]
for n in names:
    needle = 'listing_name:"%s"' % n
    assert original.count(needle) == 0, 'ALREADY PRESENT: %r' % n
    assert src.count(needle) == 1, 'EXPECTED 1 OF %r, GOT %d' % (n, src.count(needle))

assert src.count("_type:'farmersmarket'") == original.count("_type:'farmersmarket'") + 12, \
    'farmersmarket count did not rise by exactly 12'

open(PATH, 'w', encoding='utf-8').write(src)
print('OK: farmersmarket %d -> %d'
      % (original.count("_type:'farmersmarket'"), src.count("_type:'farmersmarket'")))

// Integrity checks over CURATED_LISTINGS / LOCAL_FOOD_TYPES / products in Index.html.
// Exits non-zero on any failure. No output is decorative — every line is a gate.
const fs = require('fs');
const src = fs.readFileSync(__dirname + '/../Index.html', 'utf8');

function extractArray(name) {
  const start = src.indexOf('const ' + name + ' = [');
  if (start === -1) throw new Error('cannot find ' + name);
  const open = src.indexOf('[', start);
  let depth = 0, inStr = null, esc = false;
  for (let i = open; i < src.length; i++) {
    const c = src[i];
    if (inStr) {
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === '[') depth++;
    else if (c === ']') { depth--; if (depth === 0) return src.slice(open, i + 1); }
  }
  throw new Error('unterminated ' + name);
}

function extractObject(name) {
  const start = src.indexOf('const ' + name + ' = {');
  if (start === -1) throw new Error('cannot find ' + name);
  const open = src.indexOf('{', start);
  let depth = 0, inStr = null, esc = false;
  for (let i = open; i < src.length; i++) {
    const c = src[i];
    if (inStr) {
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) return src.slice(open, i + 1); }
  }
  throw new Error('unterminated ' + name);
}

const listings = eval(extractArray('CURATED_LISTINGS'));
const types = eval('(' + extractObject('LOCAL_FOOD_TYPES') + ')');

const fail = [];
const warn = [];

// 1. Listing count
console.log('listings: ' + listings.length);
const byType = {};
listings.forEach(l => { byType[l._type] = (byType[l._type] || 0) + 1; });
Object.keys(byType).sort().forEach(t => console.log('  ' + t + ': ' + byType[t]));

// 2. Duplicate names (name+city, since chain stores legitimately repeat names)
const seen = new Map();
listings.forEach((l, i) => {
  const key = (l.listing_name || '').trim().toLowerCase() + '|' + (l.location_city || '').trim().toLowerCase();
  if (seen.has(key)) fail.push('DUPLICATE name+city: "' + l.listing_name + '" in ' + l.location_city + ' (idx ' + seen.get(key) + ' and ' + i + ')');
  else seen.set(key, i);
});

// 2b. Near-duplicate detection by TOKEN OVERLAP, not substring.
//     The substring version missed the real-world case: the CDFA register calls a market
//     "Silver Lake Certified Farmers' Market Sat" while the map calls it "Silver Lake
//     Farmers Market". Neither contains the other, so a substring test passes them both
//     through as distinct pins at identical coordinates. Jaccard overlap on meaningful
//     tokens catches it. 26 committed LA entries have register counterparts under a
//     different name; this is the gate that stops them being added twice.
const NAME_STOP = new Set(['certified', 'farmers', 'farmer', 'farmers\u2019', 'market',
  'markets', 'cfm', 'the', 'of', 'at', 'a', 'and', 'inc', 'llc', 'community', 'downtown']);
// Two real collisions slipped a plain token match and both are cheap to close:
//   "Social District" vs "Social Districts"  -> plural only, 33% raw
//   "LA City Hall"    vs "Los Angeles City Hall" -> abbreviation, 40% raw
// Singularise, and expand the handful of abbreviations that actually appear in place names.
const NAME_ALIAS = { la: 'losangeles', 'los angeles': 'losangeles', sf: 'sanfrancisco',
  st: 'saint', mt: 'mount', ft: 'fort', n: 'north', s: 'south', e: 'east', w: 'west' };
function singular(t) {
  if (t.length > 3 && t.endsWith('ies')) return t.slice(0, -3) + 'y';
  if (t.length > 3 && t.endsWith('es') && !t.endsWith('ses')) return t.slice(0, -2);
  if (t.length > 3 && t.endsWith('s') && !t.endsWith('ss')) return t.slice(0, -1);
  return t;
}
function nameTokens(s) {
  let str = String(s || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ');
  str = str.replace(/\blos angeles\b/g, 'losangeles').replace(/\bsan francisco\b/g, 'sanfrancisco');
  const out = new Set();
  str.split(/\s+/).forEach(t => {
    if (!t) return;
    t = NAME_ALIAS[t] || t;
    t = singular(t);
    if (!NAME_STOP.has(t)) out.add(t);
  });
  return out;
}
function jaccard(a, b) {
  if (!a.size || !b.size) return 0;
  let inter = 0;
  a.forEach(t => { if (b.has(t)) inter++; });
  return inter / (a.size + b.size - inter);
}
// ~1 mile in degrees at California latitudes
const NEAR_DEG = 0.015;
// Scope: chain grocery and restaurants legitimately cluster — three Trader Joe's inside a
// mile of each other in San Francisco are three real shops, and they disambiguate by a
// parenthetical suffix rather than by name. Running token overlap over them produced 20
// false positives and zero true ones. The types below are the ones where two pins at the
// same corner means an actual mistake, and they are the types being bulk-imported.
const DEDUP_TYPES = new Set(['farmersmarket', 'csa', 'onfarmmarket', 'meat']);
for (let i = 0; i < listings.length; i++) {
  for (let j = i + 1; j < listings.length; j++) {
    const a = listings[i], b = listings[j];
    if (a._type !== b._type) continue;
    if (!DEDUP_TYPES.has(a._type)) continue;
    if (typeof a.location_x !== 'number' || typeof b.location_x !== 'number') continue;
    const dx = Math.abs(a.location_x - b.location_x), dy = Math.abs(a.location_y - b.location_y);
    if (dx > NEAR_DEG || dy > NEAR_DEG) continue;
    const sim = jaccard(nameTokens(a.listing_name), nameTokens(b.listing_name));
    if (sim >= 0.5) {
      fail.push('NEAR-DUPLICATE (' + Math.round(sim * 100) + '% name overlap, <1mi): "'
        + a.listing_name + '" (' + a.location_city + ') vs "'
        + b.listing_name + '" (' + b.location_city + ')');
    }
    // Name matching alone has false NEGATIVES and one bit us: the map's "Larchmont Village
    // Farmers Market" and the register's "Larchmont Sunday CFM" are the same car park at
    // 209 N Larchmont Blvd, but share only one meaningful token and score 33%. So also flag
    // ANY two same-type listings within ~150m regardless of name. Two genuinely different
    // farmers markets that close together are rare enough to be worth a human look, and a
    // silent duplicate pin is worse than a false alarm.
    const SAME_SPOT = 0.0015;
    if (dx < SAME_SPOT && dy < SAME_SPOT && sim < 0.5) {
      fail.push('SAME-LOCATION, different names (<150m) \u2014 check for a duplicate: "'
        + a.listing_name + '" vs "' + b.listing_name + '" (' + a.location_city + ')');
    }
  }
}

// 3. Coordinates present, numeric, and inside a sane California-plus bounding box
listings.forEach(l => {
  const n = l.listing_name || '(unnamed)';
  if (typeof l.location_x !== 'number' || typeof l.location_y !== 'number' || isNaN(l.location_x) || isNaN(l.location_y)) {
    fail.push('MISSING/NON-NUMERIC coords: ' + n);
    return;
  }
  if (l.location_x > 0) fail.push('POSITIVE longitude (sign flip?): ' + n + ' x=' + l.location_x);
  if (l.location_state === 'CA' && (l.location_y < 32.4 || l.location_y > 42.1 || l.location_x < -124.5 || l.location_x > -114.1)) {
    fail.push('COORDS OUTSIDE CALIFORNIA: ' + n + ' (' + l.location_y + ', ' + l.location_x + ')');
  }
});

// 4. Every _type has LOCAL_FOOD_TYPES meta
const usedTypes = new Set(listings.map(l => l._type));
usedTypes.forEach(t => {
  if (!types[t]) fail.push('_type with no LOCAL_FOOD_TYPES entry: ' + t);
  else if (!types[t].label || !types[t].icon || !types[t].color) fail.push('LOCAL_FOOD_TYPES entry incomplete: ' + t);
});
Object.keys(types).forEach(t => { if (!usedTypes.has(t)) warn.push('LOCAL_FOOD_TYPES declares "' + t + '" but no listing uses it'); });

// 5. Required fields
listings.forEach(l => {
  const n = l.listing_name || '(unnamed)';
  ['listing_name', 'location_city', 'location_state', '_type'].forEach(f => {
    if (!l[f] || !String(l[f]).trim()) fail.push('EMPTY required field "' + f + '": ' + n);
  });
  if (l._type === 'farmersmarket' && !l.schedules) fail.push('farmersmarket with no schedules: ' + n);
});

// 6. Orphaned products + broken alts
// PRODUCTS is an object keyed by product id, not an array of {id:...} records.
const products = eval('(' + extractObject('PRODUCTS') + ')');
const prodIds = new Set(Object.keys(products));
if (prodIds.size === 0) { console.log('FATAL: parsed zero products'); process.exit(1); }

// Subcategories referenced by products must exist in the nav; products must belong to one.
const subcatRefs = new Set();
Object.entries(products).forEach(([id, p]) => {
  if (!p.subcat) fail.push('ORPHANED product (no subcat): ' + id);
  else subcatRefs.add(p.subcat);
  if (!p.brand || !p.name) fail.push('product missing brand/name: ' + id);
});

let altCount = 0;
Object.entries(products).forEach(([id, p]) => {
  if (!Array.isArray(p.alts)) {
    if (p.alts !== undefined && p.alts !== null) fail.push('alts is not an array: ' + id);
    return;
  }
  p.alts.forEach(ref => {
    altCount++;
    if (!prodIds.has(ref)) fail.push('BROKEN alt reference in ' + id + ' -> ' + ref);
    if (ref === id) fail.push('SELF-REFERENTIAL alt: ' + id);
  });
});
console.log('products: ' + prodIds.size + ' | subcats referenced: ' + subcatRefs.size + ' | alt refs checked: ' + altCount);
if (altCount === 0) { console.log('FATAL: zero alt refs checked, parser is not seeing alts'); process.exit(1); }

warn.forEach(w => console.log('WARN: ' + w));

if (fail.length) {
  console.log('\nFAILURES (' + fail.length + '):');
  fail.forEach(f => console.log('  ' + f));
  process.exit(1);
}
console.log('\nNODE CHECKS PASSED');

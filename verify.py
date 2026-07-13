#!/usr/bin/env python3
"""
Pre-push verification for ROOTED's Index.html.
Run this after every edit, before committing. Catches:
  1. JS syntax errors
  2. Any getElementById() call in the JS whose target id doesn't actually exist in the HTML
  3. Runtime errors when calling core nav functions (showSubcat for every subcat, showGolfHub, etc.)
"""
import re, subprocess, sys
from bs4 import BeautifulSoup

path = sys.argv[1] if len(sys.argv) > 1 else "Index.html"

with open(path) as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
real_ids = set(el.get("id") for el in soup.find_all(id=True))

script_match = re.search(r"<script>([\s\S]*?)</script>", html)
code = script_match.group(1)

# 1. Every literal getElementById('...') target must exist in the HTML
referenced = set(re.findall(r"getElementById\(['\"]([\w-]+)['\"]\)", code))
missing = referenced - real_ids
if missing:
    print("FAIL: JS references ids that do NOT exist in HTML:", missing)
    sys.exit(1)
else:
    print(f"OK: all {len(referenced)} literal getElementById() targets exist in HTML")

# 2. Syntax check (write to temp file — the code string is now too large for a CLI arg)
with open("/tmp/_verify_syntax_check.js", "w") as f:
    f.write("new Function(" + repr(code) + ");")
try:
    subprocess.run(["node", "/tmp/_verify_syntax_check.js"], check=True, capture_output=True)
    print("OK: JS syntax valid")
except subprocess.CalledProcessError as e:
    print("FAIL: JS syntax error:", e.stderr.decode())
    sys.exit(1)

# 3. Extract all subcat ids referenced in PRODUCTS/SUBCAT_EDU and call showSubcat for each
subcats = set(re.findall(r"subcat:'([\w-]+)'", code))
node_script = f"""
const elements = {{}};
function makeEl(id) {{
  if (!elements[id]) elements[id] = {{ id, innerHTML:'', textContent:'', style:{{}}, dataset:{{}}, className:'',
    classList:{{add(){{}},remove(){{}},contains(){{return false;}}}}, querySelectorAll: () => [], appendChild(){{}}, onclick:null }};
  return elements[id];
}}
const realIds = new Set({sorted(real_ids)!r});
global.window = {{ addEventListener: () => {{}}, scrollTo: () => {{}} }};
global.document = {{ getElementById: (id) => realIds.has(id) ? makeEl(id) : null, querySelectorAll: () => [], addEventListener: () => {{}} }};
global.localStorage = {{ getItem: () => null, setItem: () => {{}} }};
eval({code!r});
let failed = false;
for (const sub of {sorted(subcats)!r}) {{
  try {{ showSubcat(sub); }} catch(e) {{ console.log('FAIL: showSubcat(' + sub + ') threw:', e.message); failed = true; }}
}}
try {{ showGolfHub(); }} catch(e) {{ console.log('FAIL: showGolfHub threw:', e.message); failed = true; }}
if (!failed) console.log('OK: all ' + {len(subcats)} + ' subcats + hub navigation execute without error');
process.exit(failed ? 1 : 0);
"""
with open("/tmp/_verify_nav_check.js", "w") as f:
    f.write(node_script)
result = subprocess.run(["node", "/tmp/_verify_nav_check.js"], capture_output=True, text=True)
print(result.stdout.strip())
if result.returncode != 0:
    print(result.stderr)
    sys.exit(1)

print("\nALL CHECKS PASSED")

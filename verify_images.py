#!/usr/bin/env python3
"""
verify_images.py — MANDATORY pre-push check, same discipline as verify.py.

Run this BEFORE every push that touches Index.html's PRODUCTS object. It exists
because on 2026-07-21 we discovered 21 fabricated (never-verified, guessed) image
URLs sitting in the product data, silently blocking the real live-fetch system for
weeks. This script is the permanent fix for that ever happening silently again.

RULE GOING FORWARD: no product's `img:` field may be added or edited without first
confirming the URL via a real fetch (web_fetch the product page, confirm the exact
og:image or Shopify .json image URL exists) - the same discipline already used for
every other factual claim on this site. This script is a safety net that catches the
most common fabrication signatures automatically, not a replacement for that discipline.

Usage: python3 verify_images.py
Exits non-zero (and prints details) if anything looks fabricated.
"""
import re
import sys

FLAGGED_PATTERNS = [
    (r'\?width=\d+(&|$)', 'generic "?width=NNN" resize param — a strong signature of a guessed URL, since real CDN links from Shopify/Bynder/etc. almost never use a bare width param with no version hash'),
]

def main():
    with open('Index.html', 'r') as f:
        content = f.read()

    start = content.index("const PRODUCTS = {")
    end = content.index('const CURATED_LISTINGS')
    block = content[start:end]

    entries = re.findall(r"'([\w-]+)':\{brand:'([^']*)'.*?url:'([^']*)'.*?img:'([^']*)'", block)

    problems = []
    seen_version_numbers = {}

    for eid, brand, url, img in entries:
        for pattern, reason in FLAGGED_PATTERNS:
            if re.search(pattern, img):
                problems.append((eid, brand, img, reason))

        # A specific real-world signature we've already seen once: the exact same
        # fake "?v=NNNNNNNNNN" version number reused across multiple different
        # products/brands is not physically possible for a real CDN - each real
        # upload gets its own unique version/timestamp.
        m = re.search(r'[?&]v=(\d{8,})', img)
        if m:
            v = m.group(1)
            seen_version_numbers.setdefault(v, []).append((eid, brand))

    for v, ids in seen_version_numbers.items():
        if len(ids) > 1:
            problems.append((None, None, None,
                f'SAME version number "{v}" reused across {len(ids)} different products - '
                f'physically impossible for real CDN uploads, near-certain fabrication: {ids}'))

    if problems:
        print(f"FAIL: {len(problems)} product image(s) look fabricated or unverified.\n")
        for eid, brand, img, reason in problems:
            if eid:
                print(f"  - {eid} ({brand}): {img}")
            print(f"    -> {reason}")
        print("\nDo not push until each of these is either removed (let the live-fetch")
        print("system find the real image) or replaced with a URL you have personally")
        print("confirmed via a real fetch of the product's actual page.")
        sys.exit(1)
    else:
        print(f"OK: checked {len(entries)} product image override(s), none look fabricated.")
        sys.exit(0)

if __name__ == '__main__':
    main()

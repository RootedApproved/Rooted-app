#!/usr/bin/env python3
"""
verify_images.py — MANDATORY pre-push check, same discipline as verify.py.

Run this BEFORE every push that touches Index.html's PRODUCTS object. It exists
because on 2026-07-21 we discovered 21 fabricated (never-verified, guessed) image
URLs sitting in the product data, silently blocking the real live-fetch system for
weeks, PLUS a second, separate bug class: several products' `url` field pointed at
a generic category/collection page instead of a specific product page — meaning the
buy link was wrong AND the live-fetch system could never find a real per-product
image, since there isn't one to find on a collection page.

RULES GOING FORWARD:
1. No product's `img:` field may be added or edited without first confirming the
   URL via a real fetch (web_fetch the product page, confirm the exact og:image or
   Shopify .json image URL exists) - the same discipline already used for every
   other factual claim on this site.
2. No product's `url:` field may point at a category/collection/listing page. It
   must be the specific product's own page. Before adding a new product, run:
       python3 check_product_image.py <candidate-url>
   which will flag a category-page URL immediately and tell you whether a real
   image was found, before you ever add it to PRODUCTS.
3. If a brand's own site is bot-protected (Peter Millar, Brooks Brothers, and others
   sit behind Incapsula/similar), check RESELLERS.md for a known working reseller
   for that brand before spending time rediscovering one.

This script is a safety net that catches the most common fabrication/category-page
signatures automatically, not a replacement for that discipline.

Usage: python3 verify_images.py
Exits non-zero (and prints details) if anything looks fabricated or mis-linked.
"""
import re
import sys

FLAGGED_IMG_PATTERNS = [
    (r'\?width=\d+(&|$)', 'generic "?width=NNN" resize param — a strong signature of a guessed URL, since real CDN links from Shopify/Bynder/etc. almost never use a bare width param with no version hash'),
]

# Signals that a `url:` field is a category/collection/listing page rather than a
# specific product page. Any one of these patterns is a strong signal, not a
# guarantee — always eyeball a flagged URL before deciding what to do with it.
CATEGORY_PAGE_URL_PATTERNS = [
    r'/c/[\w-]+/?(\?|$)',                          # generic /c/category style
    r'/collections/[\w-]+/?(\?|$)',                # Shopify collection page with nothing after it
    r'/(mens|womens|men|women)/[\w-]+/?(\?|$)',    # e.g. brooksbrothers.com/mens/sport-coats
    r'/b/[\w-]+-for-men/[\w-]+/bn_\d+',            # eBay category-browse page
    r'/f/(fit|material)=',                          # menswearhouse.com filtered listing page
]


def check_fabricated_images(block):
    entries = re.findall(r"'([\w-]+)':\{brand:'([^']*)'.*?url:'([^']*)'.*?img:'([^']*)'", block)
    problems = []
    seen_version_numbers = {}

    for eid, brand, url, img in entries:
        for pattern, reason in FLAGGED_IMG_PATTERNS:
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

    return entries, problems


def check_category_page_urls(block):
    all_entries = re.findall(r"'([\w-]+)':\{brand:'([^']*)'.*?url:'([^']*)'", block)
    problems = []
    for eid, brand, url in all_entries:
        for pattern in CATEGORY_PAGE_URL_PATTERNS:
            if re.search(pattern, url):
                problems.append((eid, brand, url))
                break
    return all_entries, problems


def main():
    with open('Index.html', 'r') as f:
        content = f.read()

    start = content.index("const PRODUCTS = {")
    end = content.index('const CURATED_LISTINGS')
    block = content[start:end]

    img_entries, img_problems = check_fabricated_images(block)
    url_entries, url_problems = check_category_page_urls(block)

    exit_code = 0

    if img_problems:
        exit_code = 1
        print(f"FAIL: {len(img_problems)} product image(s) look fabricated or unverified.\n")
        for eid, brand, img, reason in img_problems:
            if eid:
                print(f"  - {eid} ({brand}): {img}")
            print(f"    -> {reason}")
        print("\nDo not push until each of these is either removed (let the live-fetch")
        print("system find the real image) or replaced with a URL you have personally")
        print("confirmed via a real fetch of the product's actual page.\n")
    else:
        print(f"OK: checked {len(img_entries)} product image override(s), none look fabricated.")

    if url_problems:
        exit_code = 1
        print(f"\nFAIL: {len(url_problems)} product url(s) look like category/collection pages, not specific product pages.\n")
        for eid, brand, url in url_problems:
            print(f"  - {eid} ({brand}): {url}")
        print("\nThese need the specific product page URL instead. A category-page URL means")
        print("both the buy link is wrong AND the live-fetch system can never find a real")
        print("per-product image (there isn't one to find on a collection page).\n")
    else:
        print(f"OK: checked {len(url_entries)} product url(s), none look like category/collection pages.")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()

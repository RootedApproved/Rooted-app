#!/usr/bin/env python3
"""
check_product_image.py — run this BEFORE adding any new product to PRODUCTS.

This exists so the mistakes fixed on 2026-07-21 (category-page URLs, fabricated
image URLs, bot-protected sites silently failing) get caught at the moment a new
product is being considered, not weeks later in a big retroactive audit.

USAGE:
    python3 check_product_image.py <candidate-product-url>

This script cannot fetch the URL directly (no network access from this sandbox),
so it does two things instead:

1. Pattern-checks the URL itself and tells you immediately if it looks like a
   category/collection/listing page rather than a specific product page — the
   single most common mistake found in the 2026-07-21 audit.

2. Prints a short checklist to walk through manually (via Claude's web_fetch or
   your own browser) before adding the product, so the same discipline that was
   applied retroactively gets applied up front instead.

It is NOT a substitute for actually fetching the page and confirming the image.
It is a fast first filter to catch the obvious mistake before any time is spent
on the rest of the checklist.
"""
import re
import sys

CATEGORY_PAGE_URL_PATTERNS = [
    (r'/c/[\w-]+/?(\?|$)', 'generic /c/category-style path'),
    (r'/collections/[\w-]+/?(\?|$)', 'Shopify collection page with nothing after the slug'),
    (r'/(mens|womens|men|women)/[\w-]+/?(\?|$)', 'brand.com/mens/category-name style listing page'),
    (r'/b/[\w-]+-for-men/[\w-]+/bn_\d+', 'eBay category-browse page (not a single listing)'),
    (r'/f/(fit|material)=', 'filtered listing page (e.g. menswearhouse.com /f/material=...)'),
]

KNOWN_BOT_PROTECTED_DOMAINS = [
    'brooksbrothers.com',
    'petermillar.com',
]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    problems = []

    for pattern, reason in CATEGORY_PAGE_URL_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            problems.append(reason)

    for domain in KNOWN_BOT_PROTECTED_DOMAINS:
        if domain in url:
            print(f"NOTE: {domain} is a known bot-protected site (confirmed 2026-07-21).")
            print("Check RESELLERS.md for a known-working reseller for this brand")
            print("before spending time trying to fetch this domain directly.\n")

    if problems:
        print(f"STOP: this URL looks like a category/collection/listing page, not a")
        print(f"specific product page:\n")
        for reason in problems:
            print(f"  - {reason}")
        print(f"\nFind the specific product's own page instead. A category-page URL")
        print(f"means both the buy link will be wrong AND the live-fetch image system")
        print(f"will never find a real image (there isn't one to find on a listing page).")
        sys.exit(1)

    print("OK: URL pattern looks like a specific product page, not a category page.")
    print("\nBefore adding this product to PRODUCTS, still manually confirm:")
    print("  1. Fetch the page. Does it load a single specific product (not 'sold out'")
    print("     with no image, not a redirect to a category page)?")
    print("  2. Does it have a real og:image or Shopify .json image URL you can see")
    print("     directly in the fetched content? (Not one you have to guess/construct")
    print("     from a filename pattern seen elsewhere.)")
    print("  3. Does the composition/price/details on the page match what you're about")
    print("     to write in the product entry?")
    print("  4. If you found the image via a reseller rather than the brand's own site,")
    print("     note that in the git commit message, same as every fix in the 2026-07-21")
    print("     audit did.")
    sys.exit(0)


if __name__ == '__main__':
    main()

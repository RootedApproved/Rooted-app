# Known bot-protected brands and working resellers

Built during the 2026-07-21 image audit. When a brand's own site blocks direct
fetching (Incapsula or similar WAF), check here before spending time
rediscovering a workaround.

Run `python3 check_product_image.py <url>` first — it flags known
bot-protected domains automatically.

| Brand | Own site status | Known working reseller(s) |
|---|---|---|
| Peter Millar | Bot-protected (Incapsula, confirmed 2026-07-21) | Saint Bernard (saintbernard.com), Giovanni's Fine Fashions, Neiman Marcus |
| Brooks Brothers | Own product pages inconsistent — many URLs that look like single products are actually category/collection pages | Macy's (carries genuine Brooks Brothers, not just the "B by Brooks Brothers" diffusion line — check the listing says "Brooks Brothers", not "B by Brooks Brothers", if fiber purity matters) |
| Patagonia, Faherty | — | Saint Bernard (saintbernard.com) |
| Champion, Van Heusen, Kenneth Cole, Kenneth Cole Reaction | — | Macy's |
| Demeyere | Own site (demeyere.us) mostly collection pages, thin on single-product pages | Zwilling (zwilling.com, Demeyere's parent company) — real per-SKU product pages with Scene7/Demandware image CDN |

## Not Perfect Linen: a third failure mode (SKU rotation, not bot-protection)

Confirmed 2026-07-21 (second pass). Not Perfect Linen isn't bot-protected and isn't
using category-page URLs by mistake — but it silently breaks anyway. This brand's
Shopify store frequently re-lists the *same* product design under a new numbered
slug (e.g. `mens-linen-shirts-long-sleeve-montreal` → `men-s-long-sleeve-linen-shirt-montreal-2`
→ `-3`, etc.) as old batches sell through. The old slug doesn't 404 — it silently
redirects to a generic collection page, so a stored URL can look fine for months
and then start returning the wrong (collection banner) image with no error.

**What this means in practice:** for this brand specifically, a URL that worked
when first added can go stale later even with no changes on our end. If an NPL
product's image starts failing:
1. Search `notperfectlinen.com "<product name>"` — multiple numbered variants of
   the same listing usually show up in results.
2. Fetch each candidate with `text_content_token_limit` set low (~150-300) to
   avoid the enormous country-flag-dropdown boilerplate this site includes on
   every page — the real content (og:image, price, description) appears at the
   very top of the fetch regardless.
3. Confirm the canonical in the fetched frontmatter matches the URL you fetched
   (if it doesn't, you've been redirected to a stale slug — try the next
   candidate).
4. A live product page's "Complete the look" section often links to another
   NPL product's *current* live slug — useful for chaining fixes across
   multiple products from a single fetch, as happened when Montreal's page led
   directly to Darwin's live slug.

## Notes on Macy's specifically

Macy's carries both a brand's genuine line and, for some brands, a
Macy's-exclusive diffusion line with a similar name (e.g. "Brooks Brothers"
vs. "B by Brooks Brothers"). These can differ in composition (e.g. wool vs.
wool-blend), so always check the listing title and materials section — don't
assume the diffusion line matches the genuine brand's fiber content.

Macy's product images use the Scene7 dynamic imaging CDN
(`slimages.macysassets.com`) and are usually served as `.tif` by default.
Append `?fmt=jpeg&wid=800` (or similar) to get a browser-compatible JPEG
instead of forcing a TIFF conversion client-side.

## Adding a new reseller to this list

If you find a new bot-protected brand during future product research, add a
row here once you've confirmed a reseller works — this list is the whole
point of not re-solving the same problem twice.

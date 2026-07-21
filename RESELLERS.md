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

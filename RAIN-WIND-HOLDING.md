# Rain & Wind Layers — Held for a Future Category

Removed from Golf Apparel entirely (2026-07-27) — determined not to be golf
attire. Data is fully verified and intact in the PRODUCTS object with
`subcat:'unassigned'`, invisible everywhere on the live site (nav, search,
chat assistant, recommendations) until reassigned to a real category.

## The four products

1. **Patagonia Lightweight Waxed Cotton Jacket** — id `golf-outerwear-patagonia`
   100% organic cotton ripstop, plant-based wax finish, PFAS-free. $183.99.

2. **Duckworth Snowcrest Shirt Jacket** — id `golf-outerwear-snowcrest`
   100% Montana Merino wool, 22oz/710gsm, made in USA. $599. Restocks ~once
   a year, frequently sold out.

3. **Alpkit Ranger Organic Ventile Jacket** — id `golf-rainwind-alpkit`
   100% organic cotton Ventile, both outer and liner layers, GOTS certified,
   PFC-free DWR. $239.99 (marked down from $459.99, was on pre-order —
   reconfirm stock/price before reactivating).

4. **Private White V.C. Jack's Mac** — id `golf-rainwind-pwvc`
   Twin-layer 100% cotton Ventile, genuinely fully waterproof, all-copper
   hardware. $1,250.

## To bring any of these back

Change `subcat:'unassigned'` to the target subcat id on the relevant
product(s), then update that category's nav card count and `SUBCAT_EDU`
`desc`/`backTitle` fields to match. Re-verify price and stock status first —
none of these have been checked since 2026-07-27.

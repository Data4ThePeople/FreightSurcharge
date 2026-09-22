# Status

Project: FreightSurcharge
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1
Since: 2026-09-22

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | | |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-09-22 Step 1 opened. Topic: fuel surcharges in truckload, LTL and rail freight, how they track EIA diesel, and how much a diesel spike raises freight bills and consumer prices.
- 2026-09-22 Work moved in from an exploratory session: FRED PPI and diesel pulls, 10-K fuel surcharge extraction (202 rows, quotes verified), BEA input-output pass-through layers, and the "Diesel to Surcharge" calculator (dist/index.html).
- 2026-09-22 Moved from the desktop app to PyCharm. DATASETS.md written; it audits the step 1 work and lists 19 open issues.
- 2026-09-22 Pipeline rebuilt: `./run.sh` recreates every processed file and the calculator from raw downloads, with per-row checks against the 10-K text (199 of 199 pass). Issues 1 to 5, 8 and 16 fixed. Calculator diesel now from EIA directly (Sep 14, 2026: $6.285).

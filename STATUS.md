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
- 2026-09-22 Calculator: price box no longer clipped by the number spinner; history charts start in 2006 with the diesel scale sized to the data; rings extended to January-June 2026 from second-quarter 10-Qs (9 carriers, all checks pass); "Built by Data 4 The People" added; diesel source line now names EIA.
- 2026-09-22 Calculator price scale raised to $10; note explains the two-month rail lag. Marten per-mile check: truckload surcharge tracks the formula; the falling share comes from rising base rates per mile (see DATASETS.md).
- 2026-09-22 Knight-Swift switched to its Truckload segment (all years), Werner 2000-2003 to its truckload segment; Union Pacific's escalator exclusion confirmed consistent since at least 2009. Open: Marten brokerage in its revenue base.
- 2026-09-22 Marten revenue base excludes brokerage from 2014 (marked on chart); truckload ring 2025 now 12.4%. Build now parse-checks the page script.
- 2026-09-22 LTL and rail now use what carriers collect (fitted to filings, 2004-Jun 2026) instead of hand-tuned steps; published tariffs (ODFL 128-CC, UP carload) shown as dashed comparison lines, both verified against the carriers' own published values. Truckload formula kept, supported by Marten per-mile data and the DOE matrix.

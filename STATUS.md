# Status

Project: FreightSurcharge
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: fuel-surcharge-impact-viz (visualization page)
Step: done
Since: 2026-09-22

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-22 | Post week 2026-09-21 ($6.529); tie-out 195/195 |
| 2a | Draft with brackets resolved | 2026-09-22 | Claude wrote the full visualization page per Eric |
| 2b | Eric's edit, Claude's look-over | 2026-09-23 | Caveats added, cuts for length, fitted lines and BEA method written in |
| 2c | Slice markup | 2026-09-23 | 75 slices, 780px embed, one divider, no drop cap |
| 2d | Hero 1680x1080 + alt text | 2026-09-23 | Rendered from the calculator's #hero=1 mode; tool renamed Diesel to Fuel Surcharge |
| 2e | SEO | 2026-09-23 | Dataset + WebApplication + 15 FAQs; groceries section added; 3 internal links |
| 2f | Pushed to Prismic (draft) | 2026-09-23 | Draft arRqRhEAACkAL88K in the Migration Release, 87 slices |
| 2g | Mailchimp teaser | 2026-09-24 | Approved by Eric |

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
- 2026-09-22 Truck mix set from the 2022 Economic Census (LTL 15.5%), replacing 50/50. Build now runs the page in headless Chrome and stops on any JavaScript error.
- 2026-09-22 Source coverage check done (scripts/coverage.py; DATASETS.md and METHODOLOGY.md). Diesel chart marks EIA's June 2022 sample change; ring tooltips show carrier counts. Data refreshed: EIA week of Sep 21, 2026 ($6.529).
- 2026-09-22 CPI effect added: up to +0.44 percentage points through freight costs (+0.31 dollar-for-dollar), CPI-U goods/services weights from BLS December 2025; framed as a one-time step in the price level, pump prices excluded. All consumer spending now shown as a range.
- 2026-09-22 Tie-out done for post week 2026-09-21 ($6.529 vs $3.749 a year earlier): 195 checks, 0 failed (TIEOUT.md, scripts/tieout.py, runs in run.sh). Preset buttons now read each year's actual low/high (2020 low corrected to $2.37). Step 1 ready for Eric to close.
- 2026-09-22 Step 1 confirmed by Eric. Next: 2a, needs the slug.
- 2026-09-22 Step 2a opened, slug fuel-surcharge-impact-viz. Eric chose a visualization page (house format as climate-globe), not a Data 4 Thought essay. Viz amended for the post: 780px summary embed (#embed=1) plus the full calculator at GitHub Pages; build writes a full HTML document; tie-out covers the embed (204 checks). Repo made public with GitHub Pages; carrier tariff documents kept local and purged from history (backup bundle in ~/Backups).
- 2026-09-22 Step 2a confirmed by Eric. Next: 2b, Eric edits POST.md directly.
- 2026-09-23 Step 2b confirmed by Eric. Step 2c confirmed: converter clean, warnings are the missing hero only. Next: 2d hero.
- 2026-09-23 Step 2d confirmed (hero from #hero=1). Step 2e: meta set, dataset and app schema, 15 FAQ entries, groceries section (freight is 9.6% of grocery shelf prices; +1.5% to 1.7%), links to thrifty-food-plan, gasoline-share-of-income and supertanker-rates. Tie-out 207 checks. Next: 2f push to Prismic.
- 2026-09-23 Step 2f: pushed to Prismic. Draft arRqRhEAACkAL88K in the Migration Release, hero uploaded, tags and author empty. Next: 2g Mailchimp teaser.
- 2026-09-24 Step 2g confirmed by Eric. Post complete. Prismic draft arRqRhEAACkAL88K in the Migration Release, dated 2026-09-23 (set 20:30 ET in Prismic when publishing). In-embed link removed; the page blurb carries the link to the full calculator.

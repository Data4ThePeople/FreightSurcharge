# Diesel to Fuel Surcharge: how diesel prices reach freight bills and the CPI

A calculator that follows the weekly EIA diesel price through truckload, LTL and rail fuel surcharges, then into the freight bill, store prices and the Consumer Price Index. It sets the model against fuel surcharge revenue that ten large U.S. carriers reported in their SEC filings.

## Live links

- Calculator (GitHub Pages): https://data4thepeople.github.io/FreightSurcharge/dist/index.html
- Published post: https://www.data4thepeople.com/p/fuel-surcharge-impact-viz
- Carrier data as CSV: https://raw.githubusercontent.com/Data4ThePeople/FreightSurcharge/main/data/processed/fuel_surcharge_by_mode.csv

## What's here

- `dist/index.html`: the built calculator, a single page.
- `src/calculator.template.html`: the page template the build fills with data.
- `scripts/`: the pipeline.
  - `fetch_*.py`: download diesel prices, EIA standard errors, 10-K and 10-Q filings, BEA tables, Census and BLS data.
  - `extract/build_*.py`: read fuel surcharge and revenue figures from the filings into `data/extract/`.
  - `build_surcharge.py`: checks every carrier row against its filing and writes the combined table.
  - `fit_surcharge_model.py`: fits the LTL and rail surcharge lines and writes the model settings.
  - `passthrough.py`: freight's share of costs and prices from the BEA tables and CPI weights.
  - `coverage.py`: the source coverage check.
  - `build_calculator.py`: builds `dist/index.html`.
  - `tieout.py`: recomputes the published numbers with separate code and stops the build if any fail.
  - `common.py`: shared paths and helpers.
  - `search/`: small helpers for searching the downloaded filings.
- `data/raw/`: downloaded source files. The SEC filing text and BEA workbooks are not in git; the fetch scripts download them.
- `data/extract/`: one CSV per carrier group, each row with its source filing and a short quote.
- `data/processed/`: the files the calculator reads, including `fuel_surcharge_by_mode.csv`, `surcharge_model.json`, `io_shares.json` and `diesel.json`.
- `data/reference/tariffs.json`: published Old Dominion and Union Pacific surcharge rules, for comparison.
- `explore/`: an exploratory chart of freight producer price indexes against diesel.
- `posts/`: the published post text and images.
- `DATASETS.md`: each dataset, its quirks, and the open issues found and how they were resolved.
- `METHODOLOGY.md`: the method in plain language.
- `TIEOUT.md`: the latest tie-out report for the post week.

## Data sources

| Agency | Dataset | Used for |
|---|---|---|
| U.S. Energy Information Administration | Weekly U.S. No. 2 on-highway diesel retail price (series `EMD_EPD2D_PTE_NUS_DPG`), plus its standard error report | Diesel price, the input to every surcharge |
| U.S. Securities and Exchange Commission | 10-K and 10-Q filings on EDGAR for Marten, Werner, Heartland, Knight-Swift, Old Dominion, Saia, XPO, Union Pacific, Norfolk Southern and J.B. Hunt | Fuel surcharge revenue and the revenue it belongs to |
| U.S. Bureau of Economic Analysis | Input-output accounts, 2023 summary tables (September 2024 release): use table and commodity-by-commodity total requirements | Freight's share of retailer costs, goods and consumer spending |
| U.S. Census Bureau | 2022 and 2017 Economic Census, truck transportation revenue by NAICS industry | Weight of LTL within for-hire trucking |
| U.S. Bureau of Labor Statistics | CPI relative importance, December 2025 | Goods and services weights in the CPI |
| U.S. Bureau of Labor Statistics, via FRED | Producer Price Indexes for truckload, LTL and line-haul rail | Exploratory chart only |

The weekly diesel price is also pulled from FRED (`GASDESW`) as a cross-check.

## How to rebuild

Requirements: Python 3 with `numpy`, `pandas` and an Excel reader such as `openpyxl`. The page checks in `build_calculator.py` and `tieout.py` run the calculator in headless Google Chrome and expect it at the macOS install path.

API keys: the EIA and Census fetch scripts need `EIA_API_KEY` and `CENSUS_API_KEY`. The SEC fetch sends a contact email in its User-Agent, read from `D4TP_CONTACT_EMAIL`. These are loaded from a private env file outside the repo; no key is stored here.

Rebuild everything from the files on disk:

```sh
./run.sh
```

Download fresh data first, then rebuild:

```sh
./run.sh --fetch
```

`run.sh` runs these steps in order and stops at the first failed check:

1. With `--fetch`: `fetch_prices.py`, `fetch_eia_errors.py`, `fetch_10k.py`, `fetch_10q.py`, `fetch_bea.py`, `fetch_census.py`, `fetch_bls.py`
2. `extract/build_TL_A.py`, `build_TL_B.py`, `build_LTL.py`, `build_rail.py`, `build_2026H1.py`
3. `build_surcharge.py`
4. `fit_surcharge_model.py`
5. `passthrough.py`
6. `build_explore.py`
7. `coverage.py`
8. `build_calculator.py`
9. `tieout.py 2026-09-21` (the post week)

## Method notes

- Truckload surcharge uses a common formula: EIA diesel minus $1.25, divided by 6 miles per gallon. It was checked against Marten Transport, which reports both its surcharge revenue and its miles.
- LTL and rail surcharges use what carriers collect, fitted to their filings, not the published tariff tables. Published tables are list prices, and large shippers negotiate their own fuel terms. Because these two lines are fitted to the carrier data, the carrier data is not an independent check on them.
- Trucking is weighted 84.5% truckload and 15.5% LTL, LTL's share of for-hire trucking revenue in the 2022 Economic Census.
- Every carrier row is checked by code: the quote is in the filing word for word, the dollar figure is in the quote, the revenue figure is on a revenue line in the filing, and the percent is correct. A missing year means the company did not disclose it, not zero.
- The CPI effect assumes the whole freight increase is passed along. It counts only fuel's effect through freight, not what people pay at the pump.

---

Data 4 The People

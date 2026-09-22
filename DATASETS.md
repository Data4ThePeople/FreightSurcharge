# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Written 2026-09-22, after the exploratory work had already been done in the
desktop session. So this file is partly an audit of that work. Every problem it
found is listed first, then each dataset in turn, then the model assumptions
the calculator adds on top of the data.

---

## Open issues found while writing this file

These must be resolved or disclosed before Step 1 closes. Numbered so we can
refer to them.

**Reproducibility** (issues 1 to 5 fixed 2026-09-22: `./run.sh` rebuilds
every processed file and the calculator from the raw downloads and stops at
the first failed check. The rebuild reproduced the old files exactly, except
for the changes listed under "What the rebuild changed" below.)

1. **Fixed.** **The scripts do not run from this repo.** They point at paths from the old
   session: `tenk/`, `extract_*.csv` in the working folder, `../GASDESW.csv`,
   `io.py` (the file is now `bea_io.py`), and BEA workbooks that sit inside
   `data/raw/bea/*.zip` and are never unzipped.
2. **Fixed** (`scripts/extract/build_TL_A.py` reads every value from the
   filings by regex; all 59 rows matched the old file). **There is no build script for `extract_TL_A.csv`** (Knight-Swift, Werner,
   Heartland: 59 rows). Those rows cannot be rebuilt from code today.
3. **Fixed** (`build_surcharge.py`, `build_explore.py`, `build_calculator.py`). **There is no script that makes `fuel_surcharge_by_mode.csv`,
   `reported.json`, `diesel.json` or `freight_rates_vs_diesel.csv`** from the
   extracts and raw files.
4. **Fixed** (`passthrough.py` writes `io_shares.json`, which the build injects;
   it reproduced all six shares exactly). **The calculator hardcodes its BEA freight shares** (`IO = {cogs:{truck:6.14,
   rail:0.95}, ...}`). House rule: nothing hardcoded; recompute at render
   time, or generate the constants from a script and check them.

**The 10-K fuel surcharge data**

5. **Fixed** (`build_surcharge.py` checks every row and writes
   `surcharge_checks.csv`; 199 of 199 pass. See "Row checks" below).
   **"All quotes verified" means less than it sounds.** `verify_quotes.py` checks
   that each quote appears word for word in the filing. It does not check that
   the number in the quote equals the number in the row, and it does not check
   the revenue base at all for Heartland, Knight-Swift, Werner or J.B. Hunt.
6. **Knight-Swift changes scope in 2019.** 2017 and 2018 count all fuel
   surcharge, including intermodal. From 2019 the numerator is trucking only.
   The 2019 10-K shows 2018 trucking surcharge as $534.4 million, while our 2018
   row uses $618.8 million. The denominator stays consolidated revenue, which
   includes intermodal, logistics and other revenue with no surcharge, so the
   2019 onward share is biased low. LTL is added in 2021 and U.S. Xpress on
   July 1, 2023.
7. **Werner changes denominator in 2004.** 2000 to 2003 divide by consolidated
   revenue. 2004 on divide by the Truckload Transportation Services segment. The
   share jumps partly because the base shrank.
8. **Fixed:** the quote now shows both lines. **Marten 2007 adds $3.3 million that is not in the quote.** The row is
   $83.8 million truckload surcharge plus $3.3 million from another line. The
   quote only shows the first number.
9. **Union Pacific 2012 on excludes "index-based contract escalators that
   contain some provision for fuel"** (the 10-K says so). Those escalators also
   recover fuel, so UP's reported share understates fuel recovery from 2012.
   UP 2012 on is also rounded to $0.1 billion (±$50 million, about ±0.2
   points of share). UP 2005 is "$1 billion".
10. **UP's base is freight revenue; Norfolk Southern's is total railway
    operating revenue.** Small difference (other revenue is a few percent), but
    not the same measure.
11. **Norfolk Southern 2019 is missing.** The 10-K gives only the change by
    segment. The extract stored the change (−$79 million) in the revenue column
    with method `yoy_change_only`; it was correctly left out of the final CSV
    and of `reported.json`.
12. **Composition changes move the yearly averages.** The rings in the chart
    are simple averages of whoever reported that year. Truckload goes from 1
    carrier (1999) to 2 (2000 to 2001) to 3 (2002 to 2016) to 4 (2017 on, when
    Knight-Swift enters). LTL is 1 carrier in 2007 to 2009 (Saia is missing
    those years). Rail is UP alone before 2006 and in 2019. A jump in a ring can
    come from a carrier joining, not from diesel.
13. **Old Dominion stops in 2020, Saia 2007 to 2009 is missing, XPO starts in
    2019.** Coverage gaps in LTL, not zeros.
14. **The earlier summary said 202 rows; the final CSV has 199.** The 202 were
    the four extract files. Three were dropped: CSX 2002, CSX 2015 (change
    only, never a level) and NSC 2019. The post must use 199.
15. **CSX and ArcBest never disclose a fuel surcharge amount.** They are out of
    the data. That is a disclosure gap, not a finding about them.

**The diesel data**

16. **Fixed:** the build now reads EIA directly. **The calculator's "latest" price is already out of date.** It shows $5.967
    for the week of September 7, 2026. EIA has since published $6.285 for
    September 14 (FRED had not picked it up yet). The build must pull from EIA
    directly and state the week.

**The pass-through model**

17. **Truck is the simple average of the truckload and LTL formulas.** For-hire
    truckload revenue is several times LTL revenue. The weight should come from
    data (for example, Census Service Annual Survey revenue for NAICS 484121
    and 484122), or be stated as an assumption.
18. **The BEA tables are for 2023,** released September 2024. BEA still serves
    the same file today (same size, last modified September 26, 2024). The
    freight shares describe the 2023 economy, not 2026.
19. **Two BEA workbooks were downloaded and never used:** `PCEBridge_Summary.xlsx`
    and `PCEBridge_2017_DET.xlsx`. Either use them as a cross-check on the
    freight share of consumer goods or drop them.

### What the rebuild changed

- **Rings (`reported.json`):** 14 yearly averages moved by 0.01 point. The old
  file averaged shares already rounded to two decimals; the new one averages
  the unrounded shares. No change is larger than 0.01.
- **Diesel:** the calculator now ends at EIA's September 14, 2026 week
  ($6.285), not FRED's September 7 ($5.967).
- **Labels only:** Saia 2002 to 2005 are marked `derived_subtraction` and
  Marten 2007 `derived_sum_of_segments` in the extracts themselves.

### Row checks

For each of the 199 rows, `build_surcharge.py` confirms that the quote is in
the filing word for word; that the surcharge number (or each number it was
computed from, or the company's stated percent) is in the quote at the
precision recorded; that the revenue base appears within 250 characters after
the word "revenue" in the filing; and that the percent equals surcharge divided
by base. To test the checks, every revenue base was nudged by +$1,000, +$0.1
million, +$1 million and −$1 million, and every surcharge by +$0.1 million,
+$1 million and −$1 million. The checks caught every nudged base except 7 of
652, where the
nudged number happens to be another revenue figure in the same filing. They
missed nudges of 0.1 on surcharges quoted in billions, which is expected: "$2.6
billion" cannot tell $2,600.0 million from $2,600.1 million. For J.B. Hunt,
Knight-Swift, Werner and Heartland the extract scripts also find the base on
its own labeled line, which closes the gap for those carriers.

---

## EIA weekly U.S. No. 2 diesel retail price (U.S. Energy Information Administration)

**What it is.** The average pump price of on-highway diesel in the United
States, in dollars per gallon, once a week. Each value is the cash, self-serve
price including taxes as of 8:00 a.m. local time on Monday. It is the index
nearly all fuel surcharge tables reference.

**Where it comes from.** EIA series `EMD_EPD2D_PTE_NUS_DPG` (EIA API v2, route
`petroleum/pri/gnd`). We downloaded it through FRED as `GASDESW`
(`data/raw/fred/GASDESW.csv`, 1,695 weeks). The full FRED file matches the EIA
API exactly, week for week (checked 2026-09-22). No login for FRED; the EIA API
needs `EIA_API_KEY`.

**Version and vintage.** Published about 10:00 a.m. Eastern each Tuesday
(Wednesday after a federal holiday). FRED picks it up a few days later. Our file
ends September 7, 2026. EIA's latest as of this writing is September 14, 2026.

**Coverage.** March 21, 1994 to present, every Monday, no missing weeks. National
average only here; EIA also publishes regions. Survey: Form EIA-888, a sample
of 590 outlets drawn from about 73,000 service stations and 9,500 truck stops,
stratified by region, with every large truck stop chain sampled for certain.
The national price is weighted by each outlet's annual sales volume.

How much is filled in: outlets that do not answer are imputed from their own
past prices, similar outlets, and a commercial price source. EIA will not
publish a week unless at least half of the sales volume is reported rather than
imputed. EIA does not publish the imputed share for each week. **To do in the
coverage check:** see whether the weekly standard error report gives a
response rate.

**Changes over time.** EIA drew a new sample on June 13, 2022 to improve
accuracy. The fuel was low-sulfur diesel early in the series and is now
ultra-low sulfur diesel (under 15 ppm); on-highway diesel switched to ultra-low
sulfur in 2006 to 2010. **To confirm from EIA's history notes:** the exact dates
the published series changed grade, and whether that caused a price step.

**Suppressed, censored or masked values.** A week can be withheld if too much is
imputed. None are missing in our national series.

**Missing data.** None in 1994 to 2026.

**Revisions.** EIA rarely revises published weekly retail prices. We pin the
download date and re-pull before publishing.

**Units and rounding.** Dollars per gallon to three decimals. The third decimal
is finer than the survey's real accuracy (see below).

**Known quirks.**
- Contracts use this exact series, but some use the regional price or the
  monthly average, or reset on a different day of the week. The calculator uses
  the national weekly price for truckload and LTL and a monthly average with a
  two-month lag for rail.
- The monthly diesel in `freight_rates_vs_diesel.csv` is an average of weekly
  values; the method is not written down. Rebuild it in code.

**Uncertainty.** EIA publishes a standard error for each weekly estimate in its
*Detailed Price and Standard Error Report* and flags estimates with a
coefficient of variation above 5%. **To do:** pull the recent national standard
errors and state them.

**License and attribution.** U.S. government work, public domain. Credit:
"U.S. Energy Information Administration, weekly retail on-highway diesel
prices."

---

## Producer Price Indexes for freight transportation (U.S. Bureau of Labor Statistics)

**What it is.** Monthly price indexes for what carriers charge, by industry:
- `PCU484121484121` General freight trucking, long-distance truckload
- `PCU484122484122` General freight trucking, long-distance less than truckload
- `PCU482111482111` Line-haul railroads

**Where it comes from.** FRED CSVs in `data/raw/fred/`. Used only in the
exploratory chart `explore/freight_rates_vs_diesel.png`, not in the calculator.

**Version and vintage.** Monthly. Our files run through August 2026.

**Coverage.** Truckload and LTL from December 2003 (index = 100). Rail from
January 1969, on its own base (the 2003-12 value is 122.2). **The exploratory
chart plots the three indexes on different bases; any published version must
rebase all three to the same month.**

**Changes over time.** **To check:** BLS index base periods and any NAICS or
sample redesigns for these series.

**Suppressed, censored or masked values.** BLS withholds an index value when too
few companies report. None missing in our files.

**Missing data.** None in these three series over their spans.

**Revisions.** BLS recalculates PPI values four months after first publication to
add late reports. The last four months of every pull are preliminary. Pin a
vintage for the post.

**Units and rounding.** Index points, three decimals.

**Known quirks.** The PPI prices include fuel surcharges. BLS's own article on
fuel surcharges (Beyond the Numbers, 2Q 2011) says transportation companies
passed higher fuel costs to customers through surcharges, which pushed the
transportation PPIs to then-record levels in 2008. So these indexes already
contain the effect we are modeling; they are a check on it, not an independent
input.

**Uncertainty.** BLS does not publish standard errors for industry PPIs.

**License and attribution.** Public domain. Credit: "U.S. Bureau of Labor
Statistics, Producer Price Index, via FRED."

---

## Carrier fuel surcharge revenue from 10-K filings (SEC EDGAR, compiled by Data 4 The People)

**What it is.** One row per carrier and fiscal year: fuel surcharge revenue in
millions of dollars, the revenue it is divided by, and fuel surcharge as a
percent of that revenue. Each row carries the source filing and a quote of at
most 200 characters. File: `data/processed/fuel_surcharge_by_mode.csv`, 199 rows.
Yearly averages by mode: `data/processed/reported.json`, which the calculator
plots as open rings.

**Where it comes from.** Annual 10-K filings from EDGAR (`scripts/fetch_10k.py`,
user agent with a contact email). 289 filings downloaded as HTML converted to
plain text in `data/raw/sec_10k/` (not in git; re-fetched by the script).
Extracts in `data/extract/`, one per group.

| Mode | Carrier | Years | Rows | Method |
|---|---|---|---|---|
| Truckload | Marten (MRTN) | 1999 to 2025 | 27 | dollars |
| Truckload | Werner (WERN) | 2000 to 2025 | 26 | dollars |
| Truckload | Heartland (HTLD) | 2002 to 2025 | 24 | dollars |
| Truckload | Knight-Swift (KNX) | 2017 to 2025 | 9 | dollars |
| LTL | Old Dominion (ODFL) | 2002 to 2020 | 19 | percent stated by company |
| LTL | Saia (SAIA) | 2002 to 2006, 2010 to 2025 | 21 | 4 by subtraction, 17 percent stated |
| LTL | XPO (LTL segment) | 2019 to 2025 | 7 | dollars |
| Rail | Union Pacific (UNP) | 2002 to 2025 | 24 | dollars |
| Rail | Norfolk Southern (NSC) | 2006 to 2018, 2020 to 2025 | 19 | dollars |
| Intermodal and truck mix | J.B. Hunt (JBHT) | 2003 to 2025 | 23 | dollars |

J.B. Hunt is in the CSV but not in any mode average in `reported.json`.

**Version and vintage.** Each 10-K as filed. Fiscal years end in late December;
CSX's ends on the last Friday of December. Pulled September 2026.

**Coverage.** 10 carriers out of thousands. These are large, publicly traded
carriers. Small truckload carriers, private fleets and owner-operators are not
here, and they may recover fuel differently. **This sample describes what large
public carriers report, not the industry.** Values are what the company
disclosed; nothing is imputed by us, but four Saia rows are computed by
subtraction and Marten 2007 by addition (issue 8).

**Changes over time.** See issues 6 (Knight-Swift), 7 (Werner), 9 (UP), 12 and
13 (who is in each year). Also:
- Saia 2002 to 2005 is the Saia LTL subsidiary only, from the parent SCS
  Transportation. 2006 on is Saia Inc. consolidated.
- XPO is the North American LTL segment only.
- Knight-Swift 2017 includes Swift only from the September 8, 2017 merger.
- Heartland's revenue base jumps in 2014 and 2022 with acquisitions (Gordon,
  Smith, CFI).
- Old Dominion sometimes restates the prior year (2012 was 16.7% in the 2012
  10-K and 16.5% in the 2013 10-K). We use the value first reported for each
  year.

**Suppressed, censored or masked values.** None; companies either disclose or
do not.

**Missing data.** A missing year means the company did not disclose it that
year, never zero. CSX and ArcBest never disclose an amount (issue 15).

**Revisions.** Companies restate after mergers or new accounting standards (ASC
606 in 2018). Rule: use the figure from the 10-K for that year, and note any
case where a later 10-K restated it.

**Units and rounding.** Millions of dollars. Filed tables are in thousands (three
decimals kept). Narrative figures are rounded: Heartland 2002 to 2015 and
Marten 2008 to 2025 to $0.1 million; UP 2012 on to $0.1 billion. Company-stated
percents to 0.1 point.

**Known quirks.**
- The share is fuel surcharge divided by revenue that *includes* the surcharge,
  which matches the calculator's "share of the freight bill." Werner 2004 on
  and J.B. Hunt use segment or consolidated revenue including surcharge; check
  every base follows this rule (issue 5).
- Consolidated revenue includes brokerage, logistics and other lines that carry
  no surcharge, which pulls the share down (Knight-Swift, J.B. Hunt, Heartland).
- Norfolk Southern 2012's quote ("totaled $1.3 billion in both years") does not
  name the years in the quoted text; confirm in context.

**Uncertainty.** Audited financial statements, so the dollar figures are sound.
The weak points are scope and rounding, above.

**License and attribution.** SEC filings are public. Credit: "Company 10-K
filings, SEC EDGAR; compiled by Data 4 The People."

---

## BEA input-output tables, summary level (U.S. Bureau of Economic Analysis)

**What it is.** Two tables for 2023 at the 71-industry summary level:
- **Use table, after redefinitions, producers' prices**
  (`IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx`). We take the personal
  consumption column (F010): what consumers bought from each commodity, in
  millions of dollars. Transportation and trade margins on those goods appear
  in the truck (484), rail (482), wholesale (42) and retail rows.
- **Commodity-by-commodity total requirements**
  (`CxC_TR_1997-2023_Summary.xlsx`). Each cell is how many dollars of commodity
  *k* are produced, directly and at every earlier step, per dollar of final
  demand for commodity *j*.

**Where it comes from.** `https://apps.bea.gov/industry/iTables Static
Files/AllTablesIO.zip` and `AllTablesSUP.zip`, saved in `data/raw/bea/` (not in
git). No login.

**Version and vintage.** Released September 2024 (files dated August to
September 2024). BEA still serves the same zip as of 2026-09-22. We use the
2023 sheet. Summary tables for recent years are estimates built on the 2017
benchmark and are revised in later releases.

**Coverage.** The whole U.S. economy, 2023. Truck (484) is **for-hire** trucking
only. Trucking by a company's own fleet is counted inside that company's
industry, not in 484. Couriers and parcel delivery are a separate commodity
(492) and are not in our freight share. Air (481), water (483) and pipeline
(486) are also left out of the shock. The total requirements table is built
from domestic production, so freight used abroad to make imported goods is not
counted; U.S. freight that moves imports is.

**Changes over time.** Benchmark years 1997, 2002, 2007, 2012, 2017. **To check:** which NAICS
vintage the industry codes follow in this release.

**Suppressed, censored or masked values.** Zero cells are left blank in the
published sheet ("Selected data with zero values are not shown"). We read blanks
as zero.

**Missing data.** None beyond blanks meaning zero.

**Revisions.** Every September release can revise recent years. Pin the
September 2024 vintage and name it.

**Units and rounding.** Use table in millions of dollars; requirements are
ratios. "Detail may not add to total due to rounding."

**Known quirks.**
- The code divides each row of the requirements table by its diagonal cell
  (`L_kj / L_kk`). This is the standard cost-push formula for a price change
  in one industry, and it is correct for that use. Write it down in the method
  note with a citation.
- Truck and rail are shocked at the same time and the effects are added. That
  ignores the small effect of each on the other.
- `Used` and `Other` (scrap and noncomparable imports) codes need a decision on
  whether they count as goods.

**Uncertainty.** BEA does not publish error bars for input-output tables.

**License and attribution.** Public domain. Credit: "U.S. Bureau of Economic
Analysis, input-output accounts, 2023 (September 2024 release)."

---

## Model assumptions in the calculator (not data)

These are ours, not a publisher's. The post must say so plainly.

| Setting | Value | Where it came from |
|---|---|---|
| Truckload base diesel price | $1.25 | Common peg in published tables; not checked against a carrier tariff |
| Truckload fuel economy | 6.0 mpg | Common peg; not checked |
| Truckload base rate | $2.50 per mile | Chosen so results land near reported shares |
| LTL base price, step, percent per step | $1.15, 5¢, 0.35% | Tuned to match reported shares, not from a real tariff |
| Rail base price, step, percent per step | $1.90, 4¢, 0.25% | Tuned to match reported shares, not from a real tariff |
| Rail lag | 2 months, monthly average | UP 10-K confirms the two-month lag |
| Truck mix | 50% truckload, 50% LTL | Placeholder (issue 17) |

Because the step tables were tuned to fit the rings, the rings cannot also be
used as evidence that the formulas are right. **To do:** find published fuel
surcharge tables in carrier tariffs and check each setting against them.

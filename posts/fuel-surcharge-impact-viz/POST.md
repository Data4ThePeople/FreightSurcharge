---
title: "Diesel Fuel Surcharge Calculator: How Diesel Prices Reach Freight Bills and the CPI"
subtitle: A free calculator that follows the weekly diesel price through truckload, LTL and rail fuel surcharges, the freight bill, store prices and the Consumer Price Index, with every step of the method shown.
slug: fuel-surcharge-impact-viz
date: 2026-09-23
time: 20:30:00-04:00
section: Visualization
hero: images/fuel-surcharge-impact-viz-hero-1680x1080.png
hero_alt: A dark card titled Diesel to Fuel Surcharge, showing what $6.53 diesel, the week of September 21, 2026, does against $3.75 a year earlier. Fuel surcharge is 26.0% of a truckload bill, 26.0% of an LTL bill and 20.2% of a rail bill. Below: freight bill up 15.1%, retailer cost of goods up 1.07%, store prices for goods up 0.7% to 1.1%, and the CPI up to 0.44 points through freight. A chart tracks the surcharge share since 2006, with rings for what carriers reported. Built by Data 4 The People.
meta_title: Diesel Fuel Surcharge Calculator: Freight Costs and CPI
description: Free fuel surcharge calculator: how the weekly EIA diesel price sets truckload, LTL and rail surcharges, and what it adds to freight bills and the CPI.
keywords: fuel surcharge calculator, diesel fuel surcharge, how to calculate a fuel surcharge, LTL fuel surcharge, rail fuel surcharge, diesel prices and inflation, freight cost calculator, EIA diesel price
schema_type: dataset
dataset_name: Fuel surcharge revenue reported by ten U.S. carriers, 1999 to June 2026, with weekly EIA diesel prices
dataset_description: Fuel surcharge revenue and the revenue it belongs to, from the 10-K and 10-Q filings of ten large U.S. truckload, LTL and rail carriers, 1999 through June 2026 (208 carrier-years), joined to the weekly EIA U.S. retail diesel price since March 1994. Includes fitted relationships between the diesel price and the surcharge carriers collect, and freight's share of consumer prices from the BEA 2023 input-output tables.
temporal: 1994-03/2026-09
spatial: United States
measured: Fuel surcharge share of the freight bill|percent; Change in the total freight bill|percent; Effect on the Consumer Price Index|percentage points; Retail diesel price|dollars per gallon
sources: https://www.eia.gov/petroleum/gasdiesel/|https://www.sec.gov/edgar|https://www.bea.gov/industry/input-output-accounts-data|https://www.census.gov/programs-surveys/economic-census.html|https://www.bls.gov/cpi/tables/relative-importance/
distribution: text/html|https://data4thepeople.github.io/FreightSurcharge/dist/index.html;text/csv|https://raw.githubusercontent.com/Data4ThePeople/FreightSurcharge/main/data/processed/fuel_surcharge_by_mode.csv
measurement_technique: Fuel surcharge revenue read from carrier filings with each figure checked against the quoted passage; truckload surcharge as (EIA diesel price minus base price) divided by miles per gallon; LTL and rail surcharges fitted by least squares to carrier-reported revenue; freight's share of consumer prices from BEA commodity-by-commodity total requirements, each row divided by its own diagonal cell; CPI effect weighted by BLS relative importance
credit: Data 4 The People, from the U.S. Energy Information Administration, SEC filings, the Bureau of Economic Analysis, the Census Bureau and the Bureau of Labor Statistics
license: https://www.data4thepeople.com/terms-of-use
app_url: https://data4thepeople.github.io/FreightSurcharge/dist/index.html
app_name: Diesel to Fuel Surcharge calculator
app_category: EducationalApplication
app_description: Free calculator showing how the weekly EIA diesel price sets truckload, LTL and rail fuel surcharges, and what those surcharges add to freight bills, store prices and the Consumer Price Index.
app_features: Set any diesel price from $1 to $10|Fuel surcharge share of the freight bill for truckload, LTL and rail|Change in the total freight bill from any starting price|Effect on retailer costs, store prices and the CPI|Weekly history since 2006 against what carriers reported|Published carrier tariffs for comparison|Free to embed
drop_cap: false
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# Diesel Fuel Surcharge Calculator: How Diesel Prices Reach Freight Bills and the CPI

<iframe src="https://data4thepeople.github.io/FreightSurcharge/dist/index.html?v=20260923b#embed=1" width="100%" height="780" loading="lazy" style="border:0" title="Diesel to Fuel Surcharge: fuel surcharge and price calculator"></iframe>

::: spacer 40px

::: blurb
**[Open the full calculator](https://data4thepeople.github.io/FreightSurcharge/dist/index.html)** **for the history chart, the tables, a choice of starting price, and the published tariffs side by side.**
:::

## Purpose

::: spacer

Most freight moving under contract in the United States carries a fuel surcharge that moves with one number: the weekly average diesel price published by the U.S. Energy Information Administration (EIA). Norfolk Southern, for example, says about 95% of its revenue is covered by contracts with negotiated fuel surcharges. Freight booked on the spot market is usually quoted as one all-in price, with fuel already inside it. When that number rises, shippers pay more to move goods, and some of that cost can reach the prices people pay in stores.

The calculator is free, needs no sign-in, and runs on public data from the EIA, the SEC, the BEA, the Census Bureau and the BLS. It follows that chain one link at a time. Set a diesel price, and it shows how large the fuel surcharge gets for a truckload, a less-than-truckload (LTL) shipment and a rail carload, how much the total freight bill changes, and how much of that could reach retailers' costs, store prices and the Consumer Price Index (CPI).

The CPI number is likely of most interest to investors and anyone watching the inflation data. If what you want to know is what this does to your own costs, look at store prices for goods instead. That number says how much more you would pay for the things you buy, if the whole freight increase reaches the shelf. At the September 21, 2026 price, it is 0.7% to 1.1% higher than a year earlier: about 70 cents to $1.10 on a $100 basket of goods.

## Using the calculator

::: spacer

The summary above has one control: drag the slider to set the diesel price. Everything else is compared with the same week a year earlier. The full calculator, linked above, adds:

- the weekly diesel price and the surcharge share of the freight bill since 2006, with what carriers actually reported shown as rings
- tables of the surcharge share and the freight bill change at every dollar from $2 to $10
- the published tariffs of two large carriers, shown next to what carriers actually collect

The calculator is free to use and free to embed. Add #embed=1 to the end of the full calculator's address for the 780-pixel summary shown here.

### How to read it

- **Freight bill** combines truck and rail, weighted by how much each moves the goods consumers buy.
- **Retailer cost of goods** and **store prices for goods** show how much of the freight change could reach those prices if it is all passed along. Store prices are a range; the "How we built it" section explains why.
- **CPI, through freight** is how much the Consumer Price Index could rise from freight costs alone, if the whole change is passed along. It is labeled "up to" for that reason.
- **The rings** on the history chart are what large public carriers reported in their financial filings. The lines are what the calculator's formulas give for each week.

### What it shows right now

For the week of September 21, 2026, EIA's average diesel price was $6.529 a gallon, the highest weekly price since the series began in March 1994. (That is in dollars of the day, not adjusted for inflation. The previous high was $6.285, the week before.) A year earlier, the week of September 22, 2025, it was $3.749.

With nothing else changing, that increase would raise:

- the total freight bill by 15.9% for truckload, 13.6% for LTL and 12.0% for rail
- the combined truck and rail freight bill by 15.1%
- what retailers pay for the goods they sell by 1.07%
- store prices for goods by 0.7% to 1.1%, and grocery prices by about 1.5% to 1.7%
- all consumer spending, goods and services, by 0.28% to 0.40%
- the CPI by up to 0.44 percentage points, or 0.31 points if stores pass the cost along dollar for dollar

At $6.529, fuel surcharge makes up 26.0% of a truckload bill, 26.0% of an LTL bill and, once the two-month lag passes, 20.2% of a rail bill.

## What this page is

::: spacer

Every chart we publish should be something you can check, question and rebuild yourself. This page documents how we built the calculator: where the data comes from, every step we took, and the judgment calls we made. The code, the data and the built files are in a public repository, linked at the end. If you follow energy costs, we track the price of moving crude oil the same way, in [supertanker rates](https://www.data4thepeople.com/p/supertanker-rates).

## The data sources

::: spacer

Seven public sources go into the calculator. We do not alter any published figure. Our work is connecting them.

**Diesel prices: EIA.** The weekly U.S. average retail price of on-highway diesel, series EMD_EPD2D_PTE_NUS_DPG, every Monday since March 21, 1994. It is the price the fuel surcharge formulas in this calculator are tied to, and the one named in both published tariffs we checked. We pull it directly from EIA.

**Carrier filings: SEC EDGAR.** Annual 10-K reports and quarterly 10-Q reports from ten large public carriers, 1999 through June 2026. Truckload: Heartland Express, Knight-Swift, Marten Transport and Werner. LTL: Old Dominion, Saia and XPO's LTL segment. Rail: Union Pacific and Norfolk Southern. J.B. Hunt, which mixes intermodal and trucking, is in the data but not in the averages. From each filing we take the fuel surcharge revenue and the revenue it belongs to. There are 208 carrier-years in all.

**Published tariffs: Old Dominion and Union Pacific.** Old Dominion's LTL fuel surcharge tariff (ODFL 128-CC, effective April 9, 2025) and Union Pacific's carload rate-based fuel surcharge. These show the list price. The calculator uses what carriers actually collect, and shows the list price for comparison.

**How freight flows into prices: Bureau of Economic Analysis (BEA).** The 2023 input-output tables, which trace every dollar of consumer spending back through every step of production.

**Truckload and LTL weights: Census Bureau.** Revenue of for-hire trucking by industry from the 2022 Economic Census.

**CPI weights: Bureau of Labor Statistics (BLS).** The share of goods and of services in the CPI for all urban consumers (CPI-U), December 2025.

**A check on the truckload formula: Department of Energy.** DOE publishes the weekly fuel surcharge matrix it uses for its own shipments. We use it only as a comparison.

## How we built it

::: spacer

### Step 0: What the publishers do before we get the data

EIA surveys a sample of stations and truck stops every Monday at 8 a.m. local time, asking for the cash, self-serve price including taxes. EIA has used three samples: about 350 outlets in the early years, 403 until June 2022, and 590 since, the last weighted by each outlet's sales. When an outlet does not answer, EIA fills in its price from its own past prices, similar outlets and a commercial price source. EIA does not publish how often that happens, but it will not publish a week if half or more of the sales volume is backfilled.

EIA publishes a standard error with each week. For the week of September 21, 2026 it was 3.2 cents, so the true average was very likely within about 6 cents of $6.529.

When EIA switched samples in June 2022, the new one read 5 to 8 cents lower in the two weeks both ran, and older prices were not revised. That is small next to the price moves here.

Carriers decide what to call fuel surcharge revenue and how to show it. Most of the figures we use come from the discussion section of the filings or from tables the companies label non-GAAP, not from the audited financial statements. Definitions differ between companies and sometimes change over time; Step 7 lists the changes we adjusted for.

BEA's tables give one average for all goods, but freight weighs very differently across them. For each dollar of output, food and beverages use about 6.5 cents of truck and rail freight; computers and electronics use under 1 cent. Heavy, low-value goods will feel a diesel increase more than the averages here suggest; light, high-value goods less.

### Step 1: Diesel price to truckload surcharge

Truckload surcharges are charged per mile. The common formula takes the diesel price, subtracts a base price of $1.25, and divides by 6 miles per gallon. At $6.529 that is ($6.529 − $1.25) ÷ 6 = 88 cents a mile.

We checked this formula against real results. Marten Transport reports both its truckload fuel surcharge revenue and its truckload miles every year. From 2007 to 2025, Marten collected between 91% and 115% of what the formula predicts for that year's average diesel price. DOE's own matrix, which uses a different rule, gives 81 cents a mile at $6.285, against the formula's 84 cents.

### Step 2: LTL and rail, what carriers actually collect

LTL and rail surcharges are a percentage added to the base charge. Carriers publish tables, but most shippers pay less than the published rate. Large shippers negotiate their own fuel terms, the percentage applies only to part of the charge, and railroads also run programs tied to mileage or to a price index.

The gap is large. At $6.529, Old Dominion's published table gives 55.8%, and Union Pacific's published carload rule gives 53.0% for a month that averaged that price. What carriers collect, measured from their filings, is about 35% for LTL and 25% for rail.

To measure what carriers collect, we take each carrier-year's fuel surcharge revenue as a percentage of its other revenue and line it up against that year's average diesel price. For rail we use the monthly average from two months earlier, because that is how Union Pacific bills. A straight line fits the LTL data very closely: each 5 cents of diesel adds about 0.29 percentage points of surcharge. A line fitted only to 2004 through 2019 predicted 2020 through June 2026 within about 1 point on average. Rail is looser: each 5 cents adds about 0.24 points, and railroads have collected less than the older pattern since 2020.

The fitted lines are: LTL surcharge as a percent of the base charge = −2.87 + 5.82 × diesel; rail = −6.21 + 4.84 × diesel, using the monthly average diesel price from two months earlier. Both are fitted on carrier-years from 2004 on, and both are held at zero below the price where they cross it, which is $0.49 for LTL and $1.28 for rail.

We use these fitted lines, not the published tables, because what carriers collect is what reaches shippers' costs.

### Step 3: Surcharge to the freight bill

We hold the rest of the freight rate fixed, so the only thing that changes the bill is the fuel surcharge. For truckload we use a base rate of $2.50 a mile.

A truckload example: at $3.749, the surcharge is 42 cents a mile and the bill is $2.92 a mile. At $6.529, the surcharge is 88 cents and the bill is $3.38 a mile. That is 15.9% more. On an 800-mile load, the bill goes from $2,333 to $2,704.

An LTL example: at $3.749, carriers collect a surcharge of about 18.9% of the base charge; at $6.529, about 35.1%. A $400 shipment goes from $476 to $540, 13.6% more. Rail works the same way and rises 12.0%, though rail customers see it about two months later.

### Step 4: Weighting truckload and LTL

LTL is 15.5% of for-hire trucking revenue in the 2022 Economic Census ($65.7 billion of $423.3 billion). It was 15.9% in 2017. So trucking is weighted 15.5% on the LTL formula and 84.5% on the truckload formula. Local and specialized trucking, such as tankers and flatbeds, use the truckload formula because they are mostly priced by the load or the mile.

### Step 5: Freight bill to prices

BEA's input-output tables trace every dollar of consumer spending back through every step of production: farm or mine to factory, factory to warehouse, warehouse to store. For each step they record how much for-hire trucking and rail it used.

We use BEA's 2023 commodity-by-commodity total requirements table and the personal consumption column of the use table, both at the summary level and at producers' prices. For a price change in one industry, each row of the requirements table is divided by its own diagonal cell, which is the standard way to trace one sector's cost through every later step. Goods are the farm, mining and manufacturing commodities, plus the freight, wholesale and retail margins on them.

Counting all those steps, trucking and rail make up about 7.1% of what retailers pay for the goods they sell, about 4.7% of what goods cost on the shelf, and about 1.9% of all consumer spending. Services use much less freight: about 0.6%, mostly food trucked to restaurants.

Groceries carry more freight than goods in general. Food is heavy, it is worth less per pound than most manufactured goods, and it moves farther through more steps. Counting every one of those steps, trucking and rail are about 9.6% of what groceries cost on the shelf, against 4.7% for goods overall. The same diesel increase therefore raises grocery prices by about 1.5% to 1.7%, roughly double the effect on goods in general. We have looked at grocery prices another way before, by rebuilding the government's [Thrifty Food Plan basket at real prices](https://www.data4thepeople.com/p/thrifty-food-plan-snap-grocery-receipt/).

Store prices come out as a range because it depends on how stores pass along the cost. If they add the higher freight cost dollar for dollar, shelf prices rise by the shelf-level share: 4.7% of a 15% freight increase is about 0.7%. If they keep the same percentage markup, shelf prices rise as much as their cost of goods did: about 1.1%.

### Step 6: The CPI

The CPI weights goods and services differently from total consumer spending. Goods are 36.0% of the CPI-U and services 64.0%. So the CPI effect is 36.0% of the goods effect plus 64.0% of the services effect.

At the September 21 price: goods rise 0.71% to 1.07%, services 0.09%. Weighted by the CPI, that is 0.31 to 0.44 percentage points.

The two ends differ in what the store protects. Passing the cost along dollar for dollar adds the extra freight dollars to the price and leaves the store's profit per item unchanged, so its margin percentage slips. Keeping the same percentage markup raises the price by the same percent the store's cost rose, which protects the margin and collects a few cents more. Freight is 7.1% of what retailers pay for goods but 4.7% of the shelf price, because the shelf price also holds the store's markup. That gap is the difference between the two ends.

Two things to know about that number. It is a one-time step in the price level, not a new ongoing rate. Once passed through, it would add about that much to 12-month inflation for a year, then drop out if diesel holds steady. And it counts only fuel's effect through freight. What people pay at the pump is part of the CPI too, but it is not included here.

### Step 7: The history chart and the carrier rings

The lines on the history chart run the formulas above on every week since 2006, holding today's base rate fixed. The rings are what carriers reported: each full year from annual 10-K filings, and January to June 2026 from second-quarter 10-Q filings. Each ring is the simple average of the carriers in that mode that reported that year. In the full calculator, the tooltip shows how many.

Where a company changed what it counts, we used a measure that stays the same over time:

- Knight-Swift uses its truckload segment in every year.
- Werner uses its truckload segment in every year.
- Marten's revenue leaves out brokerage from 2014 on. Brokerage has no separate surcharge line, and Marten's filings do not break it out before 2014. The chart marks 2014.
- Union Pacific leaves index-based contract escalators out of its fuel surcharge figure, and says so. That has been true since at least 2009, so the series is consistent, but it understates what Union Pacific recovers for fuel.

Two carriers never report a surcharge amount, CSX and ArcBest, so they are not in the data.

One pattern on the chart is worth explaining. The truckload share fell from about 21% in 2012 to about 12% in 2025, at similar diesel prices. The surcharge itself did not shrink much. Carriers' base rates rose: Marten's non-fuel truckload revenue went from $1.72 a mile in 2012 to $2.37 in 2025, so the same surcharge became a smaller part of a bigger bill.

### Step 8: Checking the numbers

For each of the 208 carrier-years, code confirms that the quoted passage appears in the filing word for word, that the dollar figure appears in the quote, that the revenue figure appears on a revenue line in the filing, and that the percentage is computed correctly. A separate script then recomputes every number on the calculator and on this page from the raw data, with its own code, and compares it with the calculator as it runs in a web browser: 204 checks, all passing. The build also confirms that the two published tariffs reproduce each carrier's own posted numbers.

## Updating

::: spacer

EIA publishes a new diesel price every Tuesday for the Monday before. Rebuilding the calculator is one command: it fetches the new price, recomputes everything, runs the checks and stops if anything fails. Nothing on the calculator is typed in by hand. When carriers file new quarterly or annual reports, we add them and they go through the same checks. The numbers on this page are fixed to the week of September 21, 2026; the calculator itself moves with the latest week.

## Honest notes and limitations

::: spacer

**This is illustrative.** Real contracts differ in base prices, steps, caps, rounding and which week's price applies. The calculator shows how a typical surcharge behaves, not what any one shipper pays.

**The pass-through is an upper bound.** The store-price and CPI numbers assume the whole freight increase reaches prices. In practice some is absorbed by carriers, shippers or stores, and the rest arrives over months.

**The CPI number leaves out the pump.** Gasoline and diesel bought by households are part of the CPI and move much more than freight does. This page measures only the freight channel. We covered the direct cost of filling a tank separately, in [gasoline's share of income](https://www.data4thepeople.com/p/gasoline-share-of-income).

**The CPI match is simplified.** The CPI and BEA's consumer spending measure different things: the CPI counts only what households pay out of pocket, while BEA also counts spending made on households' behalf, such as employer-paid health care. We join them with one split, goods and services. A category-by-category match would be more precise. BLS updates the CPI weights each January; these reflect 2024 spending.

**It probably understates the freight effect.** BEA's trucking figures cover only for-hire carriers. Companies that run their own trucks, and parcel carriers, also pay more for fuel, and they are left out.

**Imports are counted only after they arrive.** For imported goods, BEA counts the U.S. trucking and rail that move them after they arrive, not the freight used abroad to make them.

**Ten carriers are not the industry.** Our truckload carriers earn about 3% to 5% of truckload industry revenue, and our LTL carriers about 9% to 11%. Union Pacific and Norfolk Southern earn about 48% of the revenue of the four largest U.S. railroads. The number of carriers behind each ring changes over time, so a jump in a ring can come from a carrier joining.

**The LTL and rail lines are fitted to the rings.** So for those two modes the rings are not an independent check. The truckload line is checked separately, against Marten's miles.

**The published tariffs are snapshots.** They are the versions posted as of September 2026. Carriers revise them, so the dashed lines show today's list prices, not what the tables said in past years.

**The BEA tables describe 2023.** They are the latest available, built by updating BEA's 2017 benchmark with less detailed yearly data. Freight was a bigger part of costs in 2022; using 2022's tables raises the all-spending effect by about 15%.

**The truckload and LTL weights are partly estimated.** The Census Bureau filled in 40% to 50% of LTL revenue in the 2022 Economic Census, and counts only businesses with employees, so owner-operators without payroll are left out. The results barely depend on the weight: anything from 10% to 25% LTL moves the freight bill change by 0.3 points or less.

**Many carrier figures are rounded.** Most rail figures, and many older trucking figures, are rounded in the filings themselves. Union Pacific's January to June 2026 figure adds a second quarter rounded to $0.1 billion, which makes its share uncertain by up to about 0.4 points.

**Older diesel prices have no published error.** EIA publishes standard errors only for weeks since June 2022. The older sample was designed to keep the error within about 1%, about 4 cents at $4 diesel.

## Reproduce it yourself

::: spacer

The code, the data and the built calculator are at [github.com/Data4ThePeople/FreightSurcharge](https://github.com/Data4ThePeople/FreightSurcharge). You need Python and free API keys from EIA and the Census Bureau. The steps are the ones above; the statistics are averages, weighted sums and one straight-line fit per mode. If you rebuild it and get something different from us, we want to know. Tell us, and we will look.

::: divider

## Common questions

::: spacer

### What is a diesel fuel surcharge?

It is an extra charge on a freight bill that rises and falls with the price of diesel. Most carriers tie it to EIA's weekly national average price. Truckload surcharges are usually charged per mile; LTL and rail surcharges are usually a percentage of the base charge.

### How is a truckload fuel surcharge calculated?

A common formula is the EIA diesel price minus a base price, often $1.25, divided by an assumed fuel economy, often 6 miles per gallon. At $6.529 that is 88 cents a mile. Contracts differ in the base price and the miles per gallon.

### Why is the published surcharge so much higher than what carriers collect?

Published tables are list prices. Large shippers negotiate their own fuel terms, the percentage applies only to part of the charge, and some freight moves under other programs. At $6.529, Old Dominion's published LTL table gives 55.8%, while LTL carriers collect about 35% of their base charges.

### How much do higher diesel prices raise inflation?

Through freight alone, the rise from $3.749 to $6.529 diesel could add up to 0.44 percentage points to the CPI, if the whole increase is passed along. That is a one-time step in the price level, not a new ongoing rate. It does not include what people pay at the pump.

### How much do diesel prices add to grocery prices?

More than to goods in general. Food is heavy, cheap by the pound and moves through more steps, so trucking and rail are about 9.6% of what groceries cost on the shelf, against 4.7% for goods overall. The rise from $3.749 to $6.529 diesel works out to about 1.5% to 1.7% on grocery prices, if the whole increase is passed along.

### What is the current fuel surcharge rate?

It changes every week with the EIA diesel price. The calculator above always opens at the latest week. The numbers written on this page are fixed to the week of September 21, 2026, when diesel was $6.529 and the truckload surcharge worked out to 88 cents a mile.

### Is the fuel surcharge based on the DOE or the EIA price?

They are the same number. The Energy Information Administration is part of the Department of Energy, so a contract that says "DOE national average diesel price" and one that says "EIA weekly retail diesel price" point to the same weekly figure.

### Who pays the fuel surcharge, the shipper or the carrier?

The shipper pays it, usually as a separate line on the freight bill, and the carrier keeps it to cover fuel. It is meant to cover a cost, not to add profit.

### Does the fuel surcharge apply to the whole freight bill?

No. In LTL and rail it is a percentage of the base charge, after any discount, and it does not apply to every accessorial charge. That is one reason carriers collect less than their published tables suggest.

### How long does it take for diesel prices to show up in consumer prices?

Truckload and LTL surcharges move within a week or two of the EIA price. Rail runs about two months behind. Beyond the freight bill, the cost has to work through producers, wholesalers and stores, which takes months and is never complete.

### Why is the CPI effect a range?

It depends on how stores pass along a higher freight cost. If they add it dollar for dollar, the CPI effect is about 0.31 points. If they keep their usual percentage markup, it is about 0.44 points.

### Why does rail react later than trucking?

Railroads usually base the surcharge on the monthly average diesel price and bill it about two months later. Union Pacific's October 2026 surcharge, for example, is based on August's average.

### Why does fuel make up a smaller share of truckload bills than it used to?

Carriers' base rates have risen. The surcharge per mile follows diesel about as it always has, but it is now added to a larger base, so it is a smaller share of the total.

### Is $6.529 a record diesel price?

It is the highest weekly price in EIA's series, which began in March 1994, in dollars of the day. Adjusted for inflation it would rank differently; this page does not make that adjustment.

### How often is the calculator updated?

Weekly, after EIA publishes the new diesel price. New carrier reports are added as they are filed.

# How the Diesel to Surcharge numbers are made

Plain-language summary as of September 22, 2026. The detail behind every line
is in `DATASETS.md`. Every number here is rebuilt from the raw data by one
command, `./run.sh`.

## The question

When diesel prices rise, how much do freight bills go up, and how much of that
could reach the prices people pay in stores?

## The chain, in four links

**1. Diesel price.** The U.S. Energy Information Administration (EIA) publishes
the average price of on-highway diesel every Monday, from a survey of 590
stations and truck stops. Almost every freight fuel surcharge is tied to this
number. We pull it straight from EIA. Latest: $6.529 a gallon, week of
September 21, 2026. The numbers below use that week; they update each time
the data is rebuilt.

**2. Diesel price to fuel surcharge.** Each type of freight charges fuel
differently.

- **Truckload:** cents per mile. The standard formula is diesel minus $1.25,
  divided by 6 miles per gallon. At $6.529 that is 88¢ a mile. We checked
  this against Marten Transport, which reports both its surcharge revenue and
  its miles: from 2007 to 2025 it collected between 91% and 115% of what the
  formula predicts.
- **LTL (less-than-truckload, smaller shipments):** a percentage added to the
  shipment's charge. Carriers publish tables, but most shippers pay less than
  the published rate. Old Dominion's published table says 56% at today's
  price. What LTL carriers actually collect, based on their own financial
  filings from 2004 to 2026, is about 35%. We use what they collect.
- **Rail:** also a percentage, but based on the monthly average diesel price
  from two months earlier. Union Pacific's published rate is 53% at today's
  price; what railroads actually collect is about 25%. We use what they
  collect.

**3. Fuel surcharge to the freight bill.** We hold the rest of the freight rate
fixed, so the only thing that changes is the surcharge. From a year ago ($3.75
diesel) to today ($6.53), the total freight bill rises about 16% for
truckload, 14% for LTL and 12% for rail. Trucking is weighted 84.5% truckload
and 15.5% LTL, which is LTL's share of for-hire trucking revenue in the 2022
Economic Census. Truck and rail combined: **about +15%**.

**4. Freight bill to store prices.** The Bureau of Economic Analysis (BEA)
input-output tables trace every dollar of consumer spending back through
every step of production. For-hire trucking and rail make up about 7.1% of
what retailers pay for the goods they sell, about 4.7% of what goods cost on
the shelf, and about 1.9% of all consumer spending. If the whole freight
increase is passed along:

| Level | Change |
|---|---|
| Freight bill | +15.1% |
| What retailers pay for goods | +1.07% |
| Store prices for goods | +0.7% to +1.1% |
| All consumer spending | +0.28% to +0.40% |

The ranges depend on whether stores add the cost dollar for dollar (low end)
or keep the same percentage markup (high end).

**5. What it could add to the Consumer Price Index.** Goods and services are
affected differently. Freight is 4.7% of what goods cost on the shelf but only
0.6% of what services cost (mostly food trucked to restaurants). So goods rise
+0.7% to +1.1% and services +0.09%. The Bureau of Labor Statistics weights the
CPI-U at 36.0% goods and 64.0% services (December 2025). Putting those
together, freight costs could add **up to +0.44 percentage points** to the CPI
(+0.31 if stores pass costs along dollar for dollar).

- This is a **one-time step up in the price level**, not a new ongoing rate.
  Once passed through, it adds about that much to 12-month inflation for a
  year, then drops out if diesel holds steady.
- It counts only fuel's effect **through freight**. What people pay at the
  pump is separate and is not included.
- "Up to" because it assumes the whole increase is passed along. Some is
  usually absorbed, and the rest arrives over months.
- Applying the all-spending figure (+0.28%) to the goods share of the CPI
  would be wrong: that figure already averages in services, so weighting it
  again by goods would cut it to about +0.1 and understate the effect.

## How we checked the data

- **Carrier filings.** 208 rows of fuel surcharge revenue from 10 public
  carriers, 1999 to June 2026, taken from annual 10-K and quarterly 10-Q
  reports. For every row, code confirms that the quote is in the filing word
  for word, the dollar figure is in the quote, the revenue figure is on a
  revenue line in the filing, and the math is right. To test those checks, we
  changed each value slightly; the checks caught nearly all of the changes.
- **Consistent definitions.** Where a company changed what it counts, we
  switched to a measure that stays the same over time. Knight-Swift now uses
  its truckload segment every year. Werner uses its truckload segment every
  year. Marten's revenue leaves out brokerage from 2014 on, because brokerage
  has no separate surcharge (earlier years do not break it out).
- **Published tariffs.** Old Dominion's and Union Pacific's published
  surcharge rules are saved in the project, and code confirms they reproduce
  each carrier's own posted numbers.
- **Diesel.** Our EIA pull matches the FRED copy of the same series week for
  week.

## How complete the data is (coverage check)

- **Diesel.** EIA's weekly price comes from a survey, so it has some error.
  For the latest week, EIA's standard error is 3.2¢, so the true average is
  very likely within about 6¢ of $6.529. Outlets that do not answer are
  filled in from their own past prices, similar outlets and a commercial
  source; EIA does not publish how often that happens. The sample was about
  350 outlets in the early years, 403 until June 2022, and 590 since. When
  EIA switched samples in June 2022, the new one read 5 to 8 cents lower than
  the old one in the same weeks, and EIA did not revise older prices. That
  gap is small next to the price moves in this story.
- **Carrier filings.** Nothing in the rings is filled in by us, but the
  sample is small for trucking. Our truckload carriers earn about 3% to 5% of
  truckload industry revenue, and our LTL carriers about 9% to 11% of LTL
  revenue. Union Pacific and Norfolk Southern are about 48% of the revenue of
  the four largest U.S. railroads. The number of carriers behind each ring
  changes over time (the history chart's tooltip shows it). Most rail figures
  and many older trucking figures are rounded in the filings.
- **Truck mix.** The Census Bureau says 40% to 50% of LTL revenue in the 2022
  Economic Census was imputed (20% to 30% for all trucking). The headline
  barely moves with the weight: any LTL share from 10% to 25% gives a freight
  bill increase within 0.3 points of our figure.
- **BEA tables.** BEA builds the 2023 tables by updating its 2017 benchmark
  with less detailed yearly data. The year matters more than the truck mix:
  freight was a bigger part of costs in 2022, and using 2022's tables raises
  the all-spending effect by about 15% (for example, from +0.26% to +0.30% at
  last week's price).

## What the carrier data shows over time

The share of truckload bills that is fuel surcharge fell from about 21% in
2012 to about 12% in 2025, at similar diesel prices. The surcharge itself did
not shrink much. Carriers' base rates rose: Marten's non-fuel revenue went from
$1.72 a mile in 2012 to $2.37 in 2025, so the same surcharge became a smaller
part of a bigger bill.

## Limits a reader should know

- **This is illustrative.** Real contracts differ in base prices, steps,
  caps and timing.
- **Ten carriers.** The filings cover large public carriers, not the whole
  industry. CSX and ArcBest never report a surcharge amount.
- **The effect on prices is probably understated.** BEA's trucking figures
  cover only for-hire carriers. Companies that run their own trucks, and
  parcel carriers, also pay more for fuel, and those are left out. So is
  what consumers pay directly for gasoline and diesel.
- **Full pass-through is an assumption.** The store-price numbers assume every
  dollar of higher freight cost is passed along. In practice some is absorbed,
  and some arrives months later.
- **LTL and rail are fitted to the same carrier data shown as rings on the
  history chart,** so for those two modes the rings are not an independent
  check. Truckload is checked independently by Marten's miles.
- **BEA's tables describe the 2023 economy** (latest available). Freight's share
  of costs may have shifted since.
- **Union Pacific's January to June 2026 figure** adds a rounded second
  quarter, so its share is uncertain by up to about 0.4 percentage points.

## Still to do before Step 1 closes

1. Tie-out: recompute and list every number that will appear in a chart,
   table or headline.

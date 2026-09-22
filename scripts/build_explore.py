"""Monthly freight PPIs next to monthly average diesel, for the exploratory chart.

Output: data/processed/freight_rates_vs_diesel.csv
Diesel is the mean of the weekly EIA prices whose Monday falls in the month.
The PPIs are as published: truckload and LTL are Dec 2003 = 100, rail is on
its own older base. Rebase before any published chart (DATASETS.md).
"""
import pandas as pd
from common import EIA, FRED, PROCESSED

d = pd.read_csv(EIA / 'diesel_weekly.csv', parse_dates=['week'], index_col='week').price
ppi = {s: pd.read_csv(FRED / f'{s}.csv', parse_dates=[0], index_col=0).iloc[:, 0]
       for s in ['PCU484121484121', 'PCU484122484122', 'PCU482111482111']}
out = pd.DataFrame({'Truckload rates': ppi['PCU484121484121'], 'LTL rates': ppi['PCU484122484122'],
                    'Rail rates': ppi['PCU482111482111']}).dropna()
out['Retail diesel'] = d.resample('MS').mean().round(3).reindex(out.index)
out.index.name = 'observation_date'
out.to_csv(PROCESSED / 'freight_rates_vs_diesel.csv')
print('freight_rates_vs_diesel.csv:', len(out), 'months,', out.index[0].date(), 'to', out.index[-1].date())

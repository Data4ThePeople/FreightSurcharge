"""EIA's weekly diesel standard errors (current sample) and its June 2022 old-vs-new sample comparison."""
from common import EIA, get

BASE = 'https://www.eia.gov/petroleum/gasdiesel/'
for path in ('includes/dieselfuel_recent_prices_and_SEs.xlsx', 'dieselfuel_sample_comparisons.xlsx'):
    b = get(BASE + path)
    (EIA / path.split('/')[-1]).write_bytes(b)
    print(path, len(b), 'bytes')

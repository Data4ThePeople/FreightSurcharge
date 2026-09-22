"""BLS CPI relative importance, December 2025 (2024 weights), U.S. city average.

Output: data/raw/bls/cpi_relative_importance_dec2025.htm (the page as served).
"""
from common import RAW, get

OUT = RAW / 'bls'
OUT.mkdir(parents=True, exist_ok=True)
b = get('https://www.bls.gov/cpi/tables/relative-importance/2025.htm')
(OUT / 'cpi_relative_importance_dec2025.htm').write_bytes(b)
print('BLS relative importance', len(b), 'bytes')

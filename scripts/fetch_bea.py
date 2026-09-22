"""Download the BEA input-output archives (September 2024 release, 1997-2023 summary tables)."""
from common import BEA, get

BASE = 'https://apps.bea.gov/industry/iTables%20Static%20Files/'
BEA.mkdir(parents=True, exist_ok=True)
for z in ['AllTablesIO.zip', 'AllTablesSUP.zip']:
    b = get(BASE + z, timeout=300)
    (BEA / z).write_bytes(b)
    print(z, len(b), 'bytes')

#!/bin/sh
# Rebuild every processed file and the calculator from the raw downloads.
#   ./run.sh           build from what is on disk
#   ./run.sh --fetch   re-download prices, 10-Ks and BEA tables first
# Stops at the first failed check.
set -e
cd "$(dirname "$0")"
if [ "$1" = "--fetch" ]; then
  python3 scripts/fetch_prices.py
  python3 scripts/fetch_10k.py
  python3 scripts/fetch_bea.py
fi
for s in TL_A TL_B LTL rail 2026H1; do python3 scripts/extract/build_$s.py > /dev/null; echo "extract $s: ok"; done
python3 scripts/build_surcharge.py
python3 scripts/passthrough.py
python3 scripts/build_explore.py
python3 scripts/build_calculator.py

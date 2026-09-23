#!/bin/sh
# Render the post hero (1680x1080) from the calculator's #hero=1 mode.
set -e
cd "$(dirname "$0")/.."
SLUG=fuel-surcharge-impact-viz
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="posts/$SLUG/images/$SLUG-hero-1680x1080.png"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1680,1080 --virtual-time-budget=5000 \
  --screenshot="$OUT" "file://$PWD/dist/index.html#hero=1" 2>/dev/null
cp "$OUT" "posts/$SLUG/images/$SLUG-hero-source.png"
~/.claude/d4tp-process/hero check "posts/$SLUG/POST.md"

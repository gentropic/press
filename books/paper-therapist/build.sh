#!/usr/bin/env bash
# Build THE PAPER THERAPIST (hand-runnable ELIZA). A5 mono; fonts from shared
# ../../fonts/. One xelatex pass is enough (no remember-picture overlays).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FONTS="$(cd "$HERE/../../fonts" && pwd)"
export KIT_FONTS="${FONTS}/"     # eliza.py passes this into fontspec Path=
cd "$HERE"
echo "[gen] python eliza.py"; python eliza.py
echo "[build] xelatex eliza"
xelatex -interaction=nonstopmode -halt-on-error eliza.tex >eliza.build.log 2>&1 \
  || { echo "  FAILED — tail:"; tail -15 eliza.build.log; exit 1; }
pages="$(pdfinfo eliza.pdf 2>/dev/null | awk '/^Pages:/{print $2}')"
echo "  -> eliza.pdf  pages=${pages}  overfull=$(grep -c Overfull eliza.build.log || true)"
echo "[note] scaffold: 3 demo keyword pages + cards. Fill KEYWORDS to 19 for v1."

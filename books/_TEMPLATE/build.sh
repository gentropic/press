#!/usr/bin/env bash
# Per-book build. Copy this _TEMPLATE/ to books/<your-book>/ and edit the marked
# lines. The whole point of this file is to solve the ONE hard thing about the
# monorepo: a book in books/<x>/ must find the shared Forme in ../../forme/.
#
# How: point TEXINPUTS at the shared forme/ dir so \usepackage{forme} and the
# Path=fonts/ font loading both resolve. We run xelatex from THIS book's dir, but
# with forme/ (and its fonts/) on the input search path.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FORME="$(cd "$HERE/../../forme" && pwd)"

# --- EDIT THESE ---------------------------------------------------------------
GEN="book.py"            # this book's generator (emits the .tex)
MAIN="the_book"          # base name of the .tex the generator writes
N_EXPECT=0               # expected PDF page count (0 = don't check). The real
                         # invariant: PDF pages MUST equal this. NOT overfull count.
# ------------------------------------------------------------------------------

# Forme + its fonts on the TeX search path. Trailing '//' = search subdirs (fonts/).
# Note Forme's forme.sty uses Path=fonts/ RELATIVE to its own dir, so we also make
# the fonts findable by copying nothing — TEXINPUTS resolves forme/fonts/ via '//'.
export TEXINPUTS=".:${FORME}//:"
export OSFONTDIR="${FORME}/fonts"     # lets fontspec find the bundled .ttf by dir

cd "$HERE"
echo "[gen] python $GEN"
python "$GEN"

echo "[build] xelatex x2 (sequential — never run builds concurrently)"
for pass in 1 2; do
  xelatex -interaction=nonstopmode -halt-on-error "${MAIN}.tex" >"build_pass${pass}.log" 2>&1 \
    || { echo "  pass $pass FAILED — see build_pass${pass}.log"; tail -15 "build_pass${pass}.log"; exit 1; }
done

# THE invariant check: real PDF page count, not the Overfull count (overflow past
# \clearpage produces NO warning — see specs / repo README).
PAGES="$(pdfinfo "${MAIN}.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')"
RERUN="$(grep -c 'Rerun to get' "build_pass2.log" || true)"
echo "[check] ${MAIN}.pdf pages=${PAGES}  rerun-warnings=${RERUN}"
[ "$RERUN" -eq 0 ] || echo "  WARNING: overlay not settled (rerun>0) — run another pass."
if [ "$N_EXPECT" -ne 0 ]; then
  [ "$PAGES" = "$N_EXPECT" ] && echo "  OK: page count matches N=${N_EXPECT}." \
    || { echo "  FAIL: pages=${PAGES} != N=${N_EXPECT} (off-by-one drift!)"; exit 1; }
fi
echo "[done] ${MAIN}.pdf"

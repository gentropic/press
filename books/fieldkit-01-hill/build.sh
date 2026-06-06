#!/usr/bin/env sh
# Build both editions of "Field Kit No.01 — What's Under the Hill?".
#
# Requires:
#   - python3
#   - xelatex (TeX Live / MiKTeX)
#   - the fonts Barlow and Space Mono (both OFL), under fonts/ — fieldkit_full.py
#     loads them by file path via fontspec.
#
# One XeLaTeX pass per file is enough (no remember-picture overlays here).

set -e

python3 fieldkit_full.py            # -> fieldkit_full.tex      (EN)
xelatex -interaction=nonstopmode -halt-on-error fieldkit_full.tex

python3 fieldkit_full.py pt         # -> fieldkit_full_pt.tex   (pt-BR)
xelatex -interaction=nonstopmode -halt-on-error fieldkit_full_pt.tex

echo "Done."
echo "  fieldkit_full.pdf      (EN  — free CC0 edition)"
echo "  fieldkit_full_pt.pdf   (pt-BR — the printed edition)"
echo "Pages render at 220x220mm = 210x210 trim + 5mm bleed (Futura Cod.71)."

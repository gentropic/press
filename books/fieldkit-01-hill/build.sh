#!/usr/bin/env bash
# Build Field Kit No.01 in monorepo mode: style from ../../kit/kit.sty, fonts from
# the shared ../../fonts/. Emits EN + pt-BR editions. No remember-picture overlays
# here, so one xelatex pass per edition is enough (unlike playback).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/../../kit" && pwd)"
FONTS="$(cd "$HERE/../../fonts" && pwd)"

# kit.sty findable by \usepackage{kit}; the generator passes KIT_FONTS into the
# .tex as \kitfontpath so fontspec's Path= resolves the shared .ttf files.
export TEXINPUTS=".:${KIT}//:"
export KIT_FONTS="${FONTS}/"

cd "$HERE"
build_edition () {  # $1 = lang arg ("" or "pt"), $2 = base name
  echo "[gen] python fieldkit_full.py $1"
  python fieldkit_full.py $1
  echo "[build] xelatex $2"
  xelatex -interaction=nonstopmode -halt-on-error "$2.tex" >"$2.build.log" 2>&1 \
    || { echo "  FAILED — tail:"; tail -15 "$2.build.log"; exit 1; }
  local pages; pages="$(pdfinfo "$2.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')"
  local ovf;   ovf="$(grep -c Overfull "$2.build.log" || true)"
  echo "  -> $2.pdf  pages=${pages}  overfull=${ovf}"
}

build_edition ""   fieldkit_full       # EN  (free CC0 edition)
build_edition pt   fieldkit_full_pt    # pt-BR (the printed edition)

echo "[done] both editions. Expect 46 pp, 220x220mm (210 trim + 5mm bleed)."
echo "Press files: ./make_pdfx.sh (PDF/X-1a; TrimBox 210 / BleedBox 220)."

#!/usr/bin/env bash
# Wrap the press file as PDF/X-1a for Futura (Livro Capa Dura Quadrado, Cod.71),
# per their fechamento instructions:
#   text -> curves, CMYK, PDF/X-1a, with TrimBox inset from MediaBox by the bleed.
#
# Recipe adapted (almost verbatim) from gentropic/playback `make_pdfx.sh`, which
# Futura accepted on "The Book That Plays Back". The box-based approach (TrimBox /
# BleedBox set by offset, no drawn crop marks) is what Futura reads.
#
# Input : fieldkit_full_pt.pdf  (miolo, 220x220mm = 210x210 trim + 5mm bleed)
# Output: miolo_x1a.pdf         (upload this)
#
# ── IMPORTANT, and different from Playback ──────────────────────────────────
# Playback's miolo is B/W (Pólen 90g), so CMYK conversion was trivial (K only).
# Field Kit is FULL COLOUR on COATED stock (couché fosco 170g). Point the
# conversion at a COATED CMYK profile and PROOF the shift — the warm bone
# (#F2ECDD) and the ferrous (#C75B39) WILL move under CMYK. A coated FOGRA39
# profile is the right target for couché. TeX Live ships one at:
#   /usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc
# Override with:  ICC=/path/to/CoatedFOGRA39.icc ./make_pdfx.sh
# ─────────────────────────────────────────────────────────────────────────────
#
# Requires Ghostscript on PATH (not present in the dev container that built this;
# run on your machine / in Claude Code).
set -euo pipefail

GS="${GS:-gs}"
IN="${1:-fieldkit_full_pt.pdf}"
OUT="${2:-miolo_x1a.pdf}"
# 5mm bleed = 14.173pt. TrimBox = MediaBox shrunk by this on all four sides.
BLEED_PT="${BLEED_PT:-14.173}"

# CMYK ICC: prefer a coated profile (couché). Fall back hunts for common ones.
ICC="${ICC:-}"
if [ -z "$ICC" ]; then
  for c in \
    /usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc \
    /usr/share/color/icc/CoatedFOGRA39.icc \
    "$(dirname "$(command -v "$GS")")/../share/ghostscript/"*/iccprofiles/default_cmyk.icc ; do
    [ -f "$c" ] && ICC="$c" && break
  done
fi
[ -n "$ICC" ] && [ -f "$ICC" ] || { echo "No CMYK ICC found. Set ICC=/path/to/profile.icc"; exit 1; }
echo "Using CMYK profile: $ICC"

# stage the ICC locally with a space-free name (pdfwrite's PS 'file' op dislikes spaces)
cp "$ICC" ./_cmyk.icc

# PDF/X output-intent (embedded CMYK profile required by X-1a)
cat > _pdfx_def.ps <<'PS'
%!
[ /_objdef {icc_PDFX} /type /stream /OBJ pdfmark
[ {icc_PDFX} << /N 4 >> /PUT pdfmark
[ {icc_PDFX} (_cmyk.icc) (r) file /PUT pdfmark
[ /_objdef {OI} /type /dict /OBJ pdfmark
[ {OI} << /Type /OutputIntent /S /GTS_PDFX
   /OutputConditionIdentifier (Coated FOGRA39)
   /Info (coated_cmyk.icc) /DestOutputProfile {icc_PDFX} >> /PUT pdfmark
[ {Catalog} << /OutputIntents [ {OI} ] >> /PUT pdfmark
PS

"$GS" -dPDFX -dBATCH -dNOPAUSE --permit-file-read=_cmyk.icc \
  -sColorConversionStrategy=CMYK -dNoOutputFonts \
  -dPDFXTrimBoxToMediaBoxOffset="{$BLEED_PT $BLEED_PT $BLEED_PT $BLEED_PT}" \
  -dPDFXSetBleedBoxToMediaBox=true \
  -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
  -sOutputFile="$OUT" _pdfx_def.ps "$IN"

rm -f _cmyk.icc _pdfx_def.ps
echo "Wrote $OUT (PDF/X-1a, fonts->curves, CMYK)."
echo "Verify:  pdffonts $OUT   (expect NO fonts listed)"
echo "         pdfinfo -box $OUT   (TrimBox inset 5mm from MediaBox; BleedBox = MediaBox)"
echo "Then PROOF the colour — bone/ferrous shift under CMYK is expected."

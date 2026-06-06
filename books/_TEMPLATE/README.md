# _TEMPLATE — starting point for a new book

Copy this whole folder to `books/<your-book>/`, then:

1. **Write the generator** (`book.py` by default) — it emits the book's `.tex`.
   `\usepackage{forme}` will resolve to the shared `../../forme/forme.sty` via the
   `TEXINPUTS` set in `build.sh`. Pick the Forme options you need:
   `[color]` / `[bw]` / `[bleed]` / `[cropmarks]`.
2. **Edit `build.sh`** — set `GEN`, `MAIN`, and `N_EXPECT` (the expected page count;
   the build fails if the rendered PDF doesn't match — this is the only invariant
   that matters).
3. **Build:** `bash build.sh` (runs the generator, two XeLaTeX passes, checks pages).
4. **Press file:** when ready, run `../../tools/make_pdfx.sh` against the bleed PDF
   to produce PDF/X-1a (fonts→curves, CMYK, trim/bleed). See its header for the
   per-book trim inset (5 mm A6 = 14.173 pt; adjust per trim).

## House rules (don't relearn the hard way)

- **Build sequentially.** Never run two xelatex builds at once — they corrupt the
  remember-picture overlays and the shared aux files.
- **Page count is the truth.** A page that overflows its slot spills past
  `\clearpage` with NO `Overfull` warning. Trust `pdfinfo | Pages`, not grep.
- **UTF-8 everywhere.** Write generated `.tex` with `encoding="utf-8"` — the
  platform default (cp1252 on Windows) silently corrupts accented characters.
- **Determinism.** Fixed seed; print a SHA of the source in the colophon.

## A note on Forme's trim (read before your first non-A6 book)

The shared `forme/forme.sty` currently **hardcodes A6 (105×148 mm)** trim and a
5 mm `[bleed]`. That's correct for playback/FieldKit-square-TBD but NOT general.
The first book that needs a different trim should generalise Forme to a
**trim profile** (see `specs/GAMEBOOK_SPEC.md` §9.1 and `DISTRIBUTION.md`'s Lulu
re-target). Until then, assume A6. Don't silently ship a wrong trim.

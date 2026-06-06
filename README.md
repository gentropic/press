# press

The **Gentropic / GCU press** — sources for a small line of generative,
deterministic, public-domain books. Each book rebuilds byte-identically from a
short program and a fixed seed; the design system, tools, and engine notes are
shared across the house.

> *Information lives in shape, weight, position and label.* — Forme

## Layout

```
press/
├─ forme/        the shared design system (Forme): forme.sty, fonts/, FORME.md
├─ tools/        shared build helpers (make_pdfx.sh — PDF/X-1a for press)
├─ specs/        engine R&D: GAMEBOOK_SPEC, ELIZA_SPEC
├─ books/        one folder per book
│  └─ _TEMPLATE/ starting point for a new book (build convention inside)
└─ LICENSE / LICENSE-CONTENT   code = MIT, text/figures = CC0 (house-wide)
```

## The books

| Book | Folder | Status |
|---|---|---|
| *The Book That Plays Back* (Edition 00) | — (own repo) | **published** · A6 hardcover · ISBN 978-65-02-14290-5 |
| *Field Kit No.01 — What's Under the Hill?* | `books/fieldkit-01-hill/` | drafting |
| *The Paper Therapist* (hand-runnable ELIZA) | `books/paper-therapist/` | concept (`specs/ELIZA_SPEC.md`) |

**Note on playback:** the first book stays in its own repo
([`gentropic/playback`](https://github.com/gentropic/playback)) on purpose — its
URL is printed in ink on the cover and colophon, registered with an ISBN, and a
physical copy is deposited at the Biblioteca Nacional. It is treated as a frozen,
published edition; its `forme.sty` is the *as-shipped snapshot*. The **living**
Forme lives here in `forme/`, and future books build against it.

## Conventions

- **Deterministic.** Same source + same seed → identical output. Generators print
  a SHA of their sources in the colophon.
- **Reproducible build.** Two XeLaTeX passes (the foot timeline settles on pass 2).
  **Build sequentially, never concurrently** — overlapping runs corrupt the
  remember-picture overlays and aux files.
- **The only real invariant check is the page count**, not the Overfull count: a
  page-string that overflows spills past `\clearpage` with *no* warning. Verify the
  rendered PDF page count equals the N the generator computes.
- **Press files** go through `tools/make_pdfx.sh` → PDF/X-1a (fonts→curves, CMYK,
  trim/bleed). Built PDFs ship via GitHub Releases, not the repo.

## Licensing

Code (generators, `forme.sty`, tools) — **MIT** (`LICENSE`).
Text, figures, generated PDFs — **CC0** (`LICENSE-CONTENT`).
Keep the split; do not relicense.

*Geoscientific Chaos Union · Belo Horizonte*

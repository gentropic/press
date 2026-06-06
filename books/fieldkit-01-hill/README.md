# Field Kit No.01 — *What's Under the Hill?*

*(pt-BR: **O Que Tem Embaixo da Colina?**)*

A board-book-styled but genuinely rigorous tour of **geostatistics**, for the
very young **and** the curious grown-up. Every page carries two layers:

- a big **Barlow Black** read-aloud line for the toddler ("One rock shouts a
  giant number."), and
- a small **Space Mono** `//` gloss naming the real concept for the adult
  ("`// capping / top-cut — taming an extreme value so one sample can't
  dominate`").

It is the sibling of ***The Book That Plays Back*** (`github.com/gentropic/playback`)
and shares its philosophy: one seeded generator, single source of truth, CC0
content / MIT code, neo-dadaist GCU engineering.

- **Imprint:** Geoscientific Chaos Union (gentropic.org)
- **Licence:** content **CC0**, code **MIT**, fonts **SIL OFL** (see `LICENSE`, `LICENSE-CONTENT`)
- **Seed:** 7 (the whole deposit rebuilds identically from it)

## Build

```sh
./build.sh
```

Requires `python3`, `xelatex` (TeX Live/MiKTeX), and the fonts in `fonts/`
(Barlow + Space Mono, loaded by file path via fontspec). Outputs:

- `fieldkit_full.pdf` — **EN** (the free CC0 edition)
- `fieldkit_full_pt.pdf` — **pt-BR** (the edition that goes to print)

Pages render at **220×220 mm = 210×210 trim + 5 mm bleed** (Futura Cod.71).

One generator, two editions: `python3 fieldkit_full.py` (EN) /
`python3 fieldkit_full.py pt` (PT). The language layer is a set of tables keyed
by page **name** — see `docs/DESIGN.md`.

## Press (fechamento)

```sh
ICC=/path/to/CoatedFOGRA39.icc ./make_pdfx.sh fieldkit_full_pt.pdf miolo_x1a.pdf
```

Produces PDF/X-1a (fonts→curves, CMYK, TrimBox/BleedBox) for Futura. Needs
Ghostscript. See `docs/PRODUCTION.md` — and **proof the CMYK colour shift**.

## What's where

```
fieldkit_full.py        the generator (single file, seed 7)
build.sh                build both editions
make_pdfx.sh            wrap a built PDF as PDF/X-1a for Futura
fonts/                  Barlow + Space Mono (OFL)
proofs/                 latest rendered proofs (regenerable)
reference/gabarito/     Futura's Cod.71 21×21 hardcover templates + instructions
docs/
  DESIGN.md             how the book works: seed, field, palette, structure, bilingual layer
  PRODUCTION.md         print decisions + the gabarito specs + fechamento
  PUBLISHING.md         ISBN / ficha / legal deposit / distribution
  STATUS.md             current state, placeholders, and the ordered to-do
```

## Status (short)

Both editions build at **46 pp**, opening on the illustrated title page, with
front matter (illustrated title + copyright/dedication verso carrying **ISBN and
ficha placeholders**). Content, capping, model-choice, glossary, references all
in; full pt-BR review done; 210 trim + 5 mm bleed in place.

**Next:** reveal-on-turn imposition check → pad 46→48 (back coda) → fechamento →
capa wrap → guardas. Placeholders to fill: dedication, subtitle, ISBN, ficha.
Full detail in `docs/STATUS.md`.

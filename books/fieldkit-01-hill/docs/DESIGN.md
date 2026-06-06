# DESIGN.md — how *Field Kit No.01* is built

## The core device

Every content page has two registers:

- **read-aloud** — one big Barlow Black line, toddler-facing, via the `\readaloud{}` macro.
- **gloss** — a small Space Mono line opening with `//`, naming the real concept,
  via `\gloss{}`. This is the grown-up's layer.

Plus a quiet flight-deck-nursery scaffold on every page (`\scaffold`): warm bone
field, a thin basalt60 frame inset, corner ticks, a Space Mono panel tag + folio
in the header (`\header{tag}{folio}`).

## Seed & the field

`SEED = 7`. The deposit is a single seeded simulation:

1. white noise → repeated **box-smoothing** → **quantize to 6 levels**, on a
   `W=12 × H=7` grid. Sample/drill columns are `[1, 5, 9]`.
2. A **centred ore anomaly** is blended in: a continuous field `_fn = sim_cont(7,5)`
   is mixed with a Gaussian `_bump` centred at `(5.5, 3.0)`, spread `(2.8, 2.1)`,
   weight `_w = 0.6`:  `_comb = (1-_w)*_fn + _w*_bump`. Result: a coherent rich
   core at roughly (col 5, row 3) tapering outward — so the book has a *real*
   orebody to find, not just noise.

**Detrend-before-variography.** Because the centred trend stops the variogram
reaching a sill, the variogram / model-choice figures use a **separate stationary
field** `grade_stat` (= the quantized `_fn`, no bump). This mirrors real practice
(remove the trend, then do variography) and keeps those figures honest.

Tunable knobs sit at the top of `fieldkit_full.py`.

## Palette & type

- bone `#F2ECDD`, basalt `#24272D`, basalt60 `#6E727B`, ground `#D7CDB4`, waste `#CDC6B5`
- iron ramp (6 tints): `RAMP = ["F0E7D2","E8C57E","E0A14B","D07B3C","B85535","8F3B2E"]`
- accents: teal `#2FA199`, ferrous `#C75B39`, azure `#3B7DD8`
- fonts: Barlow (`\dispBlack`, `\dispSemi`) + Space Mono (`\mono`, `\monoB`),
  loaded by file via fontspec. No italics are used (none loaded).

## Structure (6 acts + back matter)

- **Front matter:** illustrated title page (the cover art) → copyright/dedication verso.
- **ACT I — THE UNKNOWN:** ground, it varies, we drill, deep & shallow, THE LOUD ROCK
  (capping), mostly mystery.
- **ACT II — HOW THE GROUND HANGS TOGETHER:** fair play (stationarity), near, far,
  touching (nugget), forgetting (range), biggest gap (sill), count pairs, the
  difference curve (variogram), A CHOICE OF CURVE (the model is a choice), with the
  grain (anisotropy).
- **ACT III — THE GUESS:** one block, who votes, the blend, the fairest blend
  (kriging), how sure (kriging variance).
- **ACT IV — MANY GROUNDS:** too smooth, MANY MAYBES (local distribution), ROLL THE
  DICE (draw not mean), WRITE IT DOWN (sequential conditioning), dream many hills,
  all fit the holes, a spread of answers.
- **ACT V — BLOCKS & DECISIONS:** support (volume–variance), cutoff, grade–tonnage,
  cross-validation, where to dig.
- **ACT VI — BONUS:** declustering, screen effect.
- **Back matter:** GLOSSARY (two columns, ~21 terms), TO LEARN MORE (10 canonical
  references, chronological), COLOPHON.

### Simulation is *taught*, not hand-waved (Act IV)

too-smooth (the estimate takes the safe middle) → MANY MAYBES (a bell of candidate
tints = the conditional distribution) → ROLL THE DICE (draw one off-centre — that's
the roughness) → WRITE IT DOWN (the pick becomes data; sequential) → dream many
hills → all fit the holes → a spread of answers.

## Bilingual (one generator, two editions)

`python3 fieldkit_full.py` (EN) / `python3 fieldkit_full.py pt` (PT). The language
layer is a `PT` flag plus tables keyed by page **name**: `NAME_TR` (panel names),
`RA` (read-aloud), `GL` (gloss), `DIV_T/DIV_S` (divider titles/subs), `LBL_TR`
(in-figure labels), `FOLIO_TR` (ACT→ATO), `PREFIX_TR` (BONUS→BÔNUS, COLOPHON→COLOFÃO).
Cover & colophon branch on `PT` inline. **Brand marks stay English**
(Geoscientific Chaos Union), per the GCU naming rule. pt-BR title: *O QUE TEM
EMBAIXO DA COLINA?*

A full pt-BR appropriateness review was applied (e.g. morro→colina with correct
gender, cleaner variogram axis nouns *distância/diferença*, cutoff label
*escuro = cavar · claro = deixar*, Act II divider *SE ENCAIXA*, etc.). Technical
glossary verified BR-correct (efeito pepita, alcance, patamar, krigagem, teor de
corte, minério/estéril, testemunho, validação cruzada, desagrupamento, realizações,
suporte/volume–variância, efeito de tela).

## Mechanics

- **Figure auto-numbering:** a regex renumbers every `FIG.NN` in document order
  after the body is assembled, so inserting/reordering pages never desyncs numbers.
- **Hyphenation OFF** document-wide (`\hyphenpenalty=10000` etc.) so Portuguese words
  wrap whole; zero overfull boxes in both editions.
- **Bleed/trim (`wrap_bleed`):** the design is authored on an 18-unit (originally
  180 mm) canvas. The `wrap_bleed` pass scales each page to **210 mm** via
  `\resizebox` (type included — proportions unchanged), centres it on a **220 mm**
  page, and floods the matching background (bone, or basalt for dividers) into the
  **5 mm bleed ring**. So the design code is untouched; only the page wrapper changed.

## The illustrated-open decision

An earlier pass gave the book formal front matter (half-title, frontispiece, text
title page, copyright) — which read as adult-book ceremony and, by moving the cover
art out of the interior, made the book "lose its face." Fix: the **illustrated
cover art is now the title page** (the book opens on its face), and the ceremony is
trimmed to two pages (illustrated title + copyright/dedication verso), so Act I
arrives on page 3. The same illustration also becomes the capa wrap art →
front-to-interior continuity.

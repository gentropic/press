# PRODUCTION.md — printing *Field Kit No.01*

## Printer & format (decided)

- **Printer:** Futura Express (Belo Horizonte) — local, trusted, hand-deliverable.
  Product: **Livro Capa Dura Quadrado, Cod.71**. Digital printing.
- **Format:** **21×21 cm hardcover** (210×210 trim). Chosen over 15×15 so the fine
  dual-layer (Space Mono gloss, two-column glossary, references) stays legible;
  10×10 and 21×21 were the other square options.
- **Miolo (interior):** **couché fosco 170 g**, 4/4 full colour. (Futura's spec
  sheet caps the miolo at 150 g, but the configurator allows 170 g — confirmed in
  cart. 170 g is opaque enough that the dark divider pages don't ghost; coated
  beats uncoated for the heavy solids and full-bleed darks. Avoid couché brilho,
  offset, reciclato.)
- **Lamination:** **laminação fosca, frente-e-verso.** "Frente e verso" here =
  front cover + back cover (both *outer* faces of the wrap) — NOT the inside (the
  endpapers cover that). **Not soft-touch/aveludada** for the everyday/kids copies:
  it's the most fingerprint-/scuff-/burnish-prone finish and worst on a dark cover.
  Soft-touch is reserved for a possible deluxe/gift edition (with foil or spot-gloss
  on the ore).
- **Binding:** **PUR** ("lombada quadrada"), confirmed from the Playback spine.
  PUR is the *good* perfect binding and grips coated stock well; fine for kids and
  for a thin 48-pp block at 21×21 (opens far better than Playback's chunky A6).
  Layout rule: keep critical content out of the gutter (content is already ~12–14 mm
  inset, satisfied).

## Quantity & price (decided)

- **~10 copies, pt-BR only.** EN lives as the free CC0 PDF (+ a future web twin).
- Futura price curve (qty → R$/copy): **1 → 287,73 · 5 → 160 · 10 → 135.** Flattens
  by 10 (≈ the paper+labour floor), so ~10 is the sensible batch (≈ R$1,350).

## fabricadolivro.com.br — evaluated and rejected

Much cheaper on paper (≈ R$63/copy @4) but: miolo caps at **115 g** (show-through
risk on our heavy darks), only **20×20** (not 21×21), an explicit **>15% coverage
price surcharge** (our book is ~100% coverage, so the quote wouldn't hold), and a
**middling Reclame Aqui reputation** (~6.4–7.6, recurring delivery-delay/comms
complaints). Futura wins on trust, locality, and a known-good Playback result.

## Gabarito specs (Futura Cod.71, in `reference/gabarito/`)

Read straight from the templates (mm):

- **Miolo:** art **220×220** → trim **210×210** → **5 mm bleed** all sides,
  **5 mm safety** (keep text/important art ≥5 mm inside trim). Our content sits
  ~8–14 mm in — clear.
- **Capa (case wrap):** flat **475×250 mm** — contracapa | spine | capa, with
  turn-ins (~17 mm), board ~216 mm, spine ~10 mm in the template. **The spine flexes
  with page count** → CONFIRM the exact spine width with Futura for a **48 pp / 170 g**
  block (it'll be thin, ~8–10 mm, likely too narrow for spine type).
- **Guardas (endpapers):** **430×220 mm** spreads. Per the instructions, used **only
  if the cover option is "frente e verso"** (the whole-wrap option) — which is exactly
  where the block-model endpaper idea belongs.
- **Fechamento (export, instructions p.8):** **PDF/X-1a**, **CMYK only (never RGB)**,
  **all fonts converted to curves**, images ≥300 dpi (moot — all vector), trim marks
  + document bleed. We satisfy this via `make_pdfx.sh` using box-based TrimBox/BleedBox
  (no drawn crop marks) — the same approach Futura accepted on Playback.

## Fechamento pipeline (`make_pdfx.sh`)

Adapted almost verbatim from Playback's proven recipe: Ghostscript with
`-dNoOutputFonts` (fonts→curves), `-sColorConversionStrategy=CMYK`, an embedded
CMYK output-intent, `-dPDFXTrimBoxToMediaBoxOffset={14.173 ...}` (5 mm) and
`-dPDFXSetBleedBoxToMediaBox=true`, `-dPDFSETTINGS=/prepress`.

**The one Field-Kit-specific point:** Playback is B/W, so CMYK was trivial. Field
Kit is **colour on coated stock**, so point the conversion at a **coated CMYK
profile** (CoatedFOGRA39 is right for couché; TeX Live ships
`.../colorprofiles/FOGRA39L_coated.icc`) and **proof the shift** — the warm bone
`#F2ECDD` and ferrous `#C75B39` will move under CMYK. Verify with
`pdffonts` (expect none) and `pdfinfo -box` (TrimBox inset 5 mm from MediaBox).

## Page count

For digital PUR, an **even** count is the minimum; a **multiple of 4** is the safe
target. Body content is fixed at 44 pp; with the lean front matter (2 pp) the book
is currently **46 pp**. At lockup, pad to **48** as a **back coda** (the iron-ramp
frontispiece as a closing bookend + a blank end-leaf), *not* as front ceremony — keeps
the fast illustrated opening. Confirm Futura's exact multiple requirement.

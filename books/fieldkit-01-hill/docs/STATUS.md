# STATUS.md — where we are, what's next

_Last updated: 2026-06-05._

## Current state

- Both editions build clean: **EN `fieldkit_full.pdf` + pt-BR `fieldkit_full_pt.pdf`**,
  **46 pages**, zero overfull boxes.
- **Opens on the illustrated title page** (the cover art = the book's face), then a
  **copyright/dedication verso** carrying the author credit, the CC0/MIT + seed-7
  colophon block, an **ISBN slot**, and a dashed **ficha slot**. Act I lands on p3.
- Interior is at **210×210 trim + 5 mm bleed** on a 220 mm page (`wrap_bleed`).
- Content complete: all 6 acts; capping ("The Loud Rock"), A Choice of Curve
  (model-is-a-choice), the two-column glossary, the 10-reference "To Learn More",
  the centred ore body, and the taught simulation mechanism (maybes → roll → write).
- Full pt-BR appropriateness review applied. Figure auto-numbering + no-hyphenation in place.

## Placeholders to fill (then a rebuild)

| Placeholder | Current value | Source |
|---|---|---|
| **Dedication** | "For every kid who ever wondered what's under the hill." / PT equivalent | Arthur to write |
| **Subtitle** | "geostatistics for the very young — and the curious grown-up" | Arthur to confirm |
| **ISBN** | `[ to be assigned ]` / `[ a ser atribuído ]` | CBL registration |
| **Ficha** | dashed `[ ficha catalográfica — CBL ]` box | CBL, generated LAST |

## Next steps (ordered)

1. **Reveal-on-turn imposition check.** Now the body opens on a recto (p3). Verify
   each setup→payoff pair (samples→guess, many-maybes→roll-the-dice, etc.) hides
   correctly across a physical turn — i.e. the *setup* sits on a **recto** so the
   payoff is unseen until you turn. Nudge order if a pair is off.
2. **Pad 46 → 48** (multiple of 4). Add a **back coda** (the iron-ramp frontispiece
   as a closing bookend) + a blank end-leaf — *not* front ceremony. Confirm Futura's
   exact page-count multiple.
3. **Fechamento** (`make_pdfx.sh`): coated-CMYK + fonts→curves + TrimBox 210 /
   BleedBox 220 + PDF/X-1a. **Proof the CMYK colour shift** (bone/ferrous move).
4. **Capa wrap** (475×250): place the cover art to the template; **confirm spine
   width with Futura for 48 pp / 170 g** first (likely too thin for spine type).
   Optional deluxe: foil or spot-gloss on the ore.
5. **Guardas** (430×220): block-model endpaper pattern — only if the cover option is
   **frente-e-verso**.
6. **ISBN + DOI + ficha:** register one CBL ISBN (PT hardcover) + a Zenodo DOI for
   digital; generate the ficha LAST and slot it onto the copyright verso.
7. **Archive** CC0 to **Zenodo + Internet Archive** (as planned for Playback).

## Open decisions (Arthur)

- **Cover option:** frente-e-verso (enables printed endpapers / guardas) vs. plain.
- **Deluxe edition?** soft-touch + foil/spot-gloss on the ore.
- **Author on the title illustration?** currently credited on the copyright verso.
- **References:** confirm exact editions/years to taste (he's the expert).
- **Web interactive twin:** deferred; reuses the seed-7 field.

## Pending from outside

- Futura: exact **spine width** for 48 pp / 170 g; page-count multiple rule.
- Futura: confirm "frente e verso" lamination = both outer cover faces (not inside).
- A **CMYK proof** to approve the colour shift before the run.

## Sibling

*The Book That Plays Back* — `github.com/gentropic/playback`. Same construction
DNA (seeded single-source generator, CC0/MIT, Barlow+Space Mono, Futura hardcover,
`make_pdfx.sh`). Playback printed: A6, Cod.73, Pólen 90 g, 17 mm spine, 310 pp B/W;
ISBN 978-65-02-14290-5; gift run via Futura, free Lulu Pocket as a planned sibling.

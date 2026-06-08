# GEOSTATS_LADDER.md — one curriculum, age 3 to PhD

The connecting map between GCU's geostatistics artifacts. They were built
separately and didn't know about each other; this is the spine that unifies them.

> **GCU has a geostatistics curriculum spanning preschool to practitioner — four
> artifacts, one philosophy (do it by hand; *become* the computer), graded by the
> developmental ladder in `AUDIENCE.md`. The pieces interoperate: the same
> indicator-counting idea scales up in rigor across the whole line.**

## The four tiers

| Tier | Artifact | Rung (`AUDIENCE.md`) | Core skill |
|---|---|---|---|
| **Very young (~3–6)** | **Field Kit No.00 — *Look!*** (`books/fieldkit-00-look/`) | observe / compare (concrete) | notice the ground is layered & varies |
| **Kid (~5–9)** | **the missing kid-tier kit** (counting + SIS pieces — TO BUILD) | tally / pattern (counting) | count agreements vs. disagreements |
| **Older kid / curious adult** | **Field Kit No.01 — *What's Under the Hill?*** (`books/fieldkit-01-hill/`) | read the curve (level-3 graph) | the variogram, kriging, simulation as *ideas* |
| **Practitioner / adult** | **GSLIB: The Board Game** (`gentropic/gslib_boardgame`) | full rigor | actually *do* kriging & SGSIM/SIS by hand |

This is the same graded-series move as everything else (`AUDIENCE.md`): don't make
one artifact span toddler-to-PhD; make a *ladder* of artifacts, each honest about
its rung.

## The adult capstone: GSLIB: The Board Game (separate repo)

`gentropic/gslib_boardgame` ("GSLIB Unplugged" / "KrigeKrieg") is the **finished
adult capstone** — real geostatistics with cards, atlases, nomograms, and chips:
Ordinary/Simple Kriging via lookup atlases, SGSIM, SIS, hand variography. It is the
purest expression of the house thesis applied to the home field — *"if you can't
explain geostatistics with playing cards and colored chips, you don't really
understand it"* is the Chinese Room flipped into pedagogy.

**It lives in its OWN repo and stays there** (it's a card/board product with its own
print pipeline, BOM, and manual — not a press book). This spec only *references* it;
`gslib_boardgame` remains the source of truth.

> **Status (as of this writing): parked mid-flight, Dec 2025.** First test prints
> submitted to the print shop, awaiting samples; `TODO.md` there has the open items
> (SK atlas interleave into the full manual, chip-legend card, post-playtest tweaks).
> Last worked under an earlier model. **Worth returning to** — it's close, and it's
> the anchor the rest of this ladder hangs from.

## Which board-game mechanics are kid-portable (the triage)

The "how much works for kids?" answer, by rung — this is what to *harvest* for the
missing kid tier, vs. what stays adult:

- ✅ **Kid-native (counting rung):**
  - **Indicator variography by counting.** The indicator semivariogram reduces to
    *counting pairs that straddle the cutoff*: with I ∈ {0,1}, [I(xᵢ)−I(xⱼ)]² is 1
    iff they disagree, so γ_I(h) = (discordant lag-h pairs)/2N(h). **No arithmetic —
    just tally agree/disagree.** (Sanity-check with the geostatistician, but this is
    the reduction; see `gslib_boardgame/docs/theory/INDICATORS.md`.)
  - **SIS with black/white pieces** — "add the weights, bigger pile wins, place that
    colour." No variance. The repo notes SIS needs no variance calculation.
  - **KrigeKrieg as territory** — "claim adjacent squares, biggest blob wins"
    (Go/Reversi-shaped); the kriging underneath hides behind a lookup, the way
    playback hides its engine.
- ⚠️ **Teen / motivated older kid (the curve rung):** continuous-value **SGSIM** —
  Gaussian draw, variance nomogram, real-number weights. This is the "conceito de
  curvas" wall the No.01 review found. Not for little ones.
- ❌ **Adult only:** 3-/4-point OK atlases, 70-pattern SK, full variance machinery.
  The graduate content — and it's *right* that it stays adult.

## The missing kid tier — the rung to build

Between No.00 (observe) and No.01 (the curve) sits a **counting** rung with no
artifact yet. Build it from the kid-portable mechanics above:

- **Mechanic:** lay out two-state items in a line/grid; the reader physically
  **pairs neighbours and counts the disagreements at each distance** — building an
  indicator variogram by hand, one tally at a time. Then SIS-style "bigger pile of
  weight wins" to fill unknown cells. Pure *propose-experiências*, no arithmetic.
- **Production — cheap 3D-printed two-state tiles** (rich/poor, tall/flat,
  filled/notched), NOT premium die-cut paper. This is the manipulatives idea: simple
  tiles bulk-print for pennies, where die-cut booklet cutouts are premium. Ship the
  **`.stl` as a CC0 artifact** so the manipulative re-manufactures from source —
  same ethos as the book rebuilding from seed and the relief block from a height map
  (see `ART.md` §deluxe). Already foreseen in `gslib_boardgame/docs/IDEAS.md`
  ("3D Printed Pieces").
- **Caveat — kit, not bound book.** Loose tiles + a booklet = a *physical product*
  (box / punch-out / baggie) with its own fulfilment reality (shipping objects, not
  paper). The safe pure-GCU core is the **CC0 `.stl` + booklet PDF** anyone can make
  themselves; a sold boxed kit is the more-ambitious shell around that.

## Open / next
- **Return to `gslib_boardgame`** — resume from its Dec-2025 parked state (test
  prints / `TODO.md`).
- **Build the kid-tier counting kit** — the indicator-tile manipulative; the bridge
  rung. (Could be "Field Kit No.½" or its own thing.)
- Confirm the indicator-variogram-as-counting reduction with the geostatistician
  before it goes in a kid's book.

---

*GCU. This file is a MAP, not a build — the artifacts live in their own
folders/repos. Code MIT, content CC0.*

# Field Kit No.00 — *Look!* (working title)

The **foundation** of the Field Kit series: the truly-for-the-very-young book that
*earns* the abstraction No.01 delivers. Not about geostatistics — about
**observation**. The ground is layered, it varies, and you can see it if you look.

Born from the first real-reader review of No.01 (see `specs/AUDIENCE.md`): No.01
found its real audience (older kids + curious adults), and revealed that a more
concrete, hands-on book belongs *underneath* it. No.00 is that floor.

## The seed image

A childhood memory the reviewer (the author's mother) offered:

> *"Tante Christel, em viagens, nos mostrava as camadas do solo, visíveis nos
> morros cortados na beira da estrada. Nunca esqueci."*

A road-cut hillside, its soil layers exposed. The ground is *layered*, it *varies*
from place to place, and a child can **see** it. That is the whole thesis of
geology-for-the-very-young in one remembered, sensory moment — zero math, zero
curves. No.00 opens here.

## What it teaches (habits of mind, not formulas)

The Trojan horse (handled with care — delight first, tools underneath):
- **Look.** The world rewards attention; things have insides.
- **Compare.** Two rocks, two layers, near vs. far — meaning comes from difference.
- **Notice variation.** It's not the same everywhere; that's interesting, not a flaw.
- **Wonder "why here?"** the seed of every later science.
- **Try it.** Dig a little hole. Pick up two stones. Draw what you see.

These quietly prepare *exactly* the intuitions No.01 then formalises (spatial
variability, "near things are alike", sampling) — but here they're pure observation
and doing, no plotted relationships. A reader who does No.00 is ready for No.01.

## Design

Same house **Kit** system as No.01 (`../../kit/kit.sty` — colour-first, square,
full-bleed, the `\scaffold`/`\readaloud`/`\gloss` furniture). Likely keep the
two-voice device but **lower the gloss level**: the `//` line for the grown-up
should name a *habit* ("// look closely — things have layers"), not a technical
term. Confirm trim with No.01 (square 210×210, Cod.71) unless a different size
serves little hands better.

**Status: concept.** No generator yet — the content design (the page sequence, the
concrete comparisons, the "try it" prompts) is the real creative work and the next
step. See `docs/STATUS.md`.

## House rules that apply

- `specs/AUDIENCE.md` — be honest about the true audience; this IS the very-young tier.
- `specs/FRONTMATTER.md` — reserve the ficha footprint from day one if it'll register.
- Build via a `build.sh` like the other books (shared kit + fonts); page-count is
  the only real invariant; build sequentially; UTF-8 writes.

CC0 text/figures, MIT code — house-wide.

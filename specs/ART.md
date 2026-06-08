# ART.md — how GCU books make pictures

A house convention. The short version:

> **House art is computed, not drawn.** GCU draws with code and geometry, never a
> pen. Two proven modes already shipped; a third (a virtual printing press) is the
> plan for anything that needs warmth.

## What's already proven

- **Playback** — zero illustration. Boards, rings, marks, the foot-timeline: all
  **TikZ primitives** (lines, circles, letters). Beautiful, not one drawn picture.
- **Field Kit No.01** — "art" is the **seed-7 simulated field** (an algorithm) plus
  simple geometric iconography (drill cores, the earth ramp, ?-blocks). Hand-placed
  scenes built from clean shapes, not rendered drawings.

The through-line: **diagrammatic + generative.** This is a real aesthetic
(flight-deck / instrument-panel / blueprint), and crucially it's art a
non-illustrator can produce at professional quality, because the tools don't care
whether you can draw. For the diagram-native books (Comprehension Zero boards &
mats, the gamebook engine), this *is* the whole answer — boards, grids, reticles,
type. No further machinery needed.

## When a book wants a real illustration: the virtual printing press

For the occasional **deliberate spot illustration** (e.g. a Comprehension Zero
cold-open scene), the house technique is a computed B&W pipeline — NOT a GUI tool
(no Blender, no OpenSCAD), all in-language JS so the art stays *source* that
rebuilds:

**Pipeline:** a **three.js** scene (geometry described in a committed `.js`) →
rendered headless via **Playwright** (load the page, screenshot the canvas) → a
custom **NPR post-shader** that emulates printmaking. Output committed as source +
the rendered asset.

- **Render ≥3–4× final size** (`deviceScaleFactor` / large canvas) so the raster is
  crisp at 300 dpi. Spot illustration = raster is fine; we do NOT need vector. (This
  is the one trade vs. a CAD `projection()` approach — accepted deliberately.)
- Determinism: fixed camera + fixed seed for any jitter; pin the renderer
  (SwiftShader/software) if bit-exact is wanted. "Rebuilds *visually* identically"
  is the bar; bit-exact is nice-to-have.
- Color: output is RGB → CMYK at the prepress step (`tools/make_pdfx.sh`), same as
  everything. K-only black-on-cream is the easy case.

### Making it WARM, not cold (the shader is a printmaking press, not a CAD viewport)

"Cold" is a property of *CAD* line art (uniform outlines on white), not of B&W line
art in general — pen-and-ink, woodcut, engraving, scratchboard are all lines, all
mono, and deeply warm. The shader emulates *those*, via (in rough order of impact):

1. **Line-weight variation** — biggest single lever. Modulate edge thickness by
   depth (near heavier, far lighter) and light angle (shadowed side heavier, the
   classic ink convention) + slight per-edge randomness. Takes it ~70% from
   blueprint to drawing on its own.
2. **Wobble** — perturb edge sampling with low-frequency noise so lines breathe
   (the "imperfect art shader"). Subtle; over-wobble looks gimmicky.
3. **Fill forms with MARKS, not gray** — the move people miss. Don't leave interiors
   empty (that's what makes CAD art a diagram). Map luminance to **hatching /
   cross-hatching** (engraving look), **stippling** (softer/storybook), or
   **woodcut masses** (bold black + carved white). Screen-space: sample scene
   luminance → threshold against a hatch/dot pattern → black-or-white.
4. **Mark character, not paper grain** — give the *marks* rough edges / uneven ink
   density. Do **NOT** simulate paper grain or an ink/cream ground: the book prints
   on real **Pólen** (real tooth, real cream), so faking the substrate is redundant
   *and* slightly fraudulent — it'd double the grain and gray the cream. **House
   rule: simulate the artist's hand (line, wobble, hatching, mark roughness); leave
   the substrate (paper tooth, ink, cream ground) to physical production. Never
   simulate what the physical object already provides.** (Same logic as "paper" =
   unprinted in the files; the cream shows through.) Keep hatching open enough that
   the real paper breathes through the gaps — also an argument against over-inking.
5. **Soften the forms** (in the modeling): bevel edges, avoid perfect primitives,
   lumpy low-poly reads warmer than spheres/cubes.

**Hardest part to get right:** the hatching/stipple fill (screen-space hatching can
"shimmer" or look mechanical). Prototype it FIRST — one object, one hatch shader:
does it read as an engraving or as a screen door? Line-weight + wobble are easy; the
fill is the risk.

### Register dialed per book
Even within warm B&W: **fine engraving/hatching** for a Comprehension Zero spot
(intricate, a little old-fashioned — on-tone); **bold simple woodcut** (chunky
black shapes, minimal line) for Field Kit No.00 (toddler-soft; fine hatching is too
busy/old for a 3-year-old). The technique spans the range; choose the register.

## The reusable tool
The harness becomes a house tool like `make_pdfx.sh`: a `tools/render/` with
`scene.js` (per-book) + the NPR shader + a Playwright `shoot.js`. Drop a new
`scene.js` per book's spot art. (NB: there's now an official Blender MCP connector
in the same Anthropic creative-tools batch as Affinity — a fallback if a scene ever
needs real depth/figures the JS path can't manage; same session-setup caveat as
Affinity. Default stays three.js.)

## Someday / deluxe: a real hand-pressed relief block

Escalation from *simulated* woodcut to an **actual 3D-printed printing block** —
because the 1-bit shader output IS a height map: black = raised (prints), white =
recessed (paper). One source, two manufacturing paths (screen illustration AND
relief matrix). Feasible, with real caveats:

- **Resin (SLA/MSLA)** over FDM (FDM layer lines texture the ink — sometimes a
  feature, usually noise). Print the plate solid-ish and thick (flex/crack under
  pressure otherwise).
- **Coating/ink step required** (your instinct was right): raw PLA/resin is
  ink-repellent → light matte primer/sanding, or oil-based relief ink, or a thin
  shellac seal (also protects resin from moisture).
- **Bolder, more open marks than the screen version** — fine ridges don't transfer,
  valleys fill with ink. The medium ENFORCES the woodcut register (loops back to
  §register).
- **Pressure** even & firm (baren / book-press). Hand-pulled = each pull varies =
  the charm, but it's a **handmade-edition** technique, NOT the offset run.

**Where it fits:** NOT the main run (can't hand-pull 310pp ×11). Right for a single
**hero image / frontispiece**, a **limited hand-pressed special edition** (one
plate on the real Pólen), or shipping **the block's `.stl` as a CC0 artifact**
(reader prints their own block, pulls their own copy — art that re-manufactures
from source, like the book rebuilds from seed). File under "deluxe, someday."

---

## Decisions on record
- Diagram-native books → TikZ/geometry only (done; no new tooling).
- Spot illustration → three.js + Playwright + custom NPR (woodcut/engraving) shader,
  B&W, ≥3× for 300 dpi, committed as source. **Raster is fine; vector not required.**
- Simulate the hand, never the substrate (no fake paper grain — real Pólen supplies it).
- Field Kit No.00's warm toddler art is the one genuinely open art question — likely
  bold-woodcut register, but TBD; decide when No.00 is actually built.
- Hand-pressed 3D-relief block = deluxe/someday, same 1-bit source as height map.

*GCU. Build the hatch shader on one object before committing to any book's art.*

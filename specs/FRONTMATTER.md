# FRONTMATTER.md — make the first pages breathe

A house convention, written after *The Book That Plays Back* taught it the hard
way. The lesson in one line:

> **Front matter is content, not a formality — budget its final, fullest form on
> day one. Reserve the ficha's footprint from the start.**

## What went wrong (the cautionary tale)

playback's copyright verso was laid out assuming we *might not* get a ficha
catalográfica. When the CIP block arrived, it had to be retrofitted onto a page
already holding the dedication + colophon. The result was a Tetris game: trimming
`\vspace`s by tenths of a centimetre, merging colophon sentences, shrinking the
ficha to 5.6 pt (later rescued to 6.5 pt) — all to claw back ~3 lines so the block
fit without bumping the 310-page count. It works and looks fine now, but it was
avoidable churn. The page wasn't *budgeted* for its real contents.

(FieldKit-01 got this right by accident: it ships a dashed
`[ ficha catalográfica — CBL ]` placeholder box, so the hole is already there.)

## The rule: reserve the hole

If a book *might* ever get a ficha, lay the copyright page out **as if it already
has one** — leave the ~10–11-line + boxed footprint empty (a dashed placeholder is
ideal). An empty reserved box is always better than a later squeeze. The ficha's
size is predictable: a centred 2-line CIP header, a boxed record of ~8 lines
(author / title-statement / ISBN / subject headings / CIP-no + CDD), then a 2–3
line "Índices" trailer with the cataloguer credit.

## Budget the whole first-page stack, per trim

Every GCU book's front matter is the same DNA — plan all of it up front:

| Slot | Notes |
|---|---|
| **Title page** | title, subtitle, author, imprint (GCU), place · year |
| **Copyright verso** | dedication · colophon (CC0/MIT + "rebuilds from seed N") · **ISBN** · **ficha (reserve it!)** |

Decide the *sequence and spread* deliberately by trim size:
- **Tiny (A6, playback):** everything crams onto one verso — so it MUST be budgeted
  tight from the start; there is no slack to retrofit into.
- **Roomier (A5+, square FieldKit):** give the ficha its own breathing room — its
  own lower-half, or even split dedication (one page) from copyright+ficha.

The right layout is a *decision made early*, never an emergent squeeze.

## Decide the imprint/ISBN posture early — it changes the printed ficha

The cataloguer prints what's legally true about the registrant:
- **ISBN registered to the person** (no registered *editora*) → the ficha reads
  **"Ed. do Autor"** (Author's Edition). Correct, common, zero stigma; GCU still
  appears everywhere else (cover, spine, title, colophon) as the **imprint**.
- **Want GCU printed AS the publisher in the ficha?** That needs GCU to be a real
  registered entity (CNPJ + editora registration + its own ISBN prefix block) —
  a bureaucratic/tax step worth it only if GCU publishes others' work or becomes a
  formal business. For a personal art-press, "Ed. do Autor" is the right record.

Either way: pick the posture before you finalise the title page, because the imprint
line and the ficha text depend on it.

## Encoding + sizing gotchas (carried from playback)

- **Typeset the ficha NATIVELY** (real text, not a placed image) so it stays
  reproducible and on-brand. Use **ASCII LaTeX accents** (`\c{c}`, `\~a`, `\'i`,
  `\^a`) so it is encoding-proof in print — never rely on literal UTF-8 bytes
  surviving the toolchain. (And always write generated `.tex` with
  `encoding="utf-8"` regardless — the cp1252 trap.)
- **Min legible size:** the ficha is fine print, but keep it **≥ ~6.5 pt** on the
  final stock; verify accented glyphs (ã, ç, í) on a *physical* proof — diacritics
  blur first at tiny sizes.
- **Page-count invariant still rules:** the ficha is multi-line and can reflow the
  verso onto a second page. After adding it, re-verify the PDF page count (not the
  Overfull count — see the house README / playback notes).

## The reuse opportunity (TODO)

Because every GCU book repeats this exact stack, it should be a **shared helper**,
not hand-rolled per book: a `frontmatter({title, author, dedication, isbn, ficha,
seed, trim})` that lays out title + verso **with the ficha footprint pre-reserved**,
sized to the trim. Solve "front matter that breathes" once; reuse for ELIZA,
FieldKit No.02, and beyond. Until that exists, follow this doc by hand:
**reserve the box, budget the stack, pick the imprint posture, size ≥ 6.5 pt.**

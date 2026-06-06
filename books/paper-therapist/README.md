# The Paper Therapist — a hand-runnable ELIZA, in a book

A book you **operate** with a pencil and a notepad. The book is the program; the
pad is RAM; **you are the CPU.** You write a sentence, follow the printed rules,
and the book talks back — reproducing Weizenbaum's 1966 ELIZA (the DOCTOR script)
closely enough to run his actual published conversation by hand. You converse with
it, feel it "understand" you, and — because you ran every step yourself — know
exactly how hollow the trick is. *That gap is the book.*

The inverse of *The Book That Plays Back*: playback precomputes everything and you
navigate; here nothing is precomputed, so it accepts **arbitrary input** — the
conditioning happens at read-time, in your pencil.

**Status: scaffold.** The engine works and the hard page (the two-anchor "mat") is
proven pleasant to operate (that was the only real risk). What remains is *labor,
not risk*: fill the 19-keyword roster, run the 1966 conformance check, write the
tutorial + the foot-essay. A5, mono — cheap to print, like playback.

## Build

```sh
bash build.sh        # -> eliza.tex -> eliza.pdf  (A5, fonts from ../../fonts/)
```

The generator is **engine-as-data**: each keyword is one entry in `KEYWORDS` in
`eliza.py`. Adding a keyword = appending a dict (type `spot`/`grab`/`two` drives
the page layout), not writing LaTeX. The scaffold currently emits one worked page
of each type + the two fixed reference cards.

## The design

Full design + roster + the working-memory limits are in **`docs/DESIGN.md`**
(a copy of the house spec `specs/ELIZA_SPEC.md`). The short version:

- **One flip, one tick per turn.** Spotter card (first keyword wins) → flip to its
  page → grab via the **mat** (printed cut-here boxes) → swap the grab (back-cover
  table) → drop into the next un-ticked template → tick. Doctor speaks.
- **Three keyword types:** 🔵 spot (canned reply), 🟢 grab-after (one anchor),
  🟡 two-anchor (the showcase mats — where the uncanny mirror happens).
- **The pad is the only state:** the transcript + a 2-line MEMORY shelf (passive).
- **v1 = 19 keywords**, the +3 (`alike`/`like`/`everyone`) chosen so the book runs
  Weizenbaum's 1966 transcript — which doubles as the conformance test.

## To do (labor, ordered)

1. Fill `KEYWORDS` to the 19-keyword roster (`docs/DESIGN.md` §4).
2. Tutorial page ("how to operate this book") + the `(none)` fallback page.
3. Run the **1966 conformance** conversation by hand; every Doctor line must match.
4. Foot-essay (Weizenbaum, the ELIZA effect, the Chinese Room) + the honest-limit
   colophon. Confirm final page count.
5. Then: ISBN/ficha if it's to be a registered edition (or just ship CC0 + Lulu).

CC0 text/figures, MIT code — house-wide.

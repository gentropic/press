# SEARLE_PLAYS_CHESS.md — the chess book (Comprehension Zero №1)

*Design sketch, not yet built. Title evolved: the **Searle Plays Chess** working
title is retired (we don't use the real Searle as a character — see §0.1); this is
now **Comprehension Zero №1**, the chess book, working title TBD (candidates:
"Standing Orders", "Protocol", "Check"). Sibling to `ELIZA_SPEC.md`.*

A book you **operate** to play chess. The book is the engine; you are the CPU. You
follow a short, exact rule-ladder; the book makes legal, purposeful-looking moves;
you win against weak opponents and lose to anyone decent. At no point do you form a
chess *thought*. And printed on the cover is a **measured Elo** — proof of exactly
how good the not-understanding is.

---

## The series: COMPREHENSION ZERO

GCU's reader-as-CPU line (the old "become a machine" books, now a brand). The name
is the thesis in two words — **competent output, zero understanding** — and reads
as thriller ("Threat Level Zero") while being a literal cognitive-science claim.
A numbered series like Field Kit:

| № | Book | You become | Status |
|---|---|---|---|
| **1** | the chess book (this spec) | a chess engine | concept |
| **2** | The Paper Therapist (`ELIZA_SPEC.md`) | a chatbot | scaffold |
| (3) | the parser book (Liberdade, deferred) | a translator | idea |

Every book: a plain instructional surface (you run the rules), a foot-essay
carrying the philosophy (Chinese Room etc.), and the hollowness made literal. The
Paper Therapist retro-fits into the series.

---

## 0. The thesis (why this is more than a toy)

It is the **Chinese Room** (Searle 1980) staged on chess — and chess sharpens the
argument in three ways the original Mandarin version cannot:

1. **AI's home turf.** "Can machines think?" ran through chess for a century
   (Turing's paper machine → Deep Blue → Kasparov). A Chinese Room *made of chess*
   isn't a random domain; it's staged where humanity first asked whether
   symbol-shuffling is thought.
2. **Adversarial, visceral output.** A chess move *does something to you* — you win
   or lose. The reader runs rules over symbols (literally a board of them),
   understands nothing about chess, and **a game still happens and someone wins.**
   The Room made tangible, not argued.
3. **The Elo is the Turing test, quantified.** Searle's argument is qualitative
   ("seems to understand, doesn't"). Chess lets you put a *number* on the seeming.
   Nobody has put an Elo on the Chinese Room. **"Elo ~700"** on the cover is a
   precise claim about how competent rule-following-without-understanding is.

The reader *becomes* the man in the room: follows ~7 rules, plays ~700-Elo chess,
thinks nothing. The closing turn of the knife:

> *"You just played chess at roughly 700 Elo. You followed seven rules. You never
> once thought about chess. Were you playing? Was the book? When Deep Blue beat
> Kasparov — was that any different from what you just did, only faster?"*

The acid only burns if the number is real (see §4). The Elo is not marketing — it
**is** the thesis: that rule-following-without-understanding achieves a specific,
measured competence. Hand-wave the number and you hand-wave the argument.

### 0.1 Searle is CREDITED, not charactered

The real **John Searle (1932–2025)** and his Chinese Room (1980) are engaged
*seriously* in the foot-essay (§5b), by name. He is **NOT** a character in the
fiction — we don't caricature a real (recently deceased, and reputationally
complicated) person as a recurring imprint mascot. The protagonist is a generic
invention (§0.2). This keeps GCU clean and the philosophy respectful, and gives the
series a reusable owned character the real Searle never could be.

### 0.2 The frame: Jack Stone, the Operator

The book opens with a **one-page cold-open fiction** (the only "story" — keep it to
one page; the power is in the *doing*, not plot). Then the book proper is the plain
instructional engine + foot-essay.

- **Protagonist: Jack Stone** — a thriller-generic name pitched so squarely it reads
  as an unreplaced placeholder. An "Operator": elite-coded in every cosmetic way,
  comprehension **zero** underneath. The gap between the tactical surface and the
  total absence of understanding *is* the Chinese Room, in a plate carrier.
- **Tone: tactical-deadpan ⨯ Usborne-puzzle-book earnestness.** Clancy-flavoured
  thriller narration ("Stone does not know what game he is playing. Stone follows
  the protocol.") crossed with the cosy *Puzzle Adventures* voice ("Can YOU help
  Stone read the board? Look carefully…"). The puzzle-book register secretly
  justifies the whole reader-solves-to-advance format — and makes the reveal land
  twice. **Affectionate genre-pastiche, NOT named references** (no real Clancy/Leigh
  characters or titles — keep it generic & CC0-clean).
- **The mechanic, re-skinned as mission protocol:** the 7-rung ladder = Stone's
  *standing orders*; the check-detection mat = a *threat sweep*; the capture-finder
  = *target acquisition*. (Renames only — same engine as §1–2.)
- **The cold-open premise:** Stone, locked in a back room (a Macau-casino-ish
  high-stakes frame), is passed slips of symbols he can't read; a card in English
  says *follow the rules, pass back a reply, the door opens.* He doesn't know it's
  chess. He doesn't know he's playing — or winning.
- **The reveal (closing fiction):** there was no casino, no bet, no danger. The
  "symbols under the door" were a **kindergarten class's chess project**; the kids
  fed him moves, giggling at the grown-up who insisted on rules instead of just
  *looking at the board.* Understanding was available the whole time — he chose the
  rulebook. (The deeper Chinese-Room cut, as comedy. Funnier the more "elite" Stone
  believes he is.)

---

## 1. The engine: a deterministic priority ladder

Per move, run a fixed checklist; **do the first rule that fires**; STOP. Ties broken
by a fixed rule so the policy is a *pure deterministic function* of the position
(this determinism is what licenses the cover claim — §4).

```
Tie-break convention (whenever a rule yields several moves):
  lowest from-square index, then lowest to-square index. (a1=0 ... h8=63)

1. In check?      -> lowest-indexed legal move that escapes check. STOP.
2. Mate in one?   -> play it. STOP.
3. Can capture?   -> take the highest-value enemy piece (Q>R>B=N>P);
                     ties -> tie-break convention. STOP.
4. Can give check?-> give it (tie-break). STOP.
5. Undeveloped N/B?-> develop the lowest-indexed one to its lowest-indexed
                     legal square. STOP.
6. Can castle?    -> castle (kingside before queenside). STOP.
7. Otherwise      -> push the most-advanced pawn with a legal move;
                     ties -> lowest file. STOP.
```

It hangs pieces constantly (no safety scan — deliberate, see §3), plays like a 1985
toy, and is fully deterministic. That's the point: it is to a real engine what
ELIZA-Lite is to a real chatbot.

---

## 2. The craft is the mats, not the policy

The policy is trivial; the **unavoidable** cost is chess's floor: **legal move
generation + check detection.** You can't play chess without knowing your legal
moves and whether your king is attacked. That is this book's equivalent of ELIZA's
two-anchor mat — the one expensive operation the reader can't escape, so the whole
book's pleasantness rides on making it a fill-in procedure, not arithmetic.

Required worksheets (the real content):
- **Check-detection mat** — a printed starburst from the king: 8 sliding rays +
  knight-jumps; trace each, mark the first piece met. Tells you (a) am I in check,
  (b) for rule 1, does this escape.
- **Capture-finder** — scan your pieces in fixed index order; for each, list enemy
  pieces it attacks; the ladder reads off the highest.
- **Legality check** for a candidate (does it leave my king in check? = re-run the
  check mat from the destination).
- **The ladder card** — always-open (like ELIZA's Spotter), the 7 rules + tie-break.
- **Move-log / board-state sheet** — the pad (RAM): current position, whose move,
  castling rights, the move just played.

De-risk exactly as ELIZA: **build the check-detection mat first** and run one move
by hand. If that single mat is pleasant, the book works; if it's homework, rethink.

---

## 3. The simplicity ⟷ Elo tension (pick the spot deliberately)

Simplicity and strength pull opposite ways. The binding limit is **work per move**
(human working memory + patience), same wall as ELIZA and the same reason full chess
is impossible by hand (real search = hundreds–thousands of evals/move = hours/move).

| Policy | Work per move | Likely Elo |
|---|---|---|
| Random legal mover | legality only (+ a die) | ~450–700, teaches nothing |
| **Ladder, NO safety scan** (§1) | legality + 7-rung checklist | **~600–900, minutes/move** ← target |
| Ladder + "is it defended?" scan | + attacker-scan per candidate | ~1000–1200, but ~10–15 min/move |
| Any real search (≥2-ply) | hundreds of evals/move | higher, but hours/move — NOT a book |

**Target = the no-safety-scan ladder.** Least work that still plays purposeful legal
chess, and its Elo is honestly measurable. Add the safety scan only if strength is
judged worth the operating pain — but the title wants *simplest*, so hold the line.

---

## 4. The cover claim — measurement, not assertion

An Elo is **measured, never claimed.** To print "Elo ~XXX" honestly:

1. Specify the ladder + tie-breaks **exactly** (done above — must be unambiguous).
2. **Implement the identical rules in code.**
3. Play the code engine a few thousand games vs a **calibrated reference ladder**
   (e.g. Lichess/maia or Stockfish at fixed low levels; include the random-mover as
   a baseline anchor).
4. The Elo that falls out is the number on the cover.

**Why the claim is airtight:** the policy is a pure deterministic function, so the
code is provably the *same function* as the book. The code's measured Elo **is** the
book's Elo — an identity, not an estimate. Determinism is what makes the cover line a
fact. And the number being *low* (~700) is a feature: an honest, funny, on-brand
cover line, and the whole point is measurability, not strength.

> NB: this is the one GCU book whose central claim REQUIRES running an experiment
> before it can ship. No tournament, no Elo, no honest cover. Build = author the
> ladder/mats AND run the calibration tournament.

---

## 5. The Comprehension Zero series

| № | Book | You become | Hollowness is… |
|---|---|---|---|
| 2 | **The Paper Therapist** (`ELIZA_SPEC.md`) | a chatbot | *inferred* (you feel it) |
| **1** | **the chess book** (this) | a game engine | **measured & adversarial** (a scoreboard) |
| (3) | *the parser book (Liberdade — deferred)* | a translator | *experienced* (the seam) |

Chess is the apex: the only one where the Chinese Room has a **rating**. Likely the
flagship of the series. (See the series header near the top.)

---

## 6. Format / production notes

- Mono, likely **A5** (the check-mat + board diagrams want horizontal room; A6 is
  cramped — same finding as ELIZA). Cheap to print, like playback.
- Built on the house: a generator emits the rule cards + mats; `\usepackage{forme}`
  (NOT kit — this is mono/text, not the colour/square Field Kit system); shared
  `fonts/`; the `_TEMPLATE` build convention. Page-count is the only real invariant;
  build sequentially; UTF-8 writes.
- Front matter per `specs/FRONTMATTER.md` (reserve the ficha if registering); the
  measured Elo belongs on the cover AND restated in the colophon with the method
  (N games, reference ladder, code-twin commit hash) so the claim is auditable —
  very GCU (cf. playback printing its own SHA + seed).

---

## 7. Build order (de-risk before committing)

1. **Check-detection mat, one move, by hand.** The make-or-break ergonomics test.
2. Legal-move + capture-finder mats; run a full move end-to-end.
3. Code the exact ladder; unit-test it agrees with the by-hand mats on sample
   positions (the conformance check — ELIZA's 1966-transcript analogue).
4. **Run the calibration tournament** → get the real Elo. (Gate for the cover.)
5. Then author the rule cards, tutorial ("you are now a chess engine"), the
   Searle/Chinese-Room foot-essay + the closing-knife colophon.

Risks, ranked: (1) the mats' ergonomics ARE the product; (2) per-move time must stay
in minutes (hold the no-safety-scan line); (3) the Elo must be genuinely measured,
not guessed — it's the thesis, not a label.

---

*GCU. If built: code MIT, text/figures CC0. Engine shape = reader-as-CPU (ELIZA
family), not reader-as-navigator (playback/Quire family). Not yet built.*

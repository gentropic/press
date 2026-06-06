# PUBLISHING.md — ISBN, ficha, legal deposit, distribution

Posture (like Playback): **CC0 content / MIT code**, biased toward "free and
frictionless to obtain" over revenue. *Not a lawyer; this is the practical map.*

## What's actually required vs. optional

- **The only legal mandate is depósito legal**, not ISBN and not ficha.
- **ISBN** is a voluntary international standard (helps cataloguing/discoverability).
- **Ficha catalográfica** is optional polish (a CIP block on the copyright page).

## ISBN (CBL)

- **CBL** (Câmara Brasileira do Livro) is the **sole** Brazilian ISBN agency since
  March 2020, all online at **cblservicos.org.br**. ~**R$25** each (2023 figure —
  re-check), ~2-day turnaround. Same portal also issues the **barcode (EAN)**,
  **ficha catalográfica**, and copyright registration.
- **One ISBN per language AND per format.** So "both languages" can mean several:
  PT hardcover, PT PDF, EN PDF, etc. Buy only for formats you actually publish.
- **An ISBN encodes nothing physical** — no page count, no size. Changing the page
  count (e.g. adding a ficha) **never** invalidates it; page count lives only in the
  metadata and on the ficha text ("48 p. ; 21 cm").

**Plan:** **one CBL ISBN for the PT hardcover** + a **Zenodo DOI** for the digital
editions (the DOI is the right persistent ID for a free file). e-ISBNs for the PDFs
only if we want them ISBN-catalogued under the GCU imprint.

## Ficha catalográfica

Optional but worth doing (library-grade; helps the deposited copies get shelved).
Get it from **CBL** (bundled with the ISBN) or a registered bibliotecário/CRB.
**Generate it LAST**, after the final page count is locked, because it prints the
page count. It lives **on the copyright page** (verso) — **no new leaf**, so it
doesn't change the page count or touch the ISBN.

- **Field Kit:** a dashed `[ ficha catalográfica — CBL ]` slot is already on the
  copyright verso; drop the real block in once registered.
- **Playback:** ISBN **978-65-02-14290-5** is already registered, and only a **proof
  of one** was printed → still pre-press. Its ficha slots onto the existing copyright
  page (Gardner/Shannon/Conway dedication + edition block) with **no new page** and
  the ISBN unaffected.

## Depósito legal (Lei 10.994/2004)

- Requires depositing **≥1 copy of every publication produced in Brazil** (free **or**
  sold) at the **Biblioteca Nacional** within **30 days**.
- The duty falls on the **printer (Futura)**; editor/author verify. So for the PT run,
  **ask Futura to file it**. Enforcement is loose.
- Trigger = *produced in Brazil + distributed to the public* (money isn't the line).
  The **unprinted EN edition owes nothing**. A purely private manuscript isn't
  "published."
- Foreign-printed works are equated only if they carry a **Brazil-domiciled editor/seller**
  (relevant if a Lulu edition is ever made under the GCU imprint).

## Distribution / channels

- **PT hardcover:** Futura, ~10 copies, hand-delivered (the gift run). Its own ISBN;
  Futura files the depósito legal.
- **EN + PT digital:** free **CC0 PDF** under a **Zenodo DOI**; archive to **Zenodo +
  Internet Archive** (same as Playback's plan).
- **Lulu (optional tail):** Lulu's **free ISBN makes Lulu the publisher of record**
  (imprint locked to "Lulu", ISBN locked to Lulu, requires global distribution). To
  keep the GCU imprint, use **your own ISBN or none + the DOI**. A Bookstore-only free
  listing can't carry a free Lulu ISBN. Treat any Lulu edition as a **re-target**
  (different trim/bleed), regenerated from source — never a re-upload.
- **Web interactive twin:** deferred. Will reuse the seed-7 field (live deposit,
  draggable cutoff, re-seed, #holes). Most "GCU" of the follow-ons.

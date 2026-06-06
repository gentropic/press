#!/usr/bin/env python3
"""THE PAPER THERAPIST — a hand-runnable ELIZA, in a book.
The book is the program; a notepad is RAM; the reader is the CPU.

This is a SCAFFOLD: the engine is encoded so adding a keyword = appending to
KEYWORDS, not writing LaTeX. It currently emits the two fixed reference cards and
one worked page of each of the three keyword TYPES (grab / two-anchor / spot), to
prove the machinery. Fill out the 19-keyword v1 roster (see specs/ELIZA_SPEC.md)
to complete the book. A5 mono; cheap to print, like playback.
"""
import os
FP = os.environ.get("KIT_FONTS", "../../fonts/")
if not FP.endswith("/"): FP += "/"

# ============================================================================
# THE ENGINE AS DATA. Each keyword is one entry. type drives the page layout:
#   "spot"   (blue): keyword present -> canned/cycling reply, no grab.
#   "grab"   (green): grab everything AFTER the anchor word.
#   "two"    (yellow): grab what follows a two-word anchor (the showcase mats).
# 'page' is the printed section number (matches the Spotter card).
# 'templates' cycle (reader ticks leftmost-unused). {g} = the grab, post-swap.
# 'example' = (typed sentence, the grab) for the worked illustration on the page.
# ============================================================================
KEYWORDS = [
  dict(kw="sorry", page=12, type="spot",
       templates=["Please don't apologise.", "Apologies are not necessary here."]),
  dict(kw="I am", page=14, type="two", anchor="I AM",
       templates=["How long have you been {g}?",
                  "Do you believe it is normal to be {g}?",
                  "Do you enjoy being {g}?"],
       example=("i think i am pretty tired today", "pretty tired today")),
  dict(kw="my", page=22, type="grab", anchor="my",
       templates=["Your {g}.", "Why do you say your {g}?",
                  "Does that suggest anything else which belongs to you?"],
       example=("my boyfriend made me come here", "boyfriend made you come here")),
  # ... append the rest of the v1 roster here (specs/ELIZA_SPEC.md):
  #   I feel(grab), I want(two), I think(grab), I can't(two), because(spot),
  #   why(spot), you...me(two), alike(spot), like(two), everyone(spot),
  #   mother->family(spot), dream(spot), computer(spot), always(spot),
  #   yes/no(spot), (none)(fallback).
]

# --- the two always-open cards (printed on the inside covers) ---------------
SPOTTER = [("sorry",12),("I am",14),("I feel",16),("my",22),
           ("you",24),("because",18),("(none)",31)]   # extend with the full roster
SWAP = [r"I / me $\leftrightarrow$ you", r"my $\leftrightarrow$ your",
        r"am $\leftrightarrow$ are", r"myself $\leftrightarrow$ yourself",
        r"I'm $\leftrightarrow$ you're"]

# ============================================================================
PRE = (r"""\documentclass[11pt]{article}
\usepackage[paperwidth=148mm,paperheight=210mm,margin=12mm]{geometry}
\usepackage{fontspec}\usepackage{xcolor}\usepackage{amssymb}\usepackage{graphicx}\usepackage{tikz}
\definecolor{ink}{HTML}{1B2A33}\definecolor{signal}{HTML}{C0392B}
\definecolor{mute}{HTML}{6E727B}\definecolor{paper}{HTML}{FFFFFF}
\setmainfont{Barlow-Regular.ttf}[Path=__FP__,BoldFont=Barlow-Bold.ttf,ItalicFont=Barlow-Italic.ttf]
\newfontfamily\disp{Barlow-Black.ttf}[Path=__FP__]
\newfontfamily\m{SpaceMono-Regular.ttf}[Path=__FP__,BoldFont=SpaceMono-Bold.ttf]
\pagestyle{empty}\setlength{\parindent}{0pt}\color{ink}
\begin{document}
""").replace("__FP__", FP)

def head(k):
    return (r"{\m\small\textbf{KEYWORD}\hfill \textbf{%d}}\\[2pt]"
            r"{\disp\fontsize{28}{30}\selectfont %s}\\[10pt]" % (k["page"], k["kw"].upper()))

def templates_block(tpls, grab=None):
    rows=[]
    for i,t in enumerate(tpls):
        box = r"$\boxtimes$" if (grab and i==0) else r"$\square$"
        filled = t.replace("{g}", (r"\underline{\ %s\ }"%grab) if grab else
                                   r"\underline{\hspace{3cm}}")
        rows.append(r"%s & %s\\[4pt]" % (box, filled))
    return (r"{\m\footnotesize\color{mute}say the next un-ticked line; drop the grab in; tick it.}\\[4pt]"
            r"\begin{tabular}{@{}c@{\ \ }l@{}}%s\end{tabular}\\[10pt]" % "".join(rows))

FOOT = (r"{\m\footnotesize\color{mute}$\star$ copy the grab to a MEMORY line on the pad.\\"
        r"$\triangle$\ doesn't fit cleanly? say ``Tell me more about that.'' and move on.}")

def page_spot(k):
    t0=k["templates"][0]
    return (head(k)
        + r"{\m\footnotesize\color{mute}keyword present --- no grab. say the next un-ticked line.}\\[8pt]"
        + templates_block(k["templates"], grab=None).replace(r"\underline{\hspace{3cm}}","")
        + r"{\large\textbf{Doctor:} ``%s''}\\[10pt]"%t0 + FOOT + r"\clearpage")

def _mat(prefix, anchor, grab, two):
    # solid box = anchor; dashed red box = grab. two-anchor draws prefix before anchor.
    return (r"\begin{tikzpicture}[x=1mm,y=1mm]"
        r"\draw[mute,line width=0.4pt] (0,0) rectangle (124,26);"
        r"\node[anchor=north west,font=\m\scriptsize,text=mute] at (2,24) {MATCH MAT};"
        r"\node[anchor=west,font=\m] at (3,15) {%s};"
        r"\draw[ink,line width=1pt] (28,8) rectangle (52,21);"
        r"\node[anchor=west,font=\m,text=signal] at (30,15) {%s};"
        r"\draw[signal,line width=1pt,dashed] (54,8) rectangle (121,21);"
        # grab auto-fits the 65mm box (grabs vary in length)
        r"\node[anchor=west,inner sep=0pt] at (56,15) {\resizebox{63mm}{!}{\m %s}};"
        r"\node[anchor=north,font=\m\scriptsize,text=mute] at (40,7.5) {anchor};"
        r"\node[anchor=north,font=\m\scriptsize,text=signal] at (87,7.5) {$\Rightarrow$ GRAB};"
        r"\end{tikzpicture}\\[8pt]" % (prefix, anchor, grab))

def page_grabtype(k, two):
    sent, grab = k["example"]
    anchor = k["anchor"]
    # split the example sentence at the anchor for the mat's prefix
    low = sent.lower(); a = anchor.lower()
    pre = sent[:low.index(a)].strip() if a in low else ""
    cue = ("find %s, grab what follows" % (r"\textbf{\color{ink}%s}"%anchor.upper()))
    t0 = k["templates"][0].replace("{g}", grab)
    return (head(k)
        + r"{\m\footnotesize\color{mute}you wrote it on the pad; %s.}\\[8pt]"%cue
        + _mat(pre if pre else r"\dots", anchor.upper(), grab, two)
        + r"{\m write the grab:\ \ \fbox{\strut\ \ %s\ \ }}\\[12pt]"%grab
        + templates_block(k["templates"], grab=grab)
        + r"{\large\textbf{Doctor:} ``%s''}\\[10pt]"%t0 + FOOT + r"\clearpage")

def render(k):
    if k["type"]=="spot": return page_spot(k)
    return page_grabtype(k, two=(k["type"]=="two"))

def cards():
    sp = r"\\ ".join(r"%s\dotfill %d"%(n,p) for n,p in SPOTTER)
    sw = r"\\ ".join(SWAP)
    return (r"{\color{mute}\rule{\linewidth}{0.3pt}}\\[4pt]"
        r"\begin{minipage}[t]{0.46\linewidth}{\m\small\textbf{SPOTTER} (first hit wins)}\\[3pt]"
        r"{\m\scriptsize %s}\end{minipage}\hfill"
        r"\begin{minipage}[t]{0.46\linewidth}{\m\small\textbf{SWAP} (only the grab)}\\[3pt]"
        r"{\m\scriptsize %s}\end{minipage}\clearpage" % (sp, sw))

body = "\n".join(render(k) for k in KEYWORDS) + cards()
open("eliza.tex","w",encoding="utf-8").write(PRE + body + "\n\\end{document}\n")
print("wrote eliza.tex  keyword-pages:", len(KEYWORDS),
      "(roster target: 19 — see specs/ELIZA_SPEC.md)")

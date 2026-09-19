<div align="center">

# Human Writing

**A writing skill for Claude and other assistants.<br>It edits prose so the page reads as one person thinking about one subject for one reader.**

[![Version](https://img.shields.io/badge/version-2.1.0-1f6feb?style=flat-square)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-2ea043?style=flat-square)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude_Code-plugin-d97757?style=flat-square)](#install)
[![Portable](https://img.shields.io/badge/ChatGPT_%7C_Gemini-portable-8250df?style=flat-square)](human-writing/PORTABLE.md)
[![Tools](https://img.shields.io/badge/tools-stdlib_only-3776ab?style=flat-square&logo=python&logoColor=white)](human-writing/scripts)

[Install](#install) · [Use](#use) · [How it works](#how-it-works) · [Quoting](#quoting-a-work-you-supplied) · [Evidence](#the-evidence) · [Files](#whats-in-the-box) · [Limits](#limits)

</div>

---

Most "humanizers" are a list of banned words. That doesn't work. Researchers took
AI-written stories and rewrote every cliché and every bit of purple prose out of them. A
classifier that looked only at *narrative structure* still caught them **93.9%** of the
time, against 95.5% before the edit. Swapping words bought 1.6 points.

So this skill starts at the other end. It checks the facts first, then the shape of the
reasoning, then sentence rhythm, and gets to vocabulary last.

```text
 ┌──────────────┬────────────────────────────────────────────┬──────────────────────────────┐
 │ Layer        │ What it covers                             │ Why it ranks here            │
 ├──────────────┼────────────────────────────────────────────┼──────────────────────────────┤
 │ 0. Facts     │ claims, sources, quotations, numbers       │ Wrong here, nothing counts   │
 │ 1. Structure │ what is chosen, compared, delayed, left    │ Survives paraphrase intact   │
 │ 2. Shape     │ sentence and paragraph rhythm, openings    │ How the page reads aloud     │
 │ 3. Words     │ stock phrases, register, borrowed vocab    │ Cheapest to fix, rots fast   │
 │ 4. Mechanics │ punctuation, formatting, paste artifacts   │ Near-proof when present      │
 └──────────────┴────────────────────────────────────────────┴──────────────────────────────┘
```

## New in 2.1

- **Exact quotations from your sources.** Give it a book or article and ask for an essay,
  and every quotation will match the source letter for letter, followed by (Author, page).
  A new script checks each one against the text.
- **No dashes, semicolons, or colons** in the prose it writes. A sentence has to say how its
  clauses connect instead of leaving a mark to do it.
- **Synced with the sources.** Current Wikipedia *Signs of AI writing* and `blader/humanizer`
  v3.0.0, with a table mapping every pattern onto the catalogue.
- **The research ships with it.** The StoryScope paper and the background report live in
  [`research/`](research/).

Full list in the [changelog](CHANGELOG.md).

## A before and after

This passage came out of a local model with no special instructions. It has one stock
phrase in 484 words, so a word-list tool would call it clean. A blind reviewer still flagged
it as machine-written at 96% confidence, and the scanner shows why.

| | Before | After |
|---|---:|---:|
| Stock phrases | 1 | 0 |
| Sentences of 15 words or fewer | 12% | **33%** |
| Nominalisations per 1k words | 76.5 | **45.1** |
| Paragraph-length spread (SD) | 0.00 | **1.83** |
| Dates, figures, named things | 0 | **4** |

Human news prose runs 32 to 33% short sentences. Instruction-tuned models from 2025 run 1
to 4%. The full write-up, including the rewrite that *failed* review, is in
[`TEST_REPORT.md`](human-writing/TEST_REPORT.md).

## Install

### Claude Code, as a plugin

```text
/plugin marketplace add sahil-baligar/HumanWriting
/plugin install human-writing@human-writing
```

### Claude Code or Claude Desktop, by hand

Copy the `human-writing/` folder into `~/.claude/skills/` for every project, or into
`.claude/skills/` for one. It answers to `/human-writing`.

```bash
git clone https://github.com/sahil-baligar/HumanWriting.git
cp -r HumanWriting/human-writing ~/.claude/skills/
```

### ChatGPT, Gemini, anything else

Paste [`PORTABLE.md`](human-writing/PORTABLE.md) into the system prompt, custom
instructions, or project knowledge. It is one self-contained file.

## Use

```text
Humanise this draft.                          [paste text]
Audit this essay. Do not rewrite.             [paste text]
Rewrite in my voice.                          [paste 3 samples, then the draft]
Draft this from my notes.                     [paste notes]
Write an essay on this novel, with quotes.    [upload the book]
Give me four different openings.
```

Two scripts come with it. Both need Python 3 and nothing else.

```bash
# Measure a draft. It reports and never judges.
python human-writing/scripts/scan.py draft.md
python human-writing/scripts/scan.py --summary a.md b.md     # compare two drafts

# Check every quotation in an essay against its source, including page numbers.
python human-writing/scripts/verify_quotes.py essay.md book.txt --pages
```

The scanner's columns have no target values, with one exception. The `punc` column counts
dashes, semicolons, and colons, and the house rule wants it at zero. Everything else is for
comparing a draft against its own earlier version.

## How it works

**It ranks structure above wording.** Model prose takes the default branch at every fork.
You get the linear causal chain, the tidy resolution, the three-part list, and the paragraph
that ends by restating the thesis. The skill's choice-space method asks what else the writer
could have picked, and picks it on purpose.

**It counts signs of human writing as well as machine writing.** Standard concision advice
says to cut "in order to", delete "very", and swap "is" for a stronger verb. Those exact
constructions are measured signs of human authorship. Following the usual advice pushes
prose toward the machine cluster.

**It corrects four pieces of received advice**, each against a published measurement.

1. Models *under*-use the passive voice. They don't over-use it.
2. Participial clauses are the largest grammatical gap, at 5.3× the human rate.
3. What went missing is short sentences. Long ones were never the problem.
4. No published target for sentence-length variance exists, so the skill doesn't invent one.

**It names the second template.** Over-corrected prose has its own signature. Commentary
about evidence stands where the evidence should be, invented numbers show up as texture, and
an aphorism closes every paragraph. Blind review of this skill's own output turned these up,
and they're catalogued as section H of [`tells.md`](human-writing/references/tells.md).

**It has a substance gate.** A rewrite that says less than the original has failed, however
well it reads.

## Quoting a work you supplied

This is the strictest rule in the skill. When you upload a book, story, article, or
transcript and ask for an essay about it, anything the skill puts in quotation marks is
copied from your text word for word and letter for letter. Spelling, capitals, punctuation,
and even the shape of the apostrophe stay as printed. Each quotation is followed by its
citation.

> The narrator calls the harbour "a grey mouth that swallowed the boats one by one" (Okafor, 42).

If a passage doesn't fit the sentence, the skill quotes a shorter stretch or paraphrases
without quotation marks. It never edits the quotation to fit. If it can't tell which page a
passage is on, it writes `(Okafor, page ?)` and tells you, because an invented page number
is an invented citation.

`verify_quotes.py` enforces this. It fails any quotation that isn't in the source exactly,
lacks a citation, cites the wrong page, or uses a straight apostrophe where the book has a
curly one. The rule in full is in [`quoting.md`](human-writing/references/quoting.md).

## The evidence

Every empirical claim is sourced, dated, and marked with its status in
[`evidence.md`](human-writing/references/evidence.md). That includes a list of widely repeated
figures that could not be traced back to a source and shouldn't be cited. It is also where
the punctuation rule is labelled honestly as house style rather than as a finding.

| Source | What it contributes |
|---|---|
| Russell, Rajendhran, Pham, Iyyer & Wieting, *StoryScope*, COLM 2026 ([PDF](research/StoryScope-Russell-et-al-2026.pdf)) | Structure survives surface edits (93.9% vs 95.5%) |
| Reinhart et al., *Do LLMs write like humans?*, PNAS 2025 | Grammatical gaps, and base models sitting near human rates |
| Kobak, González-Márquez, Horvát & Lause, *Science Advances* 2025 | Vocabulary drift, and why word lists rot |
| Chakrabarty, Laban & Wu, *Can AI writing be salvaged?*, CHI 2025 | Taxonomy of creative-writing artifacts |
| Juzek & Ward, COLING 2025 and BIAS 2025 | Where model-favoured words come from |
| Shaib et al., EMNLP 2024 and AACL 2025 | Syntactic templates and repetition |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Field-tested catalogue from WikiProject AI Cleanup |
| [`blader/humanizer`](https://github.com/blader/humanizer) v3.0.0 (MIT) | The pattern set this skill grew out of |

[`research/README.md`](research/README.md) maps every humanizer pattern and every relevant
Wikipedia section onto this skill's catalogue.

## What's in the box

```text
.
├── .claude-plugin/            plugin and marketplace manifests
├── human-writing/
│   ├── SKILL.md               the core, loaded on every call
│   ├── PORTABLE.md            single-file version for other assistants
│   ├── TEST_REPORT.md         baselines, rewrites, blind review, failures
│   ├── references/
│   │   ├── tells.md           full catalogue with before/after pairs and strength classes
│   │   ├── structure.md       the layer that survives paraphrase, and the choice-space method
│   │   ├── genres.md          what "natural" means per genre
│   │   ├── voice.md           building a voice profile from writing samples
│   │   ├── quoting.md         exact quotations and (Author, page) citations
│   │   └── evidence.md        every claim's source, status, and caveat
│   ├── scripts/
│   │   ├── scan.py            measuring instrument
│   │   └── verify_quotes.py   quotation checker
│   └── tests/                 the before/after corpus behind the report
└── research/
    ├── StoryScope-Russell-et-al-2026.pdf
    ├── deep-research-report.md
    ├── upstream/humanizer-v3.0.0/
    └── README.md              source-to-catalogue mapping
```

## Limits

This improves writing. It doesn't promise that any classifier will call the result human,
and it must not be tuned against one. Human judges perform near chance at this task, and
automated detectors fail under domain shift, paraphrasing, and light editing.

It never fabricates facts, sources, quotations, page numbers, experiences, or deliberate
errors.

For coursework, follow your institution's rules on AI assistance.

<div align="center">
<sub>MIT licensed · built by <a href="https://github.com/sahil-baligar">Sahil Baligar</a></sub>
</div>

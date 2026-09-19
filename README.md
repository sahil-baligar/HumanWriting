<div align="center">

# Human Writing

**A writing skill for Claude and other assistants.<br>It edits prose so the page reads as one person thinking about one subject for one reader.**

[![Version](https://img.shields.io/badge/version-2.0.0-1f6feb?style=flat-square)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-2ea043?style=flat-square)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude_Code-plugin-d97757?style=flat-square)](#install)
[![Portable](https://img.shields.io/badge/ChatGPT_%7C_Gemini-portable-8250df?style=flat-square)](human-writing/PORTABLE.md)
[![Scanner](https://img.shields.io/badge/scanner-stdlib_only-3776ab?style=flat-square&logo=python&logoColor=white)](human-writing/scripts/scan.py)

[Install](#install) · [Use](#use) · [How it works](#how-it-works) · [Evidence](#the-evidence) · [Files](#whats-in-the-box) · [Limits](#limits)

</div>

---

Most "humanizers" are a list of banned words. That doesn't work. When researchers rewrote
every cliché and every bit of purple prose out of AI-generated stories, a classifier that looked
only at *narrative structure* still caught them **93.9%** of the time, against 95.5% before
the edit. Swapping words bought 1.6 points.

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
 │ 4. Mechanics │ typography, formatting, paste artifacts    │ Near-proof when present      │
 └──────────────┴────────────────────────────────────────────┴──────────────────────────────┘
```

## A before and after

The passage below came out of a local model with no special instructions. It has one stock
phrase in 484 words, so a word-list tool would call it clean. A blind reviewer still flagged it
as machine-written at 96% confidence, and the scanner shows why.

| | Before | After |
|---|---:|---:|
| Stock phrases | 1 | 0 |
| Sentences of 15 words or fewer | 12% | **33%** |
| Nominalisations per 1k words | 76.5 | **45.1** |
| Paragraph-length spread (SD) | 0.00 | **1.83** |
| Dates, figures, named things | 0 | **4** |

Human news prose runs 32–33% short sentences. 2025 instruction-tuned models run 1–4%. The
full write-up, including the rewrite that *failed* review, is in
[`TEST_REPORT.md`](human-writing/TEST_REPORT.md).

## Install

### Claude Code, as a plugin

```text
/plugin marketplace add sahil-baligar/HumanWriting
/plugin install human-writing@human-writing
```

### Claude Code or Claude Desktop, by hand

Copy the `human-writing/` folder into `~/.claude/skills/` (every project) or
`.claude/skills/` (one project). It answers to `/human-writing`.

```bash
git clone https://github.com/sahil-baligar/HumanWriting.git
cp -r HumanWriting/human-writing ~/.claude/skills/
```

### ChatGPT, Gemini, anything else

Paste [`PORTABLE.md`](human-writing/PORTABLE.md) into the system prompt, custom
instructions, or project knowledge. It is one self-contained file.

## Use

```text
Humanise this draft.               [paste text]
Audit this essay. Do not rewrite.  [paste text]
Rewrite in my voice.               [paste 3 samples, then the draft]
Draft this from my notes.          [paste notes]
Give me four different openings.
```

The scanner measures a draft and doesn't try to judge it. It needs Python 3 and nothing else.

```bash
python human-writing/scripts/scan.py draft.md              # full report
python human-writing/scripts/scan.py --summary a.md b.md   # compare two drafts
python human-writing/scripts/scan.py --json draft.md       # raw counts
```

No column has a target value. Compare a draft against its own earlier version rather than
chasing numbers.

## How it works

**It ranks structure above wording.** Model prose takes the default branch at every fork:
the linear causal chain, the tidy resolution, the three-part list, the paragraph that ends by
restating the thesis. The skill's choice-space method asks what else the writer could have
picked, and picks it on purpose.

**It counts signs of human writing as well as machine writing.** Standard concision advice
says to cut "in order to", delete "very", and swap "is" for a stronger verb. Those exact
constructions are measured signs of human authorship. Following the usual advice pushes
prose toward the machine cluster.

**It corrects four pieces of received advice**, each against a published measurement:

1. Models *under*-use the passive voice. They don't over-use it.
2. Participial clauses are the largest grammatical gap, at 5.3× the human rate.
3. What went missing is short sentences. Long ones were never the problem.
4. No published target for sentence-length variance exists, so the skill doesn't invent one.

**It names the second template.** Over-corrected prose has its own signature: commentary
about evidence where the evidence should be, invented numbers used as texture, an aphorism
closing every paragraph. Blind review of this skill's own output turned these up, and
they're catalogued as section H of [`tells.md`](human-writing/references/tells.md).

**It has a substance gate.** A rewrite that says less than the original has failed, however
well it reads.

## The evidence

Every empirical claim is sourced, dated, and marked with its status in
[`evidence.md`](human-writing/references/evidence.md). That includes a list of widely repeated
figures that could not be traced back to a source and shouldn't be cited.

| Source | What it contributes |
|---|---|
| Russell, Rajendhran, Pham, Iyyer & Wieting, *StoryScope*, COLM 2026 | Structure survives surface edits (93.9% vs 95.5%) |
| Reinhart et al., *Do LLMs write like humans?*, PNAS 2025 | Grammatical gaps; base models sit near human rates |
| Kobak, González-Márquez, Horvát & Lause, *Science Advances* 2025 | Vocabulary drift, and why word lists rot |
| Chakrabarty, Laban & Wu, *Can AI writing be salvaged?*, CHI 2025 | Taxonomy of creative-writing artifacts |
| Juzek & Ward, COLING 2025 and BIAS 2025 | Where model-favoured words come from |
| Shaib et al., EMNLP 2024 and AACL 2025 | Syntactic templates and repetition |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Field-tested catalogue from WikiProject AI Cleanup |
| [`blader/humanizer`](https://github.com/blader/humanizer) v3.0.0 (MIT) | Pattern set this skill grew out of |

## What's in the box

```text
.
├── .claude-plugin/          plugin + marketplace manifests
└── human-writing/
    ├── SKILL.md             the core, loaded on every call (under 400 lines)
    ├── PORTABLE.md          single-file version for other assistants
    ├── TEST_REPORT.md       baselines, rewrites, blind review, failures
    ├── references/
    │   ├── tells.md         full catalogue with before/after pairs and strength classes
    │   ├── structure.md     the layer that survives paraphrase; choice-space method
    │   ├── genres.md        what "natural" means per genre
    │   ├── voice.md         building a voice profile from writing samples
    │   └── evidence.md      every claim's source, status, and caveat
    ├── scripts/scan.py      measuring instrument, stdlib only
    └── tests/               the before/after corpus behind the report
```

## Limits

This improves writing. It doesn't promise that any classifier will call the result human, and
it must not be tuned against one. Human judges perform near chance at this task, and automated
detectors fail under domain shift, paraphrasing, and light editing.

It never fabricates facts, sources, quotations, experiences, or deliberate errors.

For coursework, follow your institution's rules on AI assistance.

<div align="center">
<sub>MIT licensed · built by <a href="https://github.com/sahil-baligar">Sahil Baligar</a></sub>
</div>

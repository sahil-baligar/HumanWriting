# Research

The material the skill is built from, kept next to it so every rule can be traced back to a
source.

| File | What it is | License |
|---|---|---|
| [`StoryScope-Russell-et-al-2026.pdf`](StoryScope-Russell-et-al-2026.pdf) | Russell, Rajendhran, Pham, Iyyer & Wieting. *StoryScope: Investigating idiosyncrasies in AI fiction.* COLM 2026. [arXiv:2604.03136v6](https://arxiv.org/abs/2604.03136) | CC0 |
| [`deep-research-report.md`](deep-research-report.md) | The literature review written while planning v2.0.0 | MIT, with this repo |
| [`upstream/humanizer-v3.0.0/`](upstream/humanizer-v3.0.0/) | `SKILL.md` and `README.md` from [`blader/humanizer`](https://github.com/blader/humanizer) v3.0.0, commit `9862685` | MIT, © 2025 Siqi Chen |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1374941330) | Linked rather than copied. Revision 1374941330, 14 September 2026 | CC BY-SA 4.0 |

Full citations for everything else (Reinhart et al., Kobak et al., Chakrabarty et al.,
Juzek & Ward, Shaib et al., Freeburg, Terčon & Dobrovoljc), with their numbers, status, and
caveats, are in [`human-writing/references/evidence.md`](../human-writing/references/evidence.md).

## What the StoryScope paper contributes

The paper extracts discourse-level features from 61,608 stories (who narrates, how time
moves, whether the theme is stated or implied, how endings resolve) and trains classifiers
on those features alone. Two results carry the skill.

1. **Structure identifies AI fiction without any help from wording.** Narrative features
   alone separate human from AI stories at 93.2% macro-F1.
2. **Surface editing hardly touches it.** After every cliché and piece of purple prose was
   rewritten out of Gemini's stories, the structural classifier still reached 93.9%, against
   95.5% before. That 1.6-point gap is why the skill fixes structure before wording.

The per-feature gaps (explicit themes, linear causal chains, tidy resolutions, sensory
detail handled as decoration) became the discourse checks in
[`structure.md`](../human-writing/references/structure.md). The paper measured fiction, so
the skill marks those figures *fiction-only* and does not carry them over to other genres
as numbers.

## How humanizer v3.0.0 maps onto the catalogue

Every one of humanizer's 25 patterns has a home in
[`tells.md`](../human-writing/references/tells.md). Where the two disagree, the reason is
given.

| humanizer v3.0.0 | Here | Notes |
|---|---|---|
| 1 Not X but Y | B1 | Four shapes, including the reversed *Y rather than X* |
| 2 One-line closers | B2 | |
| 3 Sayings that sound deep | B3 | |
| 4 Staged run-up | B4 | |
| 5 Arguing with no one | B5 | Also H5, the over-corrected version |
| 6 Forced triads | D1 | |
| 7 Repeated sentence openings | D2 | |
| 8 Dashes as the universal connector | E9 | Now a house rule: no dashes in output |
| 9 Stacked qualifiers | C10 | |
| 10 Hyphenated pairs | F | Weak alone |
| 11 Passive voice and missing subjects | F | Models *under*-use the passive. See evidence.md |
| 12 Overused AI words | Layer 3, `scan.py` VOCAB | Grouped by era, because the lists rot |
| 13 Inflated significance | C1 | |
| 14 Vague connection | C5 | |
| 15 Shallow -ing riders | C3 | The largest measured grammatical gap, 5.3× |
| 16 Sales language | C6 | |
| 17 Borrowed authority | C4 | |
| 18 Avoiding is, are, has | C7 | |
| 19 Bold as decoration | E1 | |
| 20 Decorative headings | E2 | |
| 21 Curly quotation marks | F | The tell is mixing, not curliness |
| 22 Chatbot residue | A2 | |
| 23 Knowledge-limit disclaimers | A3 | |
| 24 Heading repeated in first sentence | E3 | |
| 25 Writing about the previous version | E6 | E7 adds the edit-summary form |

What this skill adds on top of humanizer: the structure layer and choice-space method, genre
targets, voice profiling, the second template (section H), the substance gate, counts of
human signals to protect, the scanner, the quotation verifier, and the evidence registry.

## How the Wikipedia page maps onto the catalogue

| Wikipedia section | Here |
|---|---|
| Undue emphasis on significance, legacy, broader trends | C1 |
| Canned emphasis on notability, attribution, media coverage | C4 |
| Superficial analyses | C3 |
| Promotional language | C6 |
| Vague attributions, overgeneralisation | C4, C8 |
| Outline-like conclusions about challenges and prospects | C2 |
| Leads treating titles as proper nouns | E8 |
| AI vocabulary | Layer 3, `scan.py` |
| Avoidance of basic copulatives | C7 |
| Vague connection or association | C5 |
| Negative parallelisms, including *Y rather than X* | B1 |
| Rule of three | D1 |
| Title case, boldface, inline-header lists, emoji, tables, heading levels | E1 to E4, `scan.py` formatting |
| Overuse of em dashes | F (audit), E9 (house rule for output) |
| Curly quotation marks | F |
| Collaborative communication | A2 |
| Knowledge-cutoff disclaimers and speculation | A3 |
| Phrasal templates and placeholder text | A1, `scan.py` placeholders |
| Markup bugs (ChatGPT, Gemini, Grok, DeepSeek, Perplexity) | A1, `scan.py` artifacts |
| Broken citations, invalid DOIs and ISBNs | A4 |
| Edit summaries that report what was preserved or avoided | E7 |
| Signs of human writing | SKILL.md "Do not over-tighten", G |
| Ineffective indicators | G |
| Historical indicators | G, and *Retired* in evidence.md |

Sections specific to Wikipedia's own markup and process (broken wikitext, non-existent
categories and templates, AfC submission statements, user pages) are left out. They do not
apply to prose written anywhere else.

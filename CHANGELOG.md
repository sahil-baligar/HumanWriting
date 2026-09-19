# Changelog

## 2.1.0

**Quoting a supplied work.** When the writer supplies a book, article, or other text and
asks for an essay drawing on it, everything in quotation marks must match the source word
for word and letter for letter, followed by (Author, page). No page is ever guessed.
- `references/quoting.md`: the full rule and its edge cases.
- `scripts/verify_quotes.py`: checks each quotation against the source text and flags
  anything not found, uncited, cited to the wrong page, or with the wrong apostrophe.

**Punctuation house rule.** No em dashes, no en dashes, no hyphens standing in for dashes.
Semicolons and colons avoided in prose. Quotations keep their source's punctuation.
- New section in SKILL.md and PORTABLE.md, and tells entry E9.
- `scan.py` reports each break with its sentence and adds a `punc` column to `--summary`.
- `evidence.md` records that this is house style and that the evidence does not support it
  as a detection measure.

**Sources synced** to Wikipedia:Signs of AI writing revision 1374941330 (14 September
2026) and `blader/humanizer` v3.0.0 at commit `9862685`.
- New tells: E7 (edit notes that report what was preserved or avoided) and E8 (a title
  introduced as if it were a thing). Historical indicators added to G.
- Scanner: procedural-summary and *refers to* lead patterns, humanizer's *quietly* and
  *deep dive*.

**Research folder.** `research/` now holds the StoryScope paper (CC0), the background
research report, humanizer v3.0.0's skill with its license, and tables mapping every
humanizer pattern and every relevant Wikipedia section onto the catalogue.

## 2.0.0

- Four-layer model covering facts, structure, shape, words, and mechanics, fixed in that order.
- `references/structure.md` with the choice-space method for the layer that survives paraphrase.
- Section H of `tells.md`, the second template, found by blind review of the skill's own output.
- Substance gate. A rewrite that says less than its original has failed.
- `scripts/scan.py`, a stdlib-only measuring instrument with `--summary` and `--json`.
- `PORTABLE.md`, a single-file version for ChatGPT, Gemini, and other assistants.
- Claude Code plugin and marketplace manifests.

## 1.0.0

- First release with a tells catalogue, genre profiles, voice samples, and a StoryScope discourse pass.

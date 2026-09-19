# Human writing

A skill for writing and editing prose so it reads as one person thinking about one subject
for one reader, instead of a model producing the safest version of the assignment.

It is not a banned-word list, and it makes no claim about AI detectors.

## What is here

| File | Purpose |
|---|---|
| `SKILL.md` | The core. Loaded on every invocation. Under 400 lines. |
| `PORTABLE.md` | Self-contained single file for ChatGPT, Gemini, or any assistant without file loading. |
| `references/tells.md` | The full catalogue, with before-and-after pairs and strength classes. |
| `references/structure.md` | The layer that survives paraphrase. The choice-space method. |
| `references/genres.md` | Register targets. What "natural" means per genre. |
| `references/voice.md` | Building a voice profile from a writer's samples. |
| `references/evidence.md` | Every claim's source, status, and honest caveat. |
| `scripts/scan.py` | A measuring instrument. Stdlib only, no dependencies. |
| `tests/` | The before-and-after corpus behind `TEST_REPORT.md`. |

## Install

**Claude Code or Claude Desktop.** Copy the `human-writing` directory into
`~/.claude/skills/` for personal use, or `.claude/skills/` inside a project. It answers to
`/human-writing`.

**ChatGPT, Gemini, or anything else.** Paste `PORTABLE.md` into the system prompt, custom
instructions, or a project's knowledge. It refers to no other file.

**Any agent that reads Markdown skills.** Point it at `SKILL.md`.

## Use

```
Humanise this draft.               [paste text]
Audit this essay. Do not rewrite.  [paste text]
Rewrite in my voice.               [paste 3 samples, then the draft]
Draft this from my notes.          [paste notes]
Give me four different openings.
```

Run the scanner directly for a measurement:

```bash
python scripts/scan.py draft.md              # full report
python scripts/scan.py --summary a.md b.md   # compare drafts
python scripts/scan.py --json draft.md       # raw counts
```

The scanner reports and never decides. Its `--summary` columns have no target values; they
exist so you can compare a draft against its own earlier version.

Note that it has no quote-awareness. Running it over a document that *discusses* stock
phrases, such as this skill's own reference files, produces a high count by design.

## What makes it different

**Structure is ranked above wording, for a measured reason.** When researchers stripped every
surface artifact out of AI-generated stories, a classifier using only structural features
still identified them at 93.9%, against 95.5% before the edit. Rewriting the prose bought 1.6
points. Word-level humanising does almost nothing on its own.

**It counts signals of human writing, not just machine writing.** Standard concision advice
tells you to cut "in order to," delete "very," and replace "is" with a stronger verb. Those
exact constructions are documented as signs of human authorship. Following the usual advice
moves prose toward the machine cluster.

**It corrects four pieces of received advice**, each against a published measurement: passive
voice is under-used by models rather than over-used; participial clauses are the largest
grammatical gap; short sentences are what actually went missing; and no published target for
sentence-length variance exists.

**It names the second template.** Over-corrected prose has its own signature — substance
replaced by commentary about evidence, invented numbers used as texture, an aphorism at the
end of every paragraph. These were found by blind review of this skill's own output and are
documented in `references/tells.md`.

**It carries a substance gate.** A rewrite that is less informative than its original is a
failed rewrite, however well it reads.

**Every empirical claim is sourced, dated, and status-marked** in `references/evidence.md`,
including a list of widely repeated figures that could not be traced and should not be
cited.

## Sources

- Wikipedia:Signs of AI writing, maintained by WikiProject AI Cleanup
- Russell, Rajendhran, Pham, Iyyer & Wieting, *StoryScope*, COLM 2026
- Reinhart et al., *Do LLMs write like humans?*, PNAS 2025
- Kobak, González-Márquez, Horvát & Lause, *Science Advances* 2025
- Chakrabarty, Laban & Wu, *Can AI writing be salvaged?*, CHI 2025
- Juzek & Ward, COLING 2025 and BIAS 2025
- Shaib et al., EMNLP 2024 and AACL 2025
- `blader/humanizer` v3.0.0 (MIT)

Full citations, numbers, and caveats in `references/evidence.md`.

## Limits

This improves writing. It does not promise that any classifier will call the result human,
and it must not be tuned against one. Human judges perform near chance at this task, and
automated detectors fail under domain shift, paraphrasing, and light editing.

For coursework, follow your institution's rules on AI assistance.

MIT licensed.

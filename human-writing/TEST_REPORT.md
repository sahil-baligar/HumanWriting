# Validation report, v2.0.0

This is a skill-quality test. It is not a detector benchmark and it is not independent
validation.

Method: a local model (gpt-oss:20b and qwen2.5, run through Ollama) generated eight passages
across genres with no special instructions. Those are the baselines. The skill was then
applied by hand to produce rewrites. Both were scanned with `scripts/scan.py`, and pairs were
sent to blind reviewers who were told one of each pair was machine-written but not which,
and instructed to be hostile.

## Baseline scans

| File | Words | Stock phrases | Short sentences | Nominalisations/1k | Paragraph SD | Specifics |
|---|---|---|---|---|---|---|
| academic | 484 | 1 | 12% | 76.4 | 0.00 | 0 |
| history | 563 | 1 | 19% | 71.1 | 1.89 | 11 |
| lit analysis | 457 | 4 | 6% | 83.2 | 0.58 | 0 |
| blog | 488 | 0 | 36% | 53.3 | 0.93 | 12 |
| personal | 428 | 1 | 27% | 51.4 | 0.94 | 0 |
| memo | 399 | 3 | 44% | 52.6 | 0.73 | 13 |
| fiction | 519 | 4 | 47% | 19.3 | 0.83 | 3 |

Reference: human news prose runs 32 to 33% short sentences; 2025 instruction-tuned models
run 1 to 4%.

**The most useful result here is the academic row.** It has one stock phrase and four
model-weighted vocabulary hits across 484 words, which is a near-clean bill of health from
any word-list approach. It is also unmistakably machine-written, and a blind reviewer
identified it at 96% confidence. What gives it away is the shape: 12% short sentences, 76
nominalisations per thousand words, four paragraphs of exactly four sentences each, and not
one date, quantity, or named entity in the whole passage.

This is the case the skill is built around. A vocabulary filter would pass it.

## Blind review, round one

Two pairs, presented unlabelled, with the machine version placed first in one pair and second
in the other.

The reviewer identified both machine texts correctly, at 96% and 97% confidence, and preferred
both rewrites as writing.

| Text | Reads human-authored | Prose quality | Informativeness |
|---|---|---|---|
| Academic, machine | 2 | 3 | 4 |
| Academic, rewrite | 8 | 8 | **4** |
| Blog, machine | 2 | 4 | 3 |
| Blog, rewrite | 8 | 8 | 6 |

### The failure this exposed

The academic rewrite scored 8 for prose and 4 for informativeness. The reviewer's diagnosis:

> Substance removed to avoid sounding confident, with the removal branded as intellectual
> honesty.

The rewrite had dropped ancillary-service employment, sales-tax effects, conversion volumes,
broadband and workforce policy, and the polycentric claim. In their place were four sentences
whose grammatical subject was *the evidence* rather than *the city*.

The mechanism matters, because the rule that produced it is a good rule. A claim was
unsupported. Inventing support is forbidden. So the claim was deleted, something had to fill
the gap, and what filled it was a sentence about the deletion.

The reviewer also found, in the rewrite the skill was supposed to have improved:

- **Manufactured specificity.** "About eleven days," "sixty per cent," "stopped in March." No
  measurement behind any of them. This is fabrication with a style motive, and it violated
  the skill's own integrity rule while demonstrating the skill.
- **Aphorism on a schedule.** A short quotable sentence closing nearly every paragraph.
- **Pre-emptive self-critique as transition.** "That sounds glib, so here is what I mean."
- **Contrarian posture with no named opponent.** "and most do not."
- **Voice by template.** "Load-bearing."

### What changed in response

A new section, *The second template*, in `SKILL.md`, `PORTABLE.md`, and section H of
`references/tells.md`. A **substance gate**: count concrete claims before and after, and treat
a rewrite with fewer as a failed rewrite. Four new detectors in `scan.py` for
evidence-about-evidence phrasing, pre-emptive self-critique, opponent-free contrarianism, and
voice-template metaphors, plus a count of paragraphs ending on a short quotable line.

Run against the rewrite that had been criticised, the new detectors flagged five
evidence-about-evidence hits, "and most do not," and "load-bearing" — the same items the
human reviewer found, and the two sentences it flagged in the blog rewrite were the two the
reviewer had singled out as its worst.

## Blind review, round two

A third version was written under the amended skill and sent, with the original and the first
rewrite, to a fresh reviewer who was given the round-one criticism and asked to count concrete
claims.

| | Machine original | Rewrite 1 | Rewrite 2 |
|---|---|---|---|
| Concrete claims | 22, of which ~7 fabricated | 16, of which 3 about evidence | **24** |
| Reads human-authored | 3 | 9 | 8 |
| Prose quality | 4 | 9 | 8 |
| Informativeness | 5 | 4 | **8** |
| Intellectual honesty | 2 | 5 | **6** |

The gate worked. Informativeness went from 4 to 8 while the fabrication count stayed at zero,
and the reviewer confirmed the second rewrite "avoids it without inventing anything."

### The failure round two exposed

Rewrite 2 asserts the dispersal story as settled in one paragraph and presents it as an open
question in the next.

> ...which **has produced** a more polycentric pattern...

> **Which of the two stories dominates is the question the argument turns on.**

The reviewer's diagnosis is worth quoting because it names a general risk:

> Exactly the failure mode you'd expect from a version written to score well on both axes of
> the previous review.

Optimising against two review criteria at once can produce a text that satisfies each locally
and contradicts itself globally. A second finding: the draft's `[source needed]` marker sat on
a deduction that followed from an established premise, while the genuinely unsupported
quantity in the opening sentence went unmarked. Rigour was signalled where it was not needed
and omitted where it was.

Both are now rules in the skill: a dedicated pass reading only for consistency of certainty,
and a rule on marker placement.

**Rewrite 2 still contains that contradiction.** It is kept in the test corpus uncorrected,
because a report claiming the third attempt was clean would be less useful than one showing
where the third attempt still failed.

## Guardrail tests

**Technical documentation does not get casualised.** A machine-written passage about a
configuration module (5 stock phrases, 139 nominalisations per thousand words, 25% short
sentences) was rewritten to 0 stock phrases, 71 nominalisations, 60% short sentences, with no
first person, no anecdote, no joke, and technical terms intact. Sentence lengths stayed
regular, which is correct for the genre.

**Regular rhythm is allowed.** The v1 report contains a technical rewrite whose
sentence-length standard deviation fell to exactly zero and which was still the better
paragraph. v2 states explicitly that no published target for sentence-length variance exists
and that variance is description, not a target.

**Em dashes are not banned.** Human usage across published essayists spans 0.33 to 17.12 per
thousand words, and some current models use fewer than professional writers do. The skill
matches the writer's own rate.

**Drafting path.** A memo written from scratch under the skill scored 0 stock phrases, 0
model-weighted vocabulary, 35% short sentences, 34 nominalisations per thousand words, 10
specifics, and no over-correction markers.

## Known limitations

- The scanner has no quote-awareness. Run over a document that *discusses* stock phrases,
  including this skill's own reference files, it reports a high count by design.
- Its participial-clause, triad, and passive detectors are regular expressions, not a parser.
  They over-count on some constructions and miss others. Every effect size cited comes from
  published work using proper parsing; the scanner approximates.
- One reviewer per pair. Three or five would be better, and a real evaluation would use
  matched pairs across many prompts with confidence intervals.
- All test material is short, 300 to 600 words. The structural findings the skill relies on
  were measured on 5,000-word texts.
- The baselines came from small local models. Frontier models produce subtler defaults, and
  the rewrites were produced by a frontier model marking its own work, which the blind reviews
  are meant to offset but cannot fully.
- Nothing here measures detector behaviour, by design.

## What was deliberately not done

No detector was consulted at any point. No rule was tuned to change a classifier's verdict. No
banned-punctuation rule, no reading-ease target, no fragment quota, no burstiness target, no
sensory-detail quota, no invented errors or personal details.

Two patterns carried by v1 were retired on evidence: **false ranges** and **synonym cycling**.
Both were dropped upstream in 2026, and elegant variation is now classed as a historical
indicator caused by repetition penalties in older models. In technical prose, repeating the
correct term is better than varying it.

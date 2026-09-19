# Voice

A voice profile is a distribution, not a template. It describes what the writer tends to do,
with how much spread, and it does not require them to do it every time.

## Getting samples

Three or more pieces, ideally in the genre being edited or a nearby one. More is better,
but four good samples beat twenty scraped from anywhere.

Do not build a profile from AI-generated or AI-edited text unless the writer says it
represents the style they want. A profile built from machine prose reproduces machine prose,
and does it under the writer's name.

Ask which samples the writer actually likes. People often submit their most formal work and
mean their most natural.

## What to record

### Sentences

Median length and the spread around it. How often they write something under fifteen words.
Whether they use fragments and where. Whether the main clause tends to arrive early or late.
Whether they subordinate or coordinate.

Run `scripts/scan.py` over the samples and over the draft, then compare. The comparison is
the point; the absolute numbers mean little on their own.

### Paragraphs

Typical length. Whether paragraphs open with the claim, with context, with an example, or
with a transition. Whether one-sentence paragraphs appear. What paragraphs tend to end on.

### Diction

Level of formality. Verbs and nouns that recur. Discipline-specific terms they use without
explaining. Contractions. Slang. Intensifiers. Words they visibly avoid. Whether they are
comfortable with `is`, `has`, `shows`, `uses`.

Do not replace precise technical language because it reads as formal.

### Punctuation

Commas, semicolons, colons, parentheses, em dashes, ellipses, quotation style. Record the
actual rate, not an impression.

This is where general rules most often collide with real habits. A writer who uses six em
dashes per thousand words uses em dashes. Match the rate; do not correct it.

### Rhetorical habits

Directness. How much they signpost. Rhetorical questions. First person. Parenthetical
asides. Self-correction. Humour, and what kind. Concession. Analogy. Anecdote. Whether they
state uncertainty or imply it.

### Source handling, for academic writers

Whether they introduce an author before quoting or lead with the claim and cite at the end.
Whether they compare sources within a paragraph. Whether they quote or paraphrase. Whether
they use first person in analysis.

## Do not overfit

If three samples all open with "In this essay," that is probably an assignment convention,
not a preference. Separate what the writer chose from what the format required.

A profile should describe a range. "Sentences from 8 to 40 words, median 19, and they use a
short one to land a point" is a profile. "Sentences of 19 words" is a cage.

## When rules conflict with the writer

The sample wins, with three exceptions.

1. **Integrity.** A fabricated source is a fabricated source regardless of style.
2. **Model residue.** If the sample is AI-assisted and contains assistant residue or paste
   artifacts, those are not the writer's habits.
3. **Genre requirements the writer is getting wrong.** If the assignment requires a citation
   style and the samples ignore it, the assignment wins. Say so rather than silently
   overriding.

Everywhere else, when a general rule in this skill collides with a habit visible in the
samples, follow the samples and say which rule you set aside and why. A writer is entitled
to their tics.

## Writing the profile

Keep it short enough to reuse. Something like:

```
VOICE: [name], from 4 samples (2 essays, 1 review, 1 blog post)

Sentences   median 19, range 6-44; ~20% under 15 words; occasional fragments for emphasis
Paragraphs  4-6 sentences; usually open with the claim; often end on a complication
Diction     plain Anglo-Saxon verbs; comfortable with "is"; avoids "utilise", "leverage"
Punctuation heavy comma user; em dashes ~5/1000w; no semicolons anywhere
Habits      concedes early, then narrows; dry asides in parentheses; no rhetorical questions
Sources     names the author in the sentence, cites at the end
Avoid       exclamation marks, second person, headings in short pieces
```

Store it and reuse it. Update it when the writer supplies newer work, and prefer newer
samples when they conflict with older ones.

## Without a sample

Take the register from the genre, in `references/genres.md`, and keep the general rules.
Then say plainly that no sample was available, so the result is a competent version of the
genre rather than a match to anyone's voice. Offer to build a profile if the writer can
supply three pieces.

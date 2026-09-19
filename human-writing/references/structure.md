# Structure

The layer that survives paraphrase. Read this before drafting, and whenever a draft still
reads as generic after the wording has been fixed.

## Why this comes first

Researchers took AI-generated stories and ran a span-level rewriting pass over them,
targeting seven categories of surface artifact: cliché, purple prose, redundant exposition,
and similar, using few-shot examples from professional writers. Then they tested a
classifier that had never seen a single stylistic feature, only structural narrative
choices.

| Text | Detected as AI |
|---|---|
| Original AI stories | 95.5% |
| After removing every surface artifact | 93.9% |

Rewriting the prose bought 1.6 points. The shape of the reasoning did not move, because
the rewriter never touched it.

The same study found that human-written stories sit in a wider, sparser region of
structural space than AI ones, which cluster tightly together. Mean distance between the
human centroid and any AI centroid was 1.6 times the mean distance between two AI
centroids. Even the closest human-AI pair was farther apart than the most distant AI-AI
pair. Human writing was not different in one fixed direction. It was more spread out.

That last point is the whole method. The goal is not to invert the defaults. It is to stop
taking the default at every fork.

## The choice-space method

At each structural decision, a model takes the modal branch. Do this instead:

1. **Name the fork.** "How does this section end?" "In what order does the evidence
   arrive?" "Does the reader get told this or work it out?"
2. **List what the material actually permits.** Three to five options. Not hypothetical
   ones, the ones this material supports.
3. **Notice the default.** It is the option you would write without deliberating. Name it
   so you can see it.
4. **Choose on the merits of this material.** Not to avoid the default.
5. **Take the default when it is right.** Then check that you are not about to take it
   again at the next fork. Taking it every single time is the tell, not taking it once.

Two paragraphs written by the same person about the same subject rarely resolve the same
way, because the material differs. Two paragraphs from a model usually do, because the
prior dominates.

### The forks worth naming, for expository and argumentative writing

- **Where the piece starts.** A precise problem, a concrete case, a definition the argument
  needs, a disagreement in the sources, the claim itself, or context. The default is the
  broad-importance funnel; it is almost never the best option.
- **What arrives second.** Elaboration of the opening, the complication, the first
  evidence, or the scope limit.
- **Order of evidence.** Strongest first, chronological, grouped by source, organised
  around the objection, or built so each piece needs the one before it.
- **Where qualification sits.** Early, and it frames the claim. Late, and it concedes.
  Absent, and the piece overclaims. All three are legitimate; the default is one hedge per
  paragraph, which is none of them.
- **How much the reader is told.** Every inference stated, or some left for the reader.
  Academic writing is explicit by convention, but not every sentence needs its moral drawn.
- **Whether the counterargument does anything.** If addressing it does not change the
  thesis, its scope, or its confidence, it is decoration.
- **How the piece ends.** The strongest implication, a bounded limitation, a concrete
  recommendation, the question left open, the opening case now read differently, or simply
  the last necessary fact. The default is summary plus optimism.
- **How many parts the explanation has.** However many the content has. Not three.
- **What each paragraph ends on.** Evidence, analysis, a complication, or a turn into the
  next paragraph. If every paragraph ends by restating the thesis, the piece has one
  paragraph written many times.

### For narrative and fiction

- **Where the story enters.** In the middle of an event, before it, long after, or at the
  wrong moment on purpose.
- **How a character first appears.** External description is the model default. Action,
  dialogue, another character's report, or their own thought are all available.
- **How emotion reaches the reader.** Naming the feeling, a bodily metaphor, behaviour, or
  leaving it ambiguous. Bodily metaphor is heavily the model default.
- **What causes the ending.** The protagonist's choice, external events, both, or nothing
  in particular.
- **Whether it resolves.** Internal acceptance is the model default. External resolution
  and no resolution are both available.
- **How time runs.** Straight through, or not.
- **Whether anything else is going on.** A second thread that rhymes with the first, one
  that contradicts it, one that is simply also happening, or none.
- **Whether the narrator knows there is a reader.**

## Mapping the piece

Write one line per paragraph naming its job. Then read the list, not the prose.

```
P1  frames the policy question
P2  first study, with its finding
P3  says P2 again in broader words      -> merge
P4  privacy concern, unconnected to P2
P5  objection nobody holds              -> replace with the real tension in P4
P6  restates the thesis                 -> the conclusion has no work to do
```

Now ask:

1. Which paragraph carries the most specific reasoning? Is it buried?
2. Which paragraphs restate the assignment rather than answering it?
3. Where does the text get too neat?
4. Where does it explain what the reader has already understood?
5. Do all the claims point the same way? Should they?
6. Is there a real tension, limitation, exception, or competing explanation already sitting
   in the material, unused?
7. Are sources evidence, or decoration?
8. Does the conclusion follow from the argument, or summarise it?
9. Does every paragraph use the same reasoning move?

Paragraphs can define, distinguish, present evidence, explain a mechanism, compare two
sources, test an exception, read a quotation closely, answer a real objection, narrow a
claim, state a limitation, or apply a concept. A paper that uses one of these eleven times
is running a template.

## The measured differences

These come from a corpus of 61,608 stories, roughly 5,000 words each, one human-written and
five model-written per prompt. Values are means on 1-5 scales, or how often a categorical
option appeared. Gap is human minus AI.

### Where AI runs high

| Feature | Human | AI | Gap |
|---|---|---|---|
| Emotion conveyed through the body | 38% | 81% | -42 |
| Narrator explicitly states the theme | 52% | 77% | -25 |
| Dialogue used for philosophical debate | 34% | 59% | -25 |
| Smell imagery present | 57% | 82% | -26 |
| Intertextual references left as vague echoes | 50% | 72% | -22 |
| Resolution driven by protagonist's choice | 46% | 69% | -23 |
| No subplots at all | 57% | 79% | -22 |
| Resolution through internal understanding | 27% | 47% | -21 |
| Character introduced by external description | 30% | 52% | -22 |
| Thematic explicitness and moralising | 3.28 | 3.94 | -0.65 |
| Setting mirrors the character's inner state | 3.58 | 4.07 | -0.49 |
| Moral or philosophical weighting | 3.26 | 3.68 | -0.42 |
| Subplots all serve one theme | 4.41 | 4.74 | -0.33 |
| Continuity of the main causal chain | 3.92 | 4.20 | -0.28 |

### Where human runs high

| Feature | Human | AI | Gap |
|---|---|---|---|
| Specific named references to other works | 47% | 24% | +23 |
| Emotion named directly ("she was afraid") | 29% | 8% | +21 |
| Protagonist framed as morally mixed | 59% | 38% | +21 |
| Subplots that run parallel rather than merge | 42% | 21% | +22 |
| Mix of explicit and implicit reference | 37% | 16% | +21 |
| Revelation forces rereading of earlier scenes | 3.28 | 2.95 | +0.34 |
| Chronological discontinuity | 2.40 | 2.12 | +0.28 |
| Fourth wall permeability | 0.67 | 0.39 | +0.28 |
| Anachrony (flashback, flash-forward) | 2.58 | 2.31 | +0.27 |
| Number of distinct locations | 1.34 | 1.08 | +0.26 |
| Dialogue relative to narration | 2.95 | 2.70 | +0.24 |
| Direct address to the reader | 0.28 | 0.07 | +0.21 |

Read these as a map of where the defaults are, not as targets. Every one of these gaps is a
tendency across tens of thousands of stories. Any individual piece can sit anywhere.

Note the two most useful rows. Models show emotion through the body 81% of the time and
name it 8% of the time; humans are at 38% and 29%. The tightening chest, the cold sweat,
the dimming lamplight are the machine default, and "she was afraid" is the human one. That
is the reverse of what creative-writing advice teaches, which is why models learned it so
hard.

## The checks

### Thematic over-determination

The text says what it means, why it matters, and what the reader should take from it. The
strongest single signal in the study.

*Fiction:* trust the scene. If an earlier scene has already made the change legible,
delete the sentence explaining it and end on an action, an image, or a line of dialogue.

*Expository:* keep the thesis explicit, because the genre requires it. Cut the "this shows
that" sentence when the analysis has already shown it. A paragraph does not need to
re-derive the thesis to have earned its place.

### Causal streamlining

Everything runs down one clean chain of causes.

*Fiction:* let a detour, a coincidence, a competing motive, or a consequence nobody
resolves stay in.

*Expository:* separate causation from correlation, chronology, and adjacency. If the
sources support a competing explanation, include it. Elegance in a causal story is usually
a sign that something was left out.

### Tidy resolution

Every question gets an answer, usually through the protagonist understanding something.

*Fiction:* not every ending is an internal acceptance. External resolution and no
resolution are both available and both underused.

*Expository:* a bounded conclusion is stronger than a total one. Say what the evidence does
not settle.

### Sensory overcoding

Emotion and significance carried by physical sensation and weather.

*Fiction:* use sensory detail where it does work, not as an emotion generator. Naming a
feeling is allowed and is the rarer choice.

*Expository:* remove it unless the assignment is reflective or ethnographic, where the
sensory detail is evidence.

### Thin reference

Vague allusion instead of a named thing.

*Fiction:* name the book, the song, the brand, the street. Human stories do this at roughly
twice the rate.

*Expository:* name the scholar, the study, the statute, the dataset, the case. Say what it
contributes. Comparing two sources beats citing four.

### Uniform temporal structure

*Fiction:* a mystery can open at the funeral and spiral backwards. It does not have to run
from first clue to reveal.

*Expository:* do not apply this. A methods section should be chronological. Historical
analysis, case studies, personal narrative, and literary analysis of a nonlinear text can
benefit; a lab report cannot.

### Reader address

Human fiction breaks the fourth wall roughly twice as often.

*Expository:* do not apply this either. Injecting "you" into a formal essay to seem human
is a different mistake with the same cause.

### Moral flattening

*Fiction:* human authors frame protagonists as morally mixed 59% of the time against 38%.

*Expository:* use evaluative language when the argument earns it. Where the sources
disagree about whether something was good, say so instead of resolving it for them.

### Single thread

*Fiction:* 79% of AI stories had no subplot at all. A second thread that runs parallel to
the first, rather than merging into it, is the most human-elevated structural choice
measured.

*Expository:* a paper can carry a secondary line of argument that qualifies the main one
without being folded into it.

## What not to do with any of this

The study is about fiction. Its findings are not empirical claims about lab reports,
memos, or history papers. Do not:

- add flashbacks to a biology paper;
- address the reader directly in a formal essay;
- manufacture moral ambiguity where the evidence is clear;
- add a second thread to expository prose that does not have one;
- remove necessary thematic explicitness from a thesis statement;
- strip sensory detail from ethnographic or reflective writing, where it is data;
- invert a feature just because the table says humans score lower on it.

The transferable finding is the one about dispersion: model output converges on a small set
of safe structural choices, and human writing does not. The fix is to make the choice
deliberately, not to make the opposite choice.

# Evidence

What is actually measured, what is folklore, and how confident to be. Read this before
citing a number or arguing with a rule.

Status values: **active** (measured, current), **weak** (real but small or model-specific),
**historical** (was true, has faded), **fiction-only** (measured on fiction, do not
generalise), **retired** (was believed, no longer supported), **unverified** (circulating
without a traceable source).

Last reviewed: September 2026. Lexical findings rot fastest; structural ones do not.

---

## The three results that shape this skill

### 1. Surface editing barely moves structure

Russell, Rajendhran, Pham, Iyyer & Wieting. *StoryScope: Investigating idiosyncrasies in AI
fiction.* COLM 2026. arXiv:2604.03136.

61,608 stories of about 5,000 words each: 10,272 prompts, each written once by a human
author and once by each of five models. 304 extracted narrative features.

| Result | Value |
|---|---|
| Human vs AI, narrative features only, no style | 93.2% macro-F1 |
| Same task with style features added | ~95.5% |
| After a span-level pass removing every surface artifact | 93.9% |
| Six-way authorship attribution, narrative only | 68.4% macro-F1 |
| Human mean rarity percentile in feature space | 0.71 vs 0.49 for AI |
| Human-AI centroid distance ÷ AI-AI centroid distance | 1.6× |

**Status: active for the general lesson, fiction-only for the specific features.** The
transferable claim is that structural choices carry authorship signal independent of style,
and that model outputs cluster while human ones disperse. The individual feature gaps are
measured on fiction and must not be applied to lab reports.

### 2. The signature comes from instruction tuning

Reinhart, Markey, Choi et al. *Do LLMs write like humans? Variation in grammatical and
rhetorical styles.* PNAS 122(8), February 2025. arXiv:2410.16107.

Biber grammatical features, GPT-4o against matched human corpora, with paired Cohen's d:

| Feature | Model vs human | d |
|---|---|---|
| Present participial clauses | 5.3× | 1.38 |
| 'That' clause as subject | 2.6× | 0.77 |
| Nominalisations | 2.1× | 1.23 |
| Phrasal coordination | 1.9× | 0.81 |
| Agentless passive | about 0.5× | — |

Random forest reaches 93 to 98% accuracy separating humans from any single model.

**The key finding is negative: base Llama models sit close to human rates on all of these.**
The distinctive noun-heavy, informationally dense register is produced by instruction
tuning, not by pretraining, and the paper concludes it "limits their ability to mimic other
writing styles."

**Status: active.** This is the best evidence for genre conditioning, and the source of the
correction about passive voice.

### 3. Short sentences are what went missing

Gude et al. *More Aligned, Less Diverse?* arXiv:2605.06030. Preprint, venue unconfirmed.

New York Times prose against model-generated news, parsed with the English Resource Grammar.

| Corpus | Tokens/sentence | Sentences ≤15 tokens | Fragments |
|---|---|---|---|
| NYT human, 2023 | 22.3 | 33% | 13% |
| NYT human, 2025 | 22.2 | 32% | 12% |
| Llama base models, 2023 | 18.2–19.4 | 35–39% | 12–13% |
| Qwen instruct, 2025 | 25.6–26.1 | 2–4% | 2% |
| GPT-4o, 2025 | 26.0 | 1% | 2% |
| Llama-70B, 2025 | 29.9 | 1% | 2% |

Note the 2023 base models again: *more* short sentences than humans. The collapse is an
alignment artifact.

Corroborated by Muñoz-Ortiz, Gómez-Rodríguez & Vilares, *Artificial Intelligence Review*
57:265 (2024), peer-reviewed, which reports that human texts show "more scattered sentence
length distributions" while models cluster in the 10-to-30-token band. That paper gives a
distribution plot and no summary statistic.

**Status: active, preprint.** Use the short-sentence proportion, not a variance target.

---

## Lexis

### Verified word lists

Kobak, González-Márquez, Horvát & Lause. *Delving into LLM-assisted writing in biomedical
publications through excess vocabulary.* Science Advances 11(27), eadt3813, 2025. 15.1M
PubMed abstracts, 2010 to 2024. Peer-reviewed, the strongest source here.

- 454 excess words in 2024, against a Covid-era peak of 190 in 2021.
- At least 13.5% of 2024 abstracts show LLM processing. This is a lower bound.
- Of the 379 excess *style* words in 2024, 66% are verbs and 14% adjectives. The tell is
  verb-shaped, not noun-shaped.
- Highest ratios: `delves` 28.0, `underscores` 13.8, `showcasing` 10.7.
- The ten highest-volume markers, which matter more for ordinary prose than `delve` does
  because they hide better: **across, additionally, comprehensive, crucial, enhancing,
  exhibited, insights, notably, particularly, within.**
- Rate varies hugely by venue: Sensors 0.25, MDPI pooled 0.21, Frontiers 0.20, against
  Nature/Science/Cell 0.07.

Juzek & Ward. *Why Does ChatGPT "Delve" So Much?* COLING 2025. PubMed, 26.7M abstracts.
Occurrences per million, 2020 to 2024: `delves` 0.21 → 14.38 (+6697%), `showcasing` 0.59 →
8.79 (+1396%), `underscores` 4.50 → 45.19 (+904%), `intricate` 6.22 → 44.22 (+611%).

Their follow-up (BIAS 2025 @ ECML-PKDD, arXiv:2508.01930) establishes the causal link:
813 of the 814 words used significantly more by Llama-Instruct than Llama-Base were also
used more than in the human baseline. Raters preferred high-feedback-score variants, 52.4%
against 47.6%, p < .01.

Liang et al. *Monitoring AI-Modified Content at Scale.* ICML 2024. Estimated LLM-generated
fraction of conference reviews: NeurIPS 2019-22 about 1.7%, NeurIPS 2023 9.1%, ICLR 2024
10.6%, EMNLP 2023 16.9%. Fold increases in ICLR 2024: `commendable` 9.8×, `meticulous`
34.7×, `intricate` 11.2×. Their 100-item adjective and adverb lists are rank-ordered with
no per-word numbers.

Reinhart et al. Table 1, rate against human: GPT-4o `camaraderie` 162×, `tapestry` 155×,
`intricate` 119×, `underscore` 107×. `tapestry` appears in 23% of GPT-4o outputs, `amidst`
in 27%. Base models' overused words are proper nouns and artifacts, which again points at
instruction tuning.

**Status: active but decaying.** Yakura et al. (arXiv:2409.01754), on 740,249 hours of
speech, tracked the odds ratio for `delve` falling from over 300:1 for GPT-3.5 and GPT-4 to
about 100:1 for GPT-4-turbo and about 40:1 for GPT-4o. Word lists are a smoke test, not a
metric.

### Function words

Terčon & Dobrovoljc. *Linguistic Characteristics of AI-Generated Text: A Survey.*
arXiv:2510.05136, reviewing 44 articles.

Machine text is **less** likely to contain: `however, but, although, because, if, that, or,
when, as`; the pronouns `this, I, they, my, it, us`; the prepositions `to, as, before,
about, since`; the modals `will, would, might, could`; the adverbs `up, out, off`. It is
**more** likely to contain `can`, `and`, `by/with/for`, and `their`.

It also underuses the verb `say`, feeling words, and sensing verbs (`read`, `look`,
`hear`).

**Status: active, survey-level.** Useful mainly as a reminder that subordination and
concession are human habits.

---

## Rhetoric

### Tricolon

Bakhshi. arXiv:2604.19768. 225 argumentative texts, 75 per group, about 0.6M tokens.

| Device, mean per document | Human expert | Human non-expert | Model | d |
|---|---|---|---|---|
| Tricolon | 3.73 | 4.87 | 7.13 | 0.95 |
| Rhetorical question | 5.55 | 5.11 | 2.28 | 0.73 |
| Correctio (self-correction) | 0.40 | 0.45 | 0.17 | 0.40 |

Note the inverse tells: models ask rhetorical questions at under half the human rate and
correct themselves less often.

**Status: weak.** Single-author preprint, and the device counts were produced by an LLM
annotator with no human validation. The authors say so themselves. Treat the direction as
suggestive and the magnitudes as soft.

### "It's not X, it's Y"

**Status: unverified.** No peer-reviewed measurement exists. The widely repeated "three
times more often than humans" traces to a single journalistic source. Two further figures
circulate, a 6% rate in one message dataset and a rise from 50 to over 200 occurrences in
Fortune 500 filings, neither traceable to a primary source.

Keep acting on this pattern. It is a real writing defect on its own terms, because the
negative half usually names something nobody claimed. Do not cite a number for it.

### Editorial artifact categories

Chakrabarty, Laban & Wu. *Can AI writing be salvaged?* CHI 2025. arXiv:2409.14509. The LAMP
corpus: 1,057 model-written passages, 8,035 fine-grained edits by 18 professional writers
holding MFAs. Seven categories, induced from the writers' own free-form labels; only 5% of
edits fell outside them.

| Category | Share of edits |
|---|---|
| Awkward word choice and phrasing | 28% |
| Poor sentence structure | 20% |
| Unnecessary or redundant exposition | 18% |
| Cliché | 17% |
| Purple prose, lack of specificity, tense inconsistency | the remainder |

Two details worth keeping. First, the generation prompt had already told the models to
avoid clichés and ornamental language; the artifacts survived the instruction. Second, edits
in the "lack of specificity" category typically make the text **longer**. Humanising is not
the same as cutting.

Edit operations were 74% replacements, 18% deletions, 8% insertions, and 70% of
non-deletion edits preserved meaning.

**Status: active.** Also useful as calibration: the best model detector reached 0.46
precision at finding these spans, against 0.57 for expert-expert agreement. Even
professionals only weakly agree on which category a span belongs to.

---

## Structure and repetition

Shaib, Li, Joseph et al. *Detection and Measurement of Syntactic Templates in Generated
Text.* EMNLP 2024. A template is a part-of-speech n-gram repeating above a threshold.

On the Rotten Tomatoes set, 95% of model outputs contain a six-tag template, against 38%
for human reference text. Templates per token rise with model size: Llama-2-7B 0.047,
70B 0.123, Llama-3-70B 0.151. Sampling temperature does not help; the rate stays at
96.8% ± 0.6 across settings.

Two caveats. On conventionally formulaic genres such as medical meta-analyses, human
references are already 83.3% templated and several models fall below them. And the
companion paper (*Measuring AI "Slop" in Text*, arXiv:2509.19163) found that repetition and
templatedness were **not** significant predictors of human judgments of slop; density,
relevance, bias, coherence, and tone were.

**Status: active for expository and narrative genres, inapplicable to formulaic ones.**

Shaib et al. *Standardizing the Measurement of Text Diversity.* AACL 2025. Compression ratio
over part-of-speech sequences is the measure that best separates human from model text.
Homogenisation and MATTR detect no difference at all. Length confounds every measure in the
type-token family, so report it alongside.

Doshi & Hauser. *Science Advances* 2024. AI assistance raised the rating of any individual
story while making the set of stories more similar to one another. This is the basis for
the `variants` mode.

---

## Typography

Freeburg. *The Last Fingerprint.* arXiv:2603.27006. Single-author preprint. Human baseline
of eight published essays, 57,232 words: **weighted mean 3.23 em dashes per 1,000 words,
median 3.83, range 0.33 to 17.12.** A fifty-fold spread across human writers.

Per 1,000 words, unconstrained: GPT-4.1 10.62, Claude Opus 9.09, DeepSeek V3 6.95, GPT-4o
4.12, **Gemini 2.5 Pro 3.53 (indistinguishable from the human mean)**, GPT-5.4 1.43, both
Llama Instruct models **0.00**.

**Status: weak and model-specific.** The paper's own limitation says claims of overuse
"must be qualified by genre and author." Older peer-reviewed work points the other way
entirely: Terčon & Dobrovoljc report that machine text contains *fewer* commas, question
marks, dashes, parentheses, semicolons, and colons than human text.

Wikipedia's own page carries a note that its em-dash section may belong in the historical
category.

**Do not ban the em dash.** Match the writer's sample.

---

## Detection, and why it is not the target

- Human judges perform at roughly chance at identifying AI text. One study of German theses
  found 57% on AI text and 64% on human text. Frequent LLM users do far better, around 90%,
  and rely on originality, formality, and clarity rather than word lists (Russell et al.,
  ACL 2025).
- Detectors fail under domain shift, unseen models, paraphrasing, and light editing. RAID,
  spanning more than six million generations across 11 models and eight domains, found broad
  vulnerability to attacks and decoding changes.
- Fine-tuning a model to imitate human style has been reported to drop detection on creative
  writing from 97% to 3%.
- GPTZero stated publicly that it stopped using perplexity and burstiness in autumn 2023.
  Any advice framed around those two terms is describing a retired method.
- Human writing is absorbing machine habits through exposure, so the base rates move.

Report detector output as a diagnostic if someone asks. Never optimise against it. A skill
tuned to a detector is a skill tuned to that detector's errors.

---

## Retired

Both were treated as AI indicators in earlier versions of this skill and by earlier upstream
catalogues. They were dropped in 2026 and are not detected here.

**False ranges** (`from X to Y, these...` where X and Y mark no real continuum). Now an
ordinary clarity question, not an authorship signal.

**Synonym cycling / elegant variation.** Reclassified as a historical indicator, caused by
repetition penalties in older models. It is also a habit taught in several school systems
outside the English-speaking world. In technical prose, stable repetition of the correct
term is *better* than variation.

---

## Do not cite

These circulate widely and cannot be traced to a primary source. Several appear in other
humanizing guides.

1. Any specific standard deviation or coefficient of variation for human sentence length.
   The figure around 8.2 words traces to marketing content.
2. The "three times more often" ratio for negative parallelism, and the associated 6% and
   Fortune-500 figures.
3. Perplexity and burstiness thresholds of any kind.
4. Any claim that a specific edit will change a detector's verdict.

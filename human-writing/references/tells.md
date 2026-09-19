# The catalogue

Every pattern below is one form of the same thing: the average chosen over the particular.
Each entry gives what to look for, why it happens, and what to write instead.

**Strength classes.** *Act* means one sighting justifies an edit. *Weak alone* means it
counts only when other tells share the passage, because careful writers do it on purpose.

---

# A. Act on sight

Nothing here needs rewriting. It needs deleting.

## A1. Paste artifacts

Machine citation markup that came along with the copy. Search for these literally:

| Source | Marker |
|---|---|
| ChatGPT | `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `citeturn0search0`, `Wikipedia+1`, `{"attribution":{"attributableIndex":...}}` |
| ChatGPT links | `utm_source=openai`, `utm_source=chatgpt.com` |
| Gemini | `[cite: 3, 12]`, `[span_1](start_span)` |
| Grok | `<grok-card data-id=...>`, `referrer=grok.com` |
| DeepSeek | `【85†L261-269】`, run-on domains like `medway.gov.ukmedway.gov.uk` |
| Perplexity | `[web:1]`, `[attached_file:1]` |
| Copilot | `utm_source=copilot.com` |
| Unclassified | `:::writing{variant="document" id="51724"}`, `↩` around footnotes |

Also: unfilled placeholders (`[Your Name]`, `INSERT_SOURCE_URL_30`, `|access-date=2025-XX-XX`),
and Markdown syntax pasted where the target format is not Markdown.

## A2. Assistant residue

> Great question! Here is an overview of the French Revolution. It began in 1789 when a
> financial crisis and food shortages led to widespread unrest. I hope this helps! Let me
> know if you'd like me to expand on any section.

> The French Revolution began in 1789 when a financial crisis and food shortages led to
> widespread unrest.

Watch for: *I hope this helps*, *Certainly!*, *Of course!*, *Great question*, *You're
absolutely right*, *Would you like me to*, *let me know if*, *here's a breakdown*, *is
there anything else*.

This is the most certain tell in the list and the easiest to miss when it wraps real
content. Remove the wrapper, keep the content.

## A3. Knowledge-cutoff disclaimers, and the guess that follows

> While specific details about the company's founding are not extensively documented in
> readily available sources, it appears to have been established sometime in the 1990s.

> The available sources do not give a founding date.

The second half is the real damage. A model that finds nothing often says so and then fills
the gap with something plausible. Watch for the pair: a disclaimer, then a *likely*, then a
sentence about why it matters.

> Information about her early life is not publicly available, suggesting she maintains a
> low profile. She likely grew up in a middle-class household, which shaped her later
> interest in education reform.

> Her early life is not documented in the available sources.

Watch for: *as of my last knowledge update*, *up to my last training update*, *while
specific details are limited*, *not widely documented*, *in the available sources*, *based
on available information*, *maintains a low profile*, *keeps personal details private*,
*likely*, *it is believed that*.

## A4. Invented sources

A DOI that resolves to an unrelated paper. A book citation with no page number for a
general-topic book. A quotation attributed to someone who was dead at the time. A page
number that does not contain the claim.

Check any citation you did not personally supply. If it cannot be checked, remove the claim
rather than the citation.

---

# B. Staging instead of stating

The sentence signals that something is important instead of adding information. This is the
strongest and most frequent class in current model prose.

## B1. Not X, but Y

The negative half names something nobody claimed, which makes the positive half sound
larger. It appears in four shapes.

**Straight:**

> It's not just about the beat riding under the vocals; it's part of the aggression and
> atmosphere.

> The heavy beat adds to the aggressive tone.

**Split across sentences:**

> This does not mean every choice is equal. It means there is no external system that
> confirms which choice is right.

> No external system confirms which choice is right, though the choices still have
> different consequences.

**Reversed:**

> The regime prioritised consolidation of power rather than ideological purity.

> The regime consolidated power first. Ideology came second, when it came at all.

**Clipped tail:**

> The options come from the selected item, no guessing.

> The options come from the selected item, so the user never has to guess.

*Keep it when* the negative half corrects a belief the reader actually holds, or when both
halves carry information. "The 1918 flu did not begin in Spain; it was first reported there
because Spanish papers were not censored" is a real contrast doing real work.

## B2. One-line closers and dramatic fragments

> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No
> nostalgia for human taste. The old rules were gone.

> AlphaEvolve searched differently because it did not favour symmetry or human-looking
> designs, which made some older assumptions less useful.

Watch for: a one-sentence paragraph restating the paragraph above it; the same closer under
every heading; *That is the real win*, *Read that again*, *Let that sink in*; a run of
fragments; one word in caps; periods. between. words.

One short sentence works when it carries something new. A closer that repeats does not.

## B3. Sayings that sound deep

> The real question is whether teams can adapt. At its core, what really matters is
> organisational readiness.

> The question is whether teams can adapt, which mostly depends on whether the organisation
> is willing to change how it works.

Watch for: *the real question is*, *at its core*, *at the heart of*, *what truly matters*,
*the deeper issue*, *herein lies*, *fundamentally*, and the aphorism form: *X is the
language of Y*, *X is the currency of Y*, *X becomes a trap*.

> Symmetry is the language of trust.

> Symmetric layouts feel more predictable to most users.

## B4. Staged run-up

> Let's dive into how caching works in Next.js. Here's what you need to know.

> Next.js caches at several layers: request memoisation, the data cache, and the router
> cache.

Watch for: *let's dive in*, *let's explore*, *let's break this down*, *here's what you need
to know*, *without further ado*, *in this article we will*.

And the staged-candour version, which is the same move wearing a different coat:

> Is it worth the price? Honestly? It depends on how often you'll use it.

> Whether it's worth the price depends on how often you'll use it.

*Keep it when* the writer genuinely talks this way. "Honestly" inside a sentence is
ordinary; the tell is the standalone opener before a routine claim.

## B5. Arguing with nobody

> This isn't mainly about prompt length, and I'm not arguing that documentation doesn't
> matter. The issue is whether the agent can use the instruction when it acts.

> The issue is whether the agent can use the instruction when it acts.

And the invented alternative, rejected to make the real choice look considered:

> Session tokens rotate every 24 hours. A tempting approach would be to rotate them by
> restarting the auth service on a cron job, but that would drop every active session.
> Rotation happens in place instead.

> Session tokens rotate in place every 24 hours, and clients refresh transparently.

Watch for: *some might argue*, *one might be tempted to*, *a tempting approach would be*,
*an obvious approach would be*, *you might think*, *it would be easy to just*, *don't get me
wrong*, *to be clear*, *this is not to say*.

*Keep it when* the objection is attributable to a source or is a position genuinely held in
the field, and when addressing it changes the thesis, its scope, or its confidence. A token
objection dismissed in one sentence is worse than none.

---

# C. Inflation and borrowed authority

The fact underneath is usually fine. Remove the dressing and keep the fact.

## C1. Inflated significance

> The Statistical Institute of Catalonia was officially established in 1989, marking a
> pivotal moment in the evolution of regional statistics in Spain. This initiative was part
> of a broader movement across Spain to decentralise administrative functions and enhance
> regional governance.

> The Statistical Institute of Catalonia was established in 1989, part of a wider
> decentralisation of administrative functions in Spain.

Watch for: *stands as a testament*, *serves as a reminder*, *a pivotal/crucial moment*,
*plays a key role*, *marking a shift*, *underscores its importance*, *reflects a broader*,
*enduring legacy*, *indelible mark*, *setting the stage for*, *paved the way for*, *ushering
in a new era*, *evolving landscape*, *cannot be overstated*, *now more than ever*, *since
the dawn of time*.

## C2. The challenges-and-future template

Three moves that travel together: a "Challenges" section that opens with *Despite its
[good thing], X faces challenges*, a vaguely positive assessment, and a send-off.

> Despite its industrial prosperity, Korattur faces challenges typical of urban areas,
> including traffic congestion and water scarcity. Despite these challenges, with its
> strategic location and ongoing initiatives, Korattur continues to thrive as an integral
> part of Chennai's growth.

> Korattur has recurring traffic congestion and water shortages.

> The future looks bright. Exciting times lie ahead as the team continues its journey
> toward excellence.

> (Cut it. End on the last concrete fact.)

Watch for the headings too: *Challenges and Legacy*, *Future Outlook*, *Future Directions*,
*Awards and Recognition*, *Legacy and Impact*. The last one is close to ubiquitous.

Also: *only time will tell*, *it remains to be seen*, *one thing is certain*, *stakeholders
must work together*, *a step in the right direction*, *continues to evolve*.

This is about the formula, not about mentioning difficulties. Real problems belong in the
text. They belong where the argument needs them, described specifically.

## C3. Superficial participial riders

An `-ing` phrase bolted to the end of a fact to make it sound analysed.

> The temple's palette of blue, green, and gold resonates with the region's natural beauty,
> symbolising Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes,
> reflecting the community's deep connection to the land.

> The temple is painted blue, green, and gold, colours chosen to evoke Texas bluebonnets
> and the Gulf.

Watch for a comma followed by: *highlighting*, *underscoring*, *emphasising*, *reflecting*,
*symbolising*, *showcasing*, *demonstrating*, *illustrating*, *ensuring*, *fostering*,
*cultivating*, *contributing to*, *encompassing*, *enhancing*, *serving as*, *paving the
way*, *cementing*, *solidifying*.

Attaching one to a named source does not rescue it. "Roger Ebert highlighted the lasting
influence" is still unsupported if Ebert said no such thing.

*Keep it when* the phrase states an inference the source actually supports.

## C4. Borrowed authority

Two forms. An unnamed expert propping up a claim:

> Due to its unique characteristics, the Haolai River is of interest to researchers and
> conservationists. Experts believe it plays a crucial role in the regional ecosystem.

> Researchers study the Haolai River for its unusual water chemistry.

And a list of prestigious outlets propping up a person:

> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She
> maintains an active social media presence with over 500,000 followers.

> The New York Times and the BBC have quoted her on central-bank policy.

Watch for: *experts say*, *researchers believe*, *studies show*, *critics argue*, *industry
reports*, *observers have cited*, *several sources*, *it is widely believed*, *independent
coverage*, *trade publications*, *cited/featured/profiled in*, *active social media
presence*, *over N followers*.

Say what the source said. If the source is not available, cut the claim. Never invent one.

A missing citation is not itself a tell. Most human writing is unsourced.

## C5. Vague connection

The text says two things are related without saying how.

> In 2017, sources identified John Doe as being associated with the leadership of
> ExampleCorp.

> John Doe was chief executive of ExampleCorp in 2017.

Watch for: *associated with*, *connected to*, *in connection with*, *in association with*,
*linked to*, *tied to*.

*Keep the vague wording* if the source really does not specify the relationship. Do not
invent a job title to make the sentence cleaner.

## C6. Sales register in neutral prose

> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as
> a vibrant town with a rich cultural heritage and stunning natural beauty.

> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

Watch for: *boasts*, *nestled*, *in the heart of*, *breathtaking*, *stunning*,
*picturesque*, *vibrant*, *rich cultural heritage*, *natural beauty*, *renowned*,
*must-visit*, *world-class*, *diverse array*, *commitment to excellence*, *exemplifies*,
*groundbreaking*.

Models trained on marketing copy reach for it under any prompt. It is most visible in
writing about places, companies, and products, and it is always wrong in neutral prose.

## C7. Avoiding is, are, and has

> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features
> four separate spaces and boasts over 3,000 square feet.

> Gallery 825 is LAAA's exhibition space for contemporary art. It has four rooms totalling
> 3,000 square feet.

Watch for: *serves as*, *stands as*, *functions as*, *operates as*, *represents a*,
*marks the*, *boasts*, *features*, *offers*, *maintains*, *refers to*, *holds the
distinction of being*, *ventured into*, *embarked on a career as*.

One study measured a drop of more than 10% in the use of *is* and *are* in academic
writing after 2022. Plain copulas are a human signal. Use them.

## C8. Overclaimed scope

> This comprehensive overview examines all aspects of the policy.

> This section covers the funding formula and the appeals process. It does not cover
> implementation.

Watch for: *comprehensive overview*, *in-depth analysis*, *all aspects of*, *a wide range
of*, *a plethora of*, *a myriad of*, *from X to Y, these...* when X and Y do not mark a real
continuum.

## C9. Didactic disclaimers

> However, it's important to note that requirements may vary by jurisdiction.

> Requirements differ between states; California requires a permit and Texas does not.

Watch for: *it's important to note*, *it's worth noting*, *it is crucial to remember*, *may
vary*. These come from safety-tuned refusals leaking into ordinary prose.

## C10. Stacked hedging

> It could potentially possibly be argued that the policy might have some effect on
> outcomes.

> The policy may affect outcomes.

Watch for: *could potentially*, *might arguably*, *in some cases it may possibly*, *it is
possible that X may*, *to be fair*, *it's also possible*.

Qualification should match the evidence. One accurate hedge beats three vague ones. Note
the difference from ordinary single hedges (*perhaps*, *tends to*, *very*), which are human
signals and should be left alone.

---

# D. Rhythm and shape by rule

## D1. Forced triads

> The event features keynote sessions, panel discussions, and networking opportunities.
> Attendees can expect innovation, inspiration, and industry insights.

> The event has talks and panels, with time between sessions for people to find each other.

Three is a real number. It is also the number reached for when the writer does not know how
many items there are. Check that each of the three carries a distinct idea; if two overlap,
merge them, or develop the strongest one.

The pattern also runs at paragraph scale: three parallel examples, or three short facts
followed by a lesson.

> A career can look promising and fail. A relationship can feel important and end. A skill
> can take years and remain useless. These decisions rarely explain themselves.

> A career can look promising and fail, and so can a relationship that felt important, or a
> skill that took years and stayed useless. These decisions rarely explain themselves.

## D2. Repeated openings

> She noted the door. She noted the lock on it. She filed both away.

> She noted the door and its lock, then filed both away.

Detect runs of three or more sentences opening with the same word, and paragraphs opening
with the same construction. Do not ban the word; a later sentence can still start with
"She." Deliberate anaphora is a real device: *She came. She saw. She conquered.*

## D3. Transition adverbs doing the joining

One "however" is normal. Every paragraph opening with *Furthermore*, *Moreover*,
*Additionally*, or *Consequently* means the paragraphs are being stapled rather than
argued.

> Moreover, the second study found a smaller effect.

> The second study found a smaller effect, and it used a wider age range, which may be why.

Name the actual relationship, or use no connective. A transition word in isolation is a
weak signal; a paper where every seam is an adverb is not.

## D4. Uniform sentence length

A run of five or more sentences within a few words of each other reads as machined. So does
a run of fragments.

Do not fix this by chopping sentences. Find the place where the content itself wants a
short sentence, or wants a long one, and let it. Manufactured burstiness is its own
template.

For reference, `scripts/scan.py` reports the coefficient of variation of sentence length.
Published prose usually sits between about 0.45 and 0.75. Below 0.35, look for a reason.
Treat that as a prompt to reread, never as a target to hit.

## D5. Uniform paragraph template

Every paragraph running `topic sentence -> two examples -> significance -> transition`.

Shape each paragraph around what it has to do. See `references/structure.md`.

## D6. Repeated thesis restatement

Academic writing is explicit by convention, but the thesis does not need paraphrasing at
the end of every paragraph. Use paragraph endings to move the argument forward.

## D7. Overclean causal language

*Therefore*, *thus*, and *consequently* imply that one point proves the next. Check which
relation actually holds: causal, correlational, chronological, inferential, contrastive, or
merely adjacent. Use the right one, or none.

---

# E. Formatting and mechanics

Templates and visual editors produce clean formatting too. The tell is decoration applied to
every item.

## E1. Bold as decoration

> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**,
> and visual strategy tools such as the **Business Model Canvas (BMC)**.

> It blends OKRs, KPIs, and tools like the Business Model Canvas.

And the labelled list, which is the single strongest formatting tell in anything meant as
prose:

> - **User Experience:** The user experience has been improved with a new interface.
> - **Performance:** Performance has been enhanced through optimised algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

> The update adds a new interface, speeds up load times, and encrypts data end to end.

Bold marks the exception, not the argument.

## E2. Decorative headings

Title Case where the publication uses sentence case. Emoji in front of headings or bullets.
Arrows as decoration. A horizontal rule between every section. A level-1 heading at the top
repeating the document's own title. Sections starting at level 3 with no level 2.

> ## Strategic Negotiations And Global Partnerships

> ## Strategic negotiations and global partnerships

> 🚀 **Launch Phase:** The product launches in Q3

> The product launches in Q3.

## E3. A heading restated by the line under it

> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

> ## Performance
>
> When users hit a slow page, they leave.

## E4. Lists carrying reasoning

When a document has more list items than prose paragraphs, check whether the lists are
holding an argument that needs sentences. Bullets are good for parallel items and bad for
reasoning, because they hide the relationships between the points.

## E5. Invisible characters

Non-breaking spaces, narrow no-break spaces, zero-width spaces, soft hyphens. Always paste
artifacts. Strip them.

## E6. Writing about the previous draft

> This function was added to replace the previous approach of iterating through all items,
> which caused O(n²) performance.

> This function uses a hash map, so lookups are O(1).

Describe what the text does now. Previous versions belong in change logs and migration
guides.

---

# F. Weak alone

Real writers do these deliberately. Count them only with company.

**Em dashes.** Standard in edited prose. A 2026 study found that among current models only
one used em dashes more than professional writers, and one used them noticeably less. The
signal, if any, is the *rate against the writer's own sample*, plus inconsistent spacing
(some spaced, some not) which indicates a paste. If the writer's sample uses dashes, match
its rate. Do not ban the mark.

**Curly quotes.** Word, macOS, iOS, LanguageTool, and every Chicago-styled publisher
produce them. The tell is *mixing* curly and straight in one document, not curliness.

**Passive voice.** Correct and expected in methods sections and where the actor is unknown
or irrelevant. Change it when the sentence hides who acted and that matters.

**Hyphenated compounds.** Keep the hyphen before a noun (`a high-quality report`), drop it
after (`the report is high quality`). Only worth acting on when the whole document does it.

**Vague association** (C5), **stacked disclaimers** (B5), **`represents a`** (C7). Each
needs a neighbour.

---

# H. The second template

What over-corrected prose looks like. These were found by blind review of this skill's own
output, which is why they are here: a reviewer who did not know which text was which
identified the rewrite as the better prose and then took it apart on these grounds.

They are harder to catch than anything in sections A to F, because they read as
intelligence rather than as sloppiness.

## H1. Substance replaced by epistemic performance

The most damaging one.

> There is a competing account, and it should be tested before this argument goes any
> further. Telling the two apart needs employment figures by metropolitan area. What can be
> said without that data is narrower. That is a claim about buildings rather than about the
> future of cities, and it has the advantage of being checkable.

Four sentences whose grammatical subject is *the evidence* rather than *the city*. Each is
defensible alone. Together they turn a piece about urban economics into a piece about its
own evidential position.

The mechanism is worth understanding, because the rule that causes it is a good rule. A
claim is unsupported. Inventing support is forbidden. So the claim is deleted, and something
has to fill the space, and what fills it is a sentence about the deletion.

**When a claim lacks support there are three moves:** find the support, state the narrower
claim the material does support, or cut it and say nothing about the cut. Announcing the gap
is a fourth move and it is almost always the worst. A bracketed `[source needed]` marker in a
draft is fine; a paragraph about what a source would show is not.

Watch for: *what can be said without that data*, *telling the two apart requires*, *before
this argument goes further*, *that has the advantage of being checkable*, *the evidence here
does not support*, *I have no clean answer, which is itself a finding*.

## H2. Manufactured specificity

> The app works beautifully for about eleven days.

> A connector that syncs one direction and silently stops in March.

> A system you maintain at sixty per cent is worth more than one you abandon at ninety.

None of those numbers is a measurement. They are the *texture* of measurement, chosen
because odd precision reads as lived experience. This is the same defect as inventing a
statistic, wearing better clothes, and it is more dangerous precisely because it is more
persuasive.

Every number comes from the source or from the writer. A number invented to sound human is a
fabrication with a style motive.

## H3. Aphorism on a schedule

> You are usually not the problem. The claim was.

> They do less. That turns out to be most of the point.

> Nobody abandons an app because it is powerful.

One short quotable sentence at the end of a paragraph is a good instinct. One at the end of
every paragraph is a rhythm, and a reader who notices the rhythm can see the machinery
behind it. Check what share of paragraphs end this way. Above roughly half, break the
pattern somewhere.

## H4. Pre-emptive self-critique as transition

> That sounds glib, so here is what I mean concretely.

It claims credit for rigour before supplying any, and it is a transition doing the work of
an argument. Cut it and start with the concrete thing.

## H5. Contrarian posture with no opponent

> Any argument about causes has to account for that lag, and most do not.

Which arguments? The claim is unfalsifiable, costs nothing, and positions the writer above a
crowd that is never named. If there is an opponent, name them. If not, drop the comparison
and make the point on its own.

## H6. Voice by template

*Load-bearing. Downstream of. The thing about X is. Is doing a lot of work. That turns out
to be most of the point.*

These come from one internet register and they arrive in clusters. Borrowed voice is still
borrowed; it just borrows from a smaller, more flattering source than the default one.

## H7. Studied plainness

Deliberately flat diction deployed to perform unpretentiousness. Plain writing that is
plain because the thought is clear reads differently from plain writing that is plain as a
costume, and readers can tell.

## The substance gate

Count the concrete claims before and after. A concrete claim names a thing, a quantity, a
mechanism, an actor, or a relationship a reader could check or dispute.

If the rewrite has fewer, the edit failed, unless cuts were requested. Removing an
unsupported claim is right. Leaving a hole where it stood is not. Put the narrower supported
claim in its place, and keep the mechanisms, the named parties, and the numbers that were
already there.

Fluent prose that says less is not an improvement. It is the same failure as inflated prose,
approached from the other side.

---

# G. Not tells

Do not act on these. Several point the other way.

- **Correct grammar.** Plenty of people write well.
- **Formal or academic register.** Models overuse a *specific* list of words. The
  correlation does not extend to formal prose in general.
- **Mixed registers**, clinical and emotional in one passage. Often a person in a technical
  field, or a young writer, or several editors on one document.
- **Bland prose.** Model output skews positive and verbose, not flat.
- **Transition words in isolation.**
- **Unsourced content.** Most writing is unsourced.
- **Markdown** from someone who writes in Markdown daily.
- **Anything written before 30 November 2022.**
- **Plain copulas, plain verbs, flat superlatives, ordinary hedges, mildly wordy
  connectives.** These are signals of human writing. Protect them. See the
  "Do not over-tighten" section of SKILL.md.

Keep the details that carry a voice:

- A specific, odd detail: a real address, a strange quote, "the lawyer who used to work
  upstairs from my dentist."
- Mixed feelings left unresolved: "I think this is mostly good, but it bothers me and I
  can't fully say why."
- References tied to a year and a subculture.
- A first-person choice the writer can explain.
- A genuine aside or self-correction: "(I keep wanting to say 'almost' here, but it really
  was certain.)"

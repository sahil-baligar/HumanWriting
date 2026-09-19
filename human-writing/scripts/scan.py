#!/usr/bin/env python3
"""
scan.py - a measuring instrument for AI-default writing patterns.

It reports. It does not rewrite, does not score "AI probability", and does
not tell you a number is bad. Every count is context-free. A human still
has to decide whether each hit is a defect, a convention of the genre, or
the writer's own habit.

Two things make this different from a banned-word list:

  * It counts signals of HUMAN writing too. Some standard "tighten your
    prose" advice (cut "in order to", replace "is" with a stronger verb,
    delete "very") moves text toward the machine cluster, not away from
    it. Those counters are reported as things to protect.

  * It measures shape - sentence-length variance, paragraph uniformity,
    opener repetition - because shape is what survives paraphrase.

Usage
    python scan.py draft.md
    python scan.py draft.md --json
    python scan.py a.md b.md c.md         # compare drafts
    cat draft.md | python scan.py -

Stdlib only. Python 3.8+.

Sources for the pattern lists:
    Wikipedia:Signs of AI writing (WikiProject AI Cleanup), read 2026-09
    Russell et al., StoryScope, COLM 2026
    Juzek & Ward 2025; Liang et al. 2024; Shaib et al. 2024
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter

VERSION = "2.0.0"

# ===========================================================================
# 1. VOCABULARY
# ===========================================================================
# Overrepresented in LLM output relative to human writing of the same genre.
# Grouped by the era in which each cluster peaked, because these lists rot.
# A word here is not a banned word. Density is the signal, not presence.

VOCAB = {
    # Peaked 2023 - mid 2024 (GPT-4 era). Still the strongest cluster.
    "gpt4": [
        "additionally", "boasts", "bolstered", "crucial", "delve", "delves",
        "delving", "emphasizing", "enduring", "garner", "garnered",
        "intricate", "intricacies", "interplay", "landscape", "meticulous",
        "meticulously", "pivotal", "underscore", "underscores",
        "underscoring", "tapestry", "testament", "valuable", "vibrant",
    ],
    # Peaked mid 2024 - mid 2025 (GPT-4o era).
    "gpt4o": [
        "align", "aligns", "aligned", "enhance", "enhances", "enhancing",
        "fostering", "foster", "fosters", "highlighting", "highlights",
        "showcasing", "showcase", "showcases",
    ],
    # Mid 2025 onward. Shorter list; the habit moved from vocabulary to
    # claims about notability and coverage.
    "current": [
        "emphasizing", "enhance", "highlighting", "showcasing",
        "independent coverage", "trade publications", "active social media",
    ],
    # Recurring across eras; documented in the lexical-shift literature.
    "persistent": [
        "realm", "robust", "seamless", "seamlessly", "comprehensive",
        "holistic", "multifaceted", "nuanced", "transformative",
        "groundbreaking", "revolutionary", "cutting-edge", "unprecedented",
        "myriad", "plethora", "cornerstone", "hallmark", "beacon",
        "elevate", "streamline", "streamlined", "unlock", "embark",
        "resonate", "resonates", "profound", "compelling", "invaluable",
        "leverage", "leverages", "leveraging", "harness", "harnessing",
        "navigate", "navigating", "empower", "empowering", "curated",
        "bespoke", "paradigm", "ecosystem", "poised", "captivating",
        "indelible", "burgeoning", "quintessential", "palpable",
        "encompassing", "encompasses", "renowned", "esteemed", "nestled",
        "breathtaking", "stunning", "exemplifies", "pioneering",
    ],
    # Grok-specific, per Wikipedia's model-differences section.
    "grok": ["causal", "empirical", "correlate", "correlates"],
}

ALL_VOCAB = sorted({w for group in VOCAB.values() for w in group if " " not in w})


# ===========================================================================
# 2. SIGNALS OF HUMAN WRITING
# ===========================================================================
# Wikipedia's "Signs of human writing" section lists constructions that are
# MORE common in human prose than in LLM output. Standard editing advice
# tells you to delete most of them. Deleting them makes text read more like
# a machine, not less. These are counted so you can see whether a rewrite
# stripped them out.

HUMAN_SIGNALS = {
    # Plain copulas. LLMs replace these with "serves as", "stands as".
    "plain_copula": r"\b(?:there\s+(?:is|are|was|were)|it\s+(?:is|was|has)|is\s+a|are\s+a|has\s+a|have\s+a)\b",
    # Plain verbs where a model reaches for a stiff synonym.
    "plain_verbs": r"\b(?:wrote|moved|used|tried|died|made|got|said|found|showed|began|kept|left|took|gave|put)\b",
    # Superlative and definitive statements. Models hedge these away.
    "definitive": r"\b(?:one\s+of\s+the\s+(?:best|worst|largest|first|only)|is\s+the\s+only|was\s+the\s+first|the\s+best|never|always|nothing)\b",
    # Plain hedges and intensifiers. Models prefer stacked formal hedges.
    "plain_hedges": r"\b(?:very|really|pretty\s+much|perhaps|maybe|tends?\s+to|kind\s+of|sort\s+of|a\s+bit|quite)\b",
    # Wordy constructions. Concision advice kills these; humans keep them.
    "wordy_human": r"\b(?:as\s+a\s+result\s+of|in\s+order\s+to|all\s+of\s+the|a\s+part\s+of|the\s+fact\s+that|because\s+of\s+the\s+fact)\b",
    # Contractions. Absent from most default LLM registers.
    "contractions": r"\b\w+(?:'|’)(?:s|t|re|ve|ll|d|m)\b",
    # First person. Models avoid it unless asked.
    "first_person": r"\b(?:I|I'?m|I'?ve|my|we|our|us)\b",
    # Named specifics: years, exact figures, proper-noun-looking tokens.
    "years": r"\b(?:1[89]\d\d|20[0-4]\d)\b",
    "numerals": r"\b\d+(?:[.,]\d+)*\b",
    # Spelled-out quantities and named times are specificity too. A rewrite that
    # says "eleven days" and "last March" is not vague for avoiding digits.
    "spelled_numbers": r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|dozen|half|quarter|third)\b",
    "named_times": r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|morning|afternoon|evening|tonight|yesterday|today|tomorrow)\b",
}


# ===========================================================================
# 3. PHRASE PATTERNS
# ===========================================================================
# (label, regex, why it matters / what to do instead, severity)
# severity: "act" = worth an edit on one sighting
#           "weak" = only counts when other tells share the passage

PHRASES = [
    # ---- assistant residue. Strongest tell. Remove outright. -------------
    ("residue.closing", r"\b(?:I\s+hope\s+this\s+helps|hope\s+(?:that|this)\s+helps|let\s+me\s+know\s+if|feel\s+free\s+to\s+(?:ask|reach)|happy\s+to\s+(?:help|clarify|expand)|is\s+there\s+anything\s+else)\b", "delete", "act"),
    ("residue.opener", r"(?m)^\s*(?:Certainly|Absolutely|Of\s+course|Sure|Great\s+question|Excellent\s+question)[!,.:]", "delete", "act"),
    ("residue.offer", r"\b(?:would\s+you\s+like\s+me\s+to|want\s+me\s+to|should\s+I\s+continue|shall\s+I\s+(?:continue|proceed))\b", "delete", "act"),
    ("residue.praise", r"\byou'?re\s+absolutely\s+right\b", "delete", "act"),
    ("residue.breakdown", r"\bhere'?s?\s+(?:is\s+)?(?:a\s+)?(?:breakdown|detailed\s+breakdown|overview|what\s+you\s+need\s+to\s+know|the\s+deal)\b", "delete", "act"),
    ("residue.as_an_ai", r"\bas\s+an?\s+(?:AI|large)\s+language\s+model\b|\bas\s+an\s+AI\b", "delete", "act"),
    ("residue.cutoff", r"\b(?:as\s+of\s+my\s+last\s+(?:knowledge\s+)?(?:update|training)|up\s+to\s+my\s+last\s+training|my\s+training\s+data|knowledge\s+cut-?off)\b", "delete", "act"),
    ("residue.sourcegap", r"\b(?:while\s+specific\s+details\s+(?:are|remain)|not\s+(?:widely|extensively|publicly)\s+(?:documented|available|disclosed)|in\s+the\s+(?:provided|available)\s+(?:sources|search\s+results)|based\s+on\s+available\s+information)\b", "say what the source does not show, or cut the sentence", "act"),
    ("residue.lowprofile", r"\b(?:maintains?\s+a\s+low\s+profile|keeps?\s+(?:personal|private)\s+details\s+private)\b", "a guess dressed as a fact; cut", "act"),

    # ---- staging instead of stating -------------------------------------
    ("staging.not_only", r"\bnot\s+only\b[^.;!?]{2,90}?\bbut\s+(?:also\s+)?", "keep only if the negative half corrects a belief the reader holds", "act"),
    ("staging.not_just", r"\bnot\s+(?:just|merely|simply)\b[^.;!?]{2,90}?\bbut\b", "keep only if both halves carry information", "act"),
    ("staging.isnt_its", r"\b(?:it'?s|it\s+is|this\s+is|that'?s|these\s+are)\s+not\s+(?:just\s+|merely\s+|simply\s+)?[^.;!?]{2,70}[,;—-]\s*(?:it'?s|it\s+is|this\s+is|that'?s|they'?re)\b", "one clause, stated straight", "act"),
    ("staging.split_negative", r"(?:This|That|It)\s+does\s+not\s+mean\b[^.!?]{2,80}[.!?]\s+(?:It|This|That)\s+means\b", "same contrast, split across two sentences", "act"),
    ("staging.rather_than", r"\brather\s+than\s+(?:merely|simply|just)\b", "say what it does", "act"),
    ("staging.more_than_just", r"\b(?:much\s+)?more\s+than\s+(?:just|simply|merely)\b", "say what it is", "act"),
    ("staging.closer", r"(?m)^\s*(?:That\s+is\s+the\s+real\s+\w+|Read\s+that\s+again|Let\s+that\s+sink\s+in|Think\s+about\s+that)\.?\s*$", "a closer that repeats the paragraph above it", "act"),
    ("staging.deep_saying", r"\b(?:at\s+(?:its|their|the)\s+(?:core|heart)|the\s+(?:real|true|deeper|bigger|fundamental)\s+(?:question|issue|problem|point)\s+is|what\s+(?:truly|really)\s+matters|the\s+heart\s+of\s+the\s+matter|here(?:in)?\s+lies)\b", "replace the saying with the specific claim", "act"),
    ("staging.aphorism", r"\b(?:is|becomes)\s+the\s+(?:language|currency|architecture|grammar|price)\s+of\b", "state the claim", "act"),
    ("staging.runup", r"\blet'?s\s+(?:dive|delve|explore|unpack|take\s+a\s+look|break\s+(?:it|this)\s+down)\b|\bwithout\s+further\s+ado\b", "delete the run-up and make the point", "act"),
    ("staging.candor", r"(?im)^\s*(?:Honestly|Look|Here'?s\s+the\s+thing|The\s+thing\s+is|Real\s+talk|Let'?s\s+be\s+honest)[,:.?]", "only if the writer actually talks this way", "act"),
    ("staging.strawman", r"\b(?:some\s+(?:might|may|would|could)\s+(?:argue|say|claim|contend)|one\s+might\s+be\s+tempted|a\s+tempting\s+approach|an\s+obvious\s+approach\s+would|you\s+might\s+think|it\s+would\s+be\s+easy\s+to\s+just)\b", "answering an objection nobody raised", "act"),
    ("staging.disclaim", r"\b(?:don'?t\s+get\s+me\s+wrong|to\s+be\s+clear|I'?m\s+not\s+saying|this\s+is\s+not\s+to\s+say)\b", "usually a leftover from an earlier draft", "weak"),

    # ---- inflated significance -------------------------------------------
    ("inflate.testament", r"\b(?:stands?|serves?)\s+as\s+a\s+testament\b|\ba\s+testament\s+to\b", "state what it did", "act"),
    ("inflate.reminder", r"\bserves?\s+as\s+a\s+(?:stark\s+|powerful\s+|sobering\s+)?reminder\b", "cut", "act"),
    ("inflate.role", r"\b(?:plays?|played)\s+(?:a|an)\s+(?:\w+\s+)?role\b|\b(?:vital|crucial|pivotal|key|central|integral)\s+role\b", "name the action", "act"),
    ("inflate.moment", r"\b(?:a|the)\s+(?:pivotal|crucial|defining|watershed|key)\s+(?:moment|turning\s+point)\b", "state what changed", "act"),
    ("inflate.marking", r"\bmark(?:s|ed|ing)\s+(?:a|the)\s+(?:significant|major|important|pivotal|new)\b", "state what changed", "act"),
    ("inflate.broader", r"\breflect(?:s|ed|ing)?\s+(?:a\s+)?broader\b|\bpart\s+of\s+a\s+(?:broader|wider|larger)\s+(?:movement|trend|shift|pattern)\b", "state the connection or drop it", "act"),
    ("inflate.legacy", r"\b(?:enduring|lasting)\s+(?:legacy|impact|influence|relevance)\b|\bindelible\s+mark\b", "give the evidence", "act"),
    ("inflate.stage", r"\bsetting\s+the\s+stage\s+for\b|\bpaved?\s+the\s+way\s+for\b", "state the causal link or drop it", "act"),
    ("inflate.cornerstone", r"\b(?:cornerstone|bedrock|linchpin|backbone|focal\s+point)\s+of\b|\bbeacon\s+of\b", "say what it supports", "act"),
    ("inflate.era", r"\b(?:usher(?:s|ed|ing)?\s+in|herald(?:s|ed|ing)?)\s+(?:a|the)\s+new\s+(?:era|chapter|dawn|age)\b", "cut", "act"),
    ("inflate.landscape", r"\bthe\s+(?:ever-\w+\s+|evolving\s+|changing\s+)?landscape\s+of\b|\bevolving\s+landscape\b", "name the field", "act"),
    ("inflate.today", r"\b(?:in\s+)?(?:today'?s|our)\s+(?:fast-paced|rapidly\s+(?:changing|evolving)|ever-\w+|digital|modern|increasingly\s+\w+)\s+(?:world|age|era|landscape|society|environment)\b", "cut", "act"),
    ("inflate.since_time", r"\bsince\s+the\s+(?:beginning|dawn)\s+of\s+(?:time|history|humanity)\b|\bthroughout\s+history\b", "give the period", "act"),
    ("inflate.overstated", r"\bcannot\s+be\s+overstated\b|\bspeaks\s+volumes\b", "give the magnitude", "act"),
    ("inflate.more_than_ever", r"\bnow\s+more\s+than\s+ever\b", "cut", "act"),

    # ---- the challenges-and-future template ------------------------------
    ("template.despite", r"\bdespite\s+(?:these|its|those|the)\s+(?:challenges|obstacles|difficulties|limitations|setbacks)\b", "the stock pivot; rewrite or cut", "act"),
    ("template.faces", r"\bfaces?\s+(?:several|numerous|many|a\s+number\s+of|various)\s+challenges\b", "name the specific problem", "act"),
    ("template.continues", r"\bcontinues?\s+to\s+(?:thrive|evolve|grow|shape|play|serve|inspire)\b", "cut", "act"),
    ("template.future_head", r"(?im)^#{1,6}\s*(?:challenges\s+and\s+(?:legacy|future|opportunities)|future\s+(?:outlook|prospects|directions)|awards\s+and\s+recognition|legacy\s+and\s+impact)\s*$", "a template heading, not a finding", "act"),
    ("template.bright", r"\bthe\s+future\s+(?:of\s+[\w\s]{1,30}\s+)?(?:is|looks|remains)\s+(?:bright|promising|uncertain)\b|\bexciting\s+times\s+(?:ahead|lie)\b|\ba\s+step\s+in\s+the\s+right\s+direction\b", "cut; end on the last concrete fact", "act"),
    ("template.only_time", r"\bonly\s+time\s+will\s+tell\b|\bit\s+remains\s+to\s+be\s+seen\b|\bone\s+thing\s+is\s+(?:certain|clear)\b", "name the open question", "act"),
    ("template.together", r"\b(?:stakeholders?|we|society|policymakers?|all\s+parties)\s+must\s+(?:work\s+together|collaborate|come\s+together)\b", "name who does what", "act"),
    ("template.conclusion", r"(?im)^\s*(?:in\s+conclusion|to\s+conclude|in\s+summary|to\s+sum\s+up|all\s+in\s+all|in\s+closing|overall)\b[,:]", "start with the conclusion itself", "act"),

    # ---- superficial participial analysis ---------------------------------
    ("participle.tail", r",\s+(?:highlight|underscor|showcas|reflect|emphasiz|demonstrat|illustrat|reinforc|ensur|solidif|cement|signal|foster|pav|shap|driv|enabl|serv|creat|represent|offer|contribut|position|embod|evok|symboliz|celebrat|honor|resonat|cultivat|encompass|enhanc)\w*ing\b", "state the inference the source supports, or cut", "act"),

    # ---- vague attribution and borrowed authority --------------------------
    ("vague.experts", r"\b(?:experts?|researchers?|scientists?|analysts?|critics?|scholars?|observers?|commentators?|reviewers?)\s+(?:say|says|believe|believes|argue|argues|note|notes|suggest|suggests|agree|contend|maintain|have\s+cited|treat)\b", "name the source or drop the claim", "act"),
    ("vague.studies", r"\b(?:studies|research|reports?|surveys?|data|evidence|industry\s+reports?)\s+(?:show|shows|suggest|suggests|indicate|indicates|reveal|reveals|demonstrate|found|find)\b", "name the study or drop the claim", "act"),
    ("vague.widely", r"\b(?:is|are|it\s+is)\s+(?:widely|generally|commonly|often)\s+(?:believed|accepted|known|regarded|considered|understood|acknowledged)\b", "name who believes it", "act"),
    ("vague.several_sources", r"\b(?:several|multiple|various|numerous)\s+(?:sources|publications|outlets|reports)\b", "count them", "act"),
    ("vague.coverage", r"\b(?:independent|national|regional|local)\s+(?:coverage|media\s+outlets)\b|\btrade\s+publications\b|\b(?:cited|featured|profiled)\s+in\s+(?:multiple|numerous|several)\b", "name what was said, not who said it", "act"),
    ("vague.social", r"\b(?:active|strong)\s+social\s+media\s+presence\b|\bover\s+[\d,.]+\s*(?:k|m|million|thousand)?\s+followers\b", "not evidence of anything; cut", "act"),
    ("vague.association", r"\b(?:associated\s+with|in\s+association\s+with|connected\s+(?:with|to)|in\s+connection\s+with|linked\s+to|tied\s+to)\b", "name the relationship the source gives", "weak"),

    # ---- copula avoidance ---------------------------------------------------
    ("copula.serves", r"\b(?:serves?|stands?|functions?|operates?)\s+as\s+(?:a|an|the)\b", "is", "act"),
    ("copula.represents", r"\brepresents?\s+(?:a|an|the)\b", "is", "weak"),
    ("copula.boasts", r"\bboasts?\b", "has", "act"),
    ("copula.features", r"\b(?:features?|offers?|maintains?)\s+(?:a|an|four|three|two|over|more\s+than)\b", "has", "weak"),
    ("copula.refers_to", r"(?m)^[^.!?\n]{0,60}\brefers\s+to\b", "is", "weak"),
    ("copula.holds_distinction", r"\bholds?\s+the\s+distinction\s+of\b", "is", "act"),
    ("copula.ventured", r"\b(?:ventured\s+into|embarked\s+(?:on|upon)|began\s+(?:his|her|their|its)\s+(?:career|journey)\s+as)\b", "was / started", "weak"),

    # ---- sales register in neutral prose --------------------------------------
    ("sales.nestled", r"\bnestled\s+(?:in|within|among|between|amid)\b|\bin\s+the\s+heart\s+of\b", "give the location", "act"),
    ("sales.beauty", r"\b(?:breathtaking|stunning|picturesque|idyllic|must-visit|world-class)\b|\bnatural\s+beauty\b", "describe it", "act"),
    ("sales.rich", r"\brich\s+(?:cultural\s+heritage|history|tapestry|tradition|array)\b|\bdiverse\s+(?:array|range)\s+of\b", "list what is there", "act"),
    ("sales.commitment", r"\bcommitment\s+to\s+(?:excellence|quality|innovation|sustainability|its\s+\w+)\b", "cut", "act"),
    ("sales.renowned", r"\b(?:renowned|esteemed|acclaimed|celebrated|prestigious)\s+(?:for|as)?\b", "say what it is known for and to whom", "weak"),

    # ---- overclaimed coverage ---------------------------------------------------
    ("scope.comprehensive", r"\b(?:comprehensive|complete|thorough|in-depth|exhaustive)\s+(?:overview|guide|analysis|understanding|examination|exploration|look)\b", "state the actual scope", "act"),
    ("scope.all_aspects", r"\b(?:all|every)\s+(?:aspects?|facets?|dimensions?)\s+of\b", "state the actual scope", "act"),
    ("scope.wide_range", r"\ba\s+(?:wide|broad|diverse|vast)\s+(?:range|array|variety|spectrum)\s+of\b|\ba\s+(?:plethora|myriad|multitude|host)\s+of\b", "give the number or list them", "act"),
    # NOTE: "false ranges" (from X to Y...) and "synonym cycling" were retired as
    # AI indicators upstream in 2026. They are ordinary clarity questions now, not
    # authorship signals, and are deliberately not detected here.

    # ---- didactic disclaimers (older models, still appear) ---------------------
    ("didactic.note", r"\bit(?:'s|\s+is)\s+(?:important|crucial|essential|vital|worth|critical)\s+to\s+(?:note|remember|consider|mention|highlight|understand)\b", "just say it", "act"),
    ("didactic.vary", r"\bmay\s+vary\s+(?:by|depending|from)\b", "give the range", "weak"),

    # ---- stacked hedging ---------------------------------------------------------
    ("hedge.stack", r"\b(?:may|might|could|can)\s+(?:potentially|possibly|perhaps|arguably|conceivably)\b|\b(?:could|might)\s+potentially\s+possibly\b", "one hedge, the accurate one", "act"),
    ("hedge.suggests_may", r"\b(?:suggests?|indicates?)\s+that\s+[^.;!?]{0,40}\b(?:may|might|could)\s+(?:potentially|possibly)\b", "one hedge, the accurate one", "act"),
    ("hedge.tofair", r"\bto\s+be\s+fair\b|\bit'?s\s+also\s+possible\s+that\b", "keep only if the source supports the doubt", "weak"),
]


# ===========================================================================
# 4. MODEL AND MARKUP ARTIFACTS
# ===========================================================================
# These are near-proof of a copy-paste from a chat interface. Not style.

ARTIFACTS = [
    ("chatgpt.contentref", r":contentReference\[oaicite:\d+\]"),
    ("chatgpt.oai_citation", r"oai_citation"),
    ("chatgpt.citeturn", r"cite\s*turn\d+(?:search|news|file|image)\d+"),
    ("chatgpt.plusnum", r"\b[A-Z][\w .]{2,30}\+\d+(?:[A-Z][\w .]{2,30}\+\d+)+"),
    ("chatgpt.attribution", r'\{\s*[“"]attribution[”"]\s*:'),
    ("chatgpt.utm", r"utm_source=(?:openai|chatgpt\.com)"),
    ("copilot.utm", r"utm_source=copilot\.com"),
    ("grok.referrer", r"referrer=grok\.com"),
    ("grok.card", r"<grok-card|grok_render_citation_card_json"),
    ("gemini.cite", r"\[cite:\s*\d"),
    ("gemini.span", r"\[span_\d+\]\((?:start|end)_span\)"),
    ("deepseek.lenticular", r"【\d+†"),
    ("perplexity.web", r"\[(?:web|attached_file):\d+\]"),
    ("unclassified.writing_block", r":::\s*(?:writing|écriture)\s*\{"),
    ("footnote.return", r"↩"),
    ("placeholder.bracket", r"\[(?:Your\s+Name|Insert[^\]]{0,40}|Specific\s+Topic|Describe\s+the[^\]]{0,60}|link\s+to[^\]]{0,30})\]"),
    ("placeholder.caps", r"\b(?:INSERT_[A-Z_]+|PASTE_[A-Z_]+|SOURCE_[A-Z_]+|YOUR_[A-Z_]+)\b"),
    ("placeholder.date", r"\b20\d\d-[Xx]{2}-[Xx]{2}\b"),
    ("markdown.fence_lang", r"```(?:wikitext|markdown)\b"),
]


# ===========================================================================
# 5. TYPOGRAPHY
# ===========================================================================

TYPOGRAPHY = [
    ("em_dash", "—", "Not a defect by itself. Compare the rate against the writer's own sample; a 2026 study found only some models exceed professional-writer rates."),
    ("en_dash", "–", "Correct for ranges. Wrong as a sentence break."),
    ("curly_double_open", "“", "Fine if the whole document uses them. A tell only when mixed with straight quotes."),
    ("curly_double_close", "”", "Fine if consistent."),
    ("curly_apostrophe", "’", "Fine if consistent. Word, macOS and iOS produce these too."),
    ("ellipsis_char", "…", "Three periods is safer in plain text."),
    ("nbsp", " ", "Almost always a paste artifact. Replace with a normal space."),
    ("narrow_nbsp", " ", "Paste artifact. Remove."),
    ("thin_space", " ", "Paste artifact. Remove."),
    ("zero_width", "​", "Invisible. Remove."),
    ("soft_hyphen", "­", "Invisible. Remove."),
    ("arrow", "→", "Rewrite as prose unless the document uses arrows."),
    ("bullet_char", "•", "Use the document's own list syntax."),
    ("middot", "·", "Paste artifact."),
]

TRANSITIONS = [
    "moreover", "furthermore", "additionally", "consequently", "therefore",
    "thus", "hence", "however", "nevertheless", "nonetheless", "notably",
    "importantly", "significantly", "indeed", "ultimately", "overall",
    "essentially", "fundamentally", "crucially", "arguably", "similarly",
    "conversely", "accordingly", "subsequently", "meanwhile", "likewise",
]

SENT_SPLIT = re.compile(r'(?<=[.!?])["\')\]”’]*\s+(?=[A-Z"\'(\[“])')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*")


# ===========================================================================
# helpers
# ===========================================================================

def strip_code(text):
    """Blank fenced code so it is not scanned as prose. Keep line numbers."""
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"),
                  text, flags=re.S)


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def prose_paragraphs(text):
    return [p for p in paragraphs(text)
            if not re.match(r"^\s*(?:[-*+#>|]|\d+\.)", p)]


def sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    guarded = re.sub(r"\b(Mr|Mrs|Ms|Dr|Prof|St|vs|etc|Inc|Ltd|i\.e|e\.g|cf|al|Fig|No)\.",
                     r"\1<D>", text)
    return [p.replace("<D>", ".").strip()
            for p in SENT_SPLIT.split(guarded) if p.strip()]


def words(text):
    return WORD_RE.findall(text)


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def per_k(n, total):
    return round(n / total * 1000, 2) if total else 0.0


# ===========================================================================
# checks
# ===========================================================================

def check_phrases(text):
    hits = []
    for label, pat, fix, sev in PHRASES:
        flags = 0 if pat.startswith("(?") else re.I
        for m in re.finditer(pat, text, flags):
            hits.append({"label": label, "severity": sev,
                         "line": line_of(text, m.start()),
                         "match": re.sub(r"\s+", " ", m.group(0))[:95],
                         "fix": fix})
    return sorted(hits, key=lambda h: h["line"])


def check_vocab(text, total):
    counts = Counter(w.lower().replace("’", "'") for w in words(text))
    found = {w: counts[w] for w in ALL_VOCAB if counts.get(w)}
    by_era = {}
    for era, group in VOCAB.items():
        n = sum(counts.get(w, 0) for w in group if " " not in w)
        if n:
            by_era[era] = n
    total_hits = sum(found.values())
    return {"distinct": len(found), "total": total_hits,
            "per_1000w": per_k(total_hits, total),
            "by_era": by_era,
            "top": sorted(found.items(), key=lambda kv: -kv[1])[:25]}


def check_human_signals(text, total):
    out = {}
    for name, pat in HUMAN_SIGNALS.items():
        n = len(re.findall(pat, text, re.I))
        out[name] = {"count": n, "per_1000w": per_k(n, total)}
    return out


def check_artifacts(text):
    out = []
    for label, pat in ARTIFACTS:
        for m in re.finditer(pat, text):
            out.append({"label": label, "line": line_of(text, m.start()),
                        "match": m.group(0)[:70]})
    return out


def check_rhythm(text):
    sents = sentences(" ".join(prose_paragraphs(text)) or text)
    lens = [len(words(s)) for s in sents]
    lens = [n for n in lens if n > 0]
    if len(lens) < 3:
        return {"n_sentences": len(lens), "note": "too short to analyse"}
    mean = statistics.mean(lens)
    sd = statistics.pstdev(lens)
    run = best = 1
    for i in range(1, len(lens)):
        if abs(lens[i] - lens[i - 1]) <= 3:
            run += 1
            best = max(best, run)
        else:
            run = 1
    tiny = tiny_best = 0
    for n in lens:
        tiny = tiny + 1 if n < 8 else 0
        tiny_best = max(tiny_best, tiny)
    return {"n_sentences": len(lens), "mean_len": round(mean, 1),
            "median_len": statistics.median(lens), "stdev": round(sd, 2),
            "coef_var": round(sd / mean, 3) if mean else 0,
            "min": min(lens), "max": max(lens),
            # <=15 words is the measured cut point: human news prose runs
            # 32-33% short sentences, 2025 instruction-tuned models 1-4%.
            "pct_short_le15": round(100 * sum(1 for n in lens if n <= 15) / len(lens)),
            "pct_long_gt30": round(100 * sum(1 for n in lens if n > 30) / len(lens)),
            "longest_flat_run": best, "longest_tiny_run": tiny_best,
            "lengths": lens}


def check_paragraph_shape(text):
    paras = prose_paragraphs(text)
    counts = [len(sentences(p)) for p in paras]
    counts = [c for c in counts if c]
    if len(counts) < 2:
        return {"n_paragraphs": len(counts)}
    return {"n_paragraphs": len(counts), "sentences_per_para": counts,
            "mean": round(statistics.mean(counts), 1),
            "stdev": round(statistics.pstdev(counts), 2)}


def check_openers(text):
    sents = sentences(" ".join(prose_paragraphs(text)) or text)
    firsts, bigrams, trans = Counter(), Counter(), Counter()
    for s in sents:
        w = words(s)
        if w:
            firsts[w[0].lower()] += 1
            if w[0].lower() in TRANSITIONS:
                trans[w[0].lower()] += 1
        if len(w) > 1:
            bigrams[w[0].lower() + " " + w[1].lower()] += 1
    para_trans = Counter()
    for p in prose_paragraphs(text):
        w = words(p)
        if w and w[0].lower() in TRANSITIONS:
            para_trans[w[0].lower()] += 1
    return {"repeated_first_word": [kv for kv in firsts.most_common() if kv[1] >= 3][:10],
            "repeated_first_bigram": [kv for kv in bigrams.most_common() if kv[1] >= 2][:10],
            "sentence_initial_transitions": dict(trans),
            "sentence_initial_transitions_total": sum(trans.values()),
            "paragraph_initial_transitions": dict(para_trans),
            "paragraph_initial_transitions_total": sum(para_trans.values()),
            "n_sentences": len(sents)}


def check_triads(text):
    pat = re.compile(
        r"\b([A-Za-z][\w\-'’]*(?:\s+[\w\-'’]+){0,3}),\s+"
        r"([A-Za-z][\w\-'’]*(?:\s+[\w\-'’]+){0,3}),\s+"
        r"and\s+([A-Za-z][\w\-'’]*(?:\s+[\w\-'’]+){0,3})\b")
    return [{"line": line_of(text, m.start()),
             "match": re.sub(r"\s+", " ", m.group(0))[:100]}
            for m in pat.finditer(text)]


def check_typography(text, total):
    out = []
    for label, ch, note in TYPOGRAPHY:
        n = text.count(ch)
        if n:
            out.append({"label": label, "char": repr(ch), "count": n,
                        "per_1000w": per_k(n, total), "note": note})
    emoji = [c for c in text if unicodedata.category(c) == "So"]
    if emoji:
        out.append({"label": "pictographs", "char": "".join(sorted(set(emoji)))[:40],
                    "count": len(emoji), "per_1000w": per_k(len(emoji), total),
                    "note": "Remove unless the genre uses them."})
    spaced = len(re.findall(r"\s—\s", text))
    tight = len(re.findall(r"\w—\w", text))
    if spaced and tight:
        out.append({"label": "mixed_em_dash_spacing", "char": "", "count": spaced + tight,
                    "per_1000w": 0,
                    "note": f"{spaced} spaced, {tight} unspaced. Pick one and hold it."})
    if '"' in text and ("“" in text or "”" in text):
        out.append({"label": "mixed_quote_styles", "char": "", "count": 0, "per_1000w": 0,
                    "note": "Document mixes straight and curly quotes. Inconsistency is the tell, not curliness."})
    return out


def check_formatting(text):
    out = {}
    bold = re.findall(r"\*\*[^*\n]{1,80}\*\*", text)
    out["bold_spans"] = len(bold)
    out["bold_examples"] = [b[:48] for b in bold[:6]]
    heads = re.findall(r"(?m)^(#{1,6})\s+(.+?)\s*$", text)
    out["headings"] = len(heads)
    out["title_case_headings"] = [
        h for _, h in heads
        if len(h.split()) >= 3
        and len([w for w in h.split() if w[:1].isupper()]) >= 3][:8]
    out["emoji_headings"] = [
        h for _, h in heads
        if any(unicodedata.category(c) == "So" for c in h)][:6]
    levels = [len(h) for h, _ in heads]
    out["skips_h2"] = bool(levels) and 3 in levels and 2 not in levels
    out["h1_count"] = levels.count(1)
    out["list_items"] = len(re.findall(r"(?m)^\s*(?:[-*+]|\d+\.)\s+\S", text))
    out["bold_led_bullets"] = len(re.findall(r"(?m)^\s*(?:[-*+]|\d+\.)\s+\*\*[^*\n]{1,60}\*\*\s*:", text))
    out["thematic_breaks"] = len(re.findall(r"(?m)^\s*(?:---+|\*\*\*+|___+)\s*$", text))
    out["prose_paragraphs"] = len(prose_paragraphs(text))
    # heading immediately restated by a one-line paragraph
    echo = 0
    for m in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*\n+([^\n#].{0,90})\n", text):
        head_words = set(w.lower() for w in words(m.group(1)))
        body_words = set(w.lower() for w in words(m.group(2)))
        if head_words and len(head_words & body_words) >= max(1, len(head_words) // 2) \
                and len(words(m.group(2))) <= 12:
            echo += 1
    out["heading_echoes"] = echo
    return out


NOMINAL_SUFFIX = re.compile(
    r"\b\w{4,}(?:tions?|sions?|ments?|nesses|ness|ities|ity|ances?|ences?|isms?|"
    r"izations?|isations?|ivity|ologies|ology|ancy|ency)\b", re.I)

# Verbs that carry no action, typical of nominalised prose: the work has moved
# into the noun and the verb is left holding the sentence together.
LIGHT_VERB = re.compile(
    r"\b(?:provide[sd]?|providing|conduct(?:s|ed|ing)?|perform(?:s|ed|ing)?|"
    r"undertake[sn]?|achiev(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|"
    r"implement(?:s|ed|ing)?|utiliz(?:e|es|ed|ing)|enabl(?:e|es|ed|ing)|"
    r"ensur(?:e|es|ed|ing)|involv(?:e|es|ed|ing)|constitut(?:e|es|ed|ing))\b", re.I)


# Reinhart et al., PNAS 2025, measured these against matched human corpora.
# Ratios are GPT-4o over human rate, with paired Cohen's d.
#   present participial clauses   5.3x   d = 1.38   <- largest single effect
#   'that' clause as subject      2.6x   d = 0.77
#   nominalizations               2.1x   d = 1.23
#   phrasal coordination          1.9x   d = 0.81
#   agentless passive             ~0.5x             <- models use LESS
PARTICIPIAL = re.compile(
    r"(?:^|[,;]\s+|\.\s+)(?:[A-Z]?[a-z]+ing)\b(?=\s+(?:the|a|an|his|her|its|their|to|in|on|with|at|from|into|for|toward))",
    re.M)
THAT_SUBJECT = re.compile(
    r"\bThat\s+\w+(?:\s+\w+){0,6}\s+(?:is|was|are|were|means|suggests|matters)\b|"
    r"\bThe\s+fact\s+that\b", re.I)
PHRASAL_COORD = re.compile(
    r"\b\w+\s+and\s+\w+\s+(?:of|in|for|to|with)\b|"
    r"\b(?:\w+ly)\s+and\s+(?:\w+ly)\b")
AGENTLESS_PASSIVE = re.compile(
    r"\b(?:is|are|was|were|been|being|be)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b(?!\s+by\b)", re.I)
MODALS = re.compile(r"\b(?:will|would|might|could|should|must|shall|may|can)\b", re.I)
# Function words that AIGT is LESS likely to contain (Tercon & Dobrovoljc 2025).
UNDERUSED_FUNCTION = re.compile(
    r"\b(?:however|but|although|because|if|when|though|whereas|unless|since)\b", re.I)
SENSING_VERBS = re.compile(
    r"\b(?:say|says|said|saw|see|sees|look|looks|looked|hear|hears|heard|"
    r"read|reads|feel|feels|felt|smell|smelled|touch|touched)\b", re.I)
RHETORICAL_Q = re.compile(r"\?")


def check_syntax(text, total):
    """Grammatical features with published human/model effect sizes."""
    sents = sentences(" ".join(prose_paragraphs(text)) or text)
    return {
        "participial_clauses": len(PARTICIPIAL.findall(text)),
        "participial_per_1000w": per_k(len(PARTICIPIAL.findall(text)), total),
        "that_subject": len(THAT_SUBJECT.findall(text)),
        "phrasal_coord": len(PHRASAL_COORD.findall(text)),
        "agentless_passive": len(AGENTLESS_PASSIVE.findall(text)),
        "agentless_passive_per_1000w": per_k(len(AGENTLESS_PASSIVE.findall(text)), total),
        "modals": len(MODALS.findall(text)),
        "modals_per_1000w": per_k(len(MODALS.findall(text)), total),
        "underused_function_words": len(UNDERUSED_FUNCTION.findall(text)),
        "underused_function_per_1000w": per_k(len(UNDERUSED_FUNCTION.findall(text)), total),
        "sensing_verbs_per_1000w": per_k(len(SENSING_VERBS.findall(text)), total),
        "questions": sum(1 for x in sents if x.rstrip().endswith("?")),
    }


def check_density(text, total):
    """Noun-heavy, informationally dense register.

    Instruction-tuned models drift toward a nominalised explanatory style and
    apply it across genres. High density is correct in some genres (legal analysis,
    policy writing) and wrong in most others, so this is a prompt to reread,
    never a target.
    """
    noms = NOMINAL_SUFFIX.findall(text)
    lights = LIGHT_VERB.findall(text)
    preps = len(re.findall(r"\b(?:of|for|with|by|through|within|regarding|"
                           r"concerning|via|upon)\b", text, re.I))
    # chains of three or more prepositional phrases: "the implementation of the
    # provision of services for the improvement of outcomes"
    chains = len(re.findall(
        r"\b\w+\s+of\s+(?:the\s+|a\s+)?\w+\s+(?:of|for|in)\s+(?:the\s+|a\s+)?\w+\s+"
        r"(?:of|for|in)\b", text, re.I))
    return {"nominalizations": len(noms),
            "nominalizations_per_1000w": per_k(len(noms), total),
            "top_nominalizations": Counter(n.lower() for n in noms).most_common(10),
            "light_verbs": len(lights),
            "light_verbs_per_1000w": per_k(len(lights), total),
            "prepositions_per_1000w": per_k(preps, total),
            "of_chains": chains}


# ===========================================================================
# OVER-CORRECTION
# ===========================================================================
# The second template: what prose looks like after a humanising pass has been
# applied too hard. Found by blind review of this skill's own output. These
# read as intelligent, which is why they survive review.

META_EVIDENTIAL = re.compile(
    r"\b(?:what\s+(?:can|could)\s+be\s+said|"
    r"(?:telling|distinguishing)\s+(?:the\s+two|them)\s+apart|"
    r"(?:that|this)\s+(?:is|would\s+be)\s+(?:a\s+)?(?:claim|question)\s+about|"
    r"(?:has|with)\s+the\s+advantage\s+of\s+being\s+checkable|"
    r"before\s+(?:this|the)\s+argument\s+goes|"
    r"the\s+(?:evidence|data|sources?)\s+(?:here\s+)?(?:does|do)\s+not|"
    r"(?:needs|requires|would\s+need)\s+(?:data|figures|evidence|numbers)\s+"
    r"(?:this|that|which)\b|"
    r"which\s+is\s+itself\s+(?:a\s+sort\s+of\s+)?(?:a\s+)?finding|"
    r"I\s+have\s+no\s+(?:clean\s+)?answer)\b", re.I)

PREEMPTIVE_CRITIQUE = re.compile(
    r"\b(?:that\s+sounds?\s+(?:glib|grand|abstract|obvious)|"
    r"I\s+know\s+how\s+(?:that|this)\s+(?:sounds|reads)|"
    r"which\s+sounds?\s+like\s+a\s+(?:dodge|cop-?out)|"
    r"to\s+put\s+that\s+less\s+(?:grandly|abstractly))\b", re.I)

CONTRARIAN_NO_OPPONENT = re.compile(
    r"\b(?:and\s+most\s+do\s+not|which\s+(?:almost\s+)?(?:nobody|no\s+one)\s+"
    r"(?:says|admits|mentions|notices)|contrary\s+to\s+what\s+(?:people|most)|"
    r"everyone\s+(?:says|assumes|thinks)\s+\w+,?\s+but|"
    r"the\s+(?:usual|standard|received)\s+(?:advice|story|view)\s+is\s+wrong)\b", re.I)

VOICE_TEMPLATE = re.compile(
    r"\b(?:load-?bearing|downstream\s+of|the\s+thing\s+about\s+\w+\s+is|"
    r"is\s+doing\s+a\s+lot\s+of\s+work|which\s+is\s+the\s+whole\s+point|"
    r"that\s+turns\s+out\s+to\s+be|and\s+that\s+is\s+fine)\b", re.I)


def check_overcorrection(text, total):
    """Tells of a humanising pass applied too hard."""
    paras = prose_paragraphs(text)
    # a short, quotable sentence closing a paragraph, over and over
    punchy_endings = 0
    for p in paras:
        ss = sentences(p)
        if len(ss) >= 2 and len(words(ss[-1])) <= 9:
            punchy_endings += 1
    return {
        "meta_evidential": [re.sub(r"\s+", " ", m.group(0))[:70]
                            for m in META_EVIDENTIAL.finditer(text)],
        "preemptive_critique": [m.group(0)[:60]
                                for m in PREEMPTIVE_CRITIQUE.finditer(text)],
        "contrarian_no_opponent": [m.group(0)[:60]
                                   for m in CONTRARIAN_NO_OPPONENT.finditer(text)],
        "voice_template": [m.group(0)[:60] for m in VOICE_TEMPLATE.finditer(text)],
        "punchy_paragraph_endings": punchy_endings,
        "n_paragraphs": len(paras),
    }


def check_closers(text):
    """One-sentence paragraphs that restate the paragraph above them."""
    paras = prose_paragraphs(text)
    out = []
    for i, p in enumerate(paras[1:], start=1):
        sents = sentences(p)
        if len(sents) == 1 and len(words(p)) <= 14:
            prev = set(w.lower() for w in words(paras[i - 1]))
            here = set(w.lower() for w in words(p))
            content = {w for w in here if len(w) > 4}
            overlap = content & prev
            out.append({"text": p[:80],
                        "echoes_previous": len(overlap) >= max(1, len(content) // 3)})
    return out


def check_repetition(text, total):
    w = [x.lower() for x in words(text)]
    grams = Counter(tuple(w[i:i + 4]) for i in range(len(w) - 3))
    rep = [(" ".join(g), c) for g, c in grams.most_common(15) if c >= 2]
    return {"repeated_4grams": rep[:10],
            "type_token_ratio": round(len(set(w)) / len(w), 3) if w else 0,
            "unique_words": len(set(w)), "total_words": total}


def analyse(raw):
    text = strip_code(raw)
    tw = len(words(text))
    return {"version": VERSION, "total_words": tw,
            "artifacts": check_artifacts(raw),
            "phrases": check_phrases(text),
            "vocab": check_vocab(text, tw),
            "human_signals": check_human_signals(text, tw),
            "density": check_density(text, tw),
            "syntax": check_syntax(text, tw),
            "closers": check_closers(text),
            "overcorrection": check_overcorrection(text, tw),
            "rhythm": check_rhythm(text),
            "paragraph_shape": check_paragraph_shape(text),
            "openers": check_openers(text),
            "triads": check_triads(text),
            "typography": check_typography(text, tw),
            "formatting": check_formatting(text),
            "repetition": check_repetition(text, tw)}


# ===========================================================================
# rendering
# ===========================================================================

def render(r, name=""):
    L, add = [], None
    L = []
    def add(s=""):
        L.append(s)
    tw = r["total_words"]
    add("=" * 72)
    add(f"SCAN {name}  ({tw} words)".rstrip())
    add("=" * 72)
    add("Counts, not verdicts. Every hit needs a human decision.")
    add("Fix structure before wording: surface edits leave the shape of the")
    add("reasoning unchanged, and the shape is what a reader notices.")
    add("")

    art = r["artifacts"]
    add(f"[0] PASTE ARTIFACTS: {len(art)}")
    if art:
        for a in art[:15]:
            add(f"    L{a['line']:<5} {a['label']:<26} {a['match']}")
        add("    These are not style. Delete them before anything else.")
    else:
        add("    none")
    add("")

    ph = r["phrases"]
    act = [h for h in ph if h["severity"] == "act"]
    weak = [h for h in ph if h["severity"] == "weak"]
    add(f"[1] STOCK PHRASES: {len(act)} act-on-sight, {len(weak)} weak-alone"
        f"  ({per_k(len(ph), tw)} per 1000 words)")
    for h in act[:35]:
        add(f"    L{h['line']:<5} {h['match']}")
        add(f"    {'':<6} -> {h['fix']}")
    if len(act) > 35:
        add(f"    ... {len(act) - 35} more")
    if weak:
        add(f"    weak-alone (act only if other tells share the passage): "
            f"{', '.join(sorted({h['label'] for h in weak}))}")
    if ph:
        top = Counter(h["label"] for h in ph).most_common(6)
        add(f"    most frequent: {', '.join(f'{k}({v})' for k, v in top)}")
    add("")

    v = r["vocab"]
    add(f"[2] MODEL-WEIGHTED VOCABULARY: {v['total']} tokens, {v['distinct']} distinct"
        f"  ({v['per_1000w']} per 1000 words)")
    if v["top"]:
        add("    " + ", ".join(f"{w}({c})" for w, c in v["top"]))
        add(f"    by era: {v['by_era']}")
    add("    No word here is banned. A high rate means the draft reaches for")
    add("    the same register everywhere instead of choosing per sentence.")
    add("")

    hs = r["human_signals"]
    add("[3] HUMAN-SIGNAL COUNTERS  (per 1000 words)")
    add("    These are constructions more common in human prose than in model")
    add("    output. Standard concision advice deletes most of them. Do not")
    add("    let a rewrite drive these to zero.")
    for k in ["plain_copula", "plain_verbs", "definitive", "plain_hedges",
              "wordy_human", "contractions", "first_person", "years", "numerals",
              "spelled_numbers", "named_times"]:
        d = hs[k]
        add(f"    {k:<16} {d['count']:>4}   {d['per_1000w']:>7}")
    if hs["plain_copula"]["per_1000w"] < 8:
        add("    ! Very few plain is/are/has constructions. Check whether they were")
        add("      replaced by serves as / stands as / represents.")
    specifics = (hs["numerals"]["count"] + hs["years"]["count"]
                 + hs["spelled_numbers"]["count"] + hs["named_times"]["count"])
    if specifics == 0 and tw > 200:
        add("    ! No dates, figures or measurements anywhere. Specificity is the")
        add("      cheapest thing a model leaves out. Add only what the source has.")
    add("")

    rh = r["rhythm"]
    add("[4] SENTENCE RHYTHM")
    if rh.get("n_sentences", 0) >= 3:
        add(f"    n={rh['n_sentences']}  mean {rh['mean_len']}  median {rh['median_len']}"
            f"  range {rh['min']}-{rh['max']}  stdev {rh['stdev']}  coef.var {rh['coef_var']}")
        add(f"    short (<=15w) {rh['pct_short_le15']}%      long (>30w) {rh['pct_long_gt30']}%")
        add("      reference: human news prose runs 32-33% short sentences;")
        add("      2025 instruction-tuned models run 1-4%. (Gude et al. 2026)")
        add(f"    longest run of near-equal sentences: {rh['longest_flat_run']}")
        add(f"    lengths: {rh['lengths']}")
        if rh["pct_short_le15"] < 12:
            add("    ! Almost no short sentences. This is the clearest measured gap")
            add("      between aligned models and human prose. Do not fix it by")
            add("      chopping sentences in half. Find the places where the content")
            add("      already wanted to stop, and stop there.")
        if rh["longest_flat_run"] >= 5:
            add("    ! Five or more consecutive sentences of near-identical length.")
        if rh.get("longest_tiny_run", 0) >= 4:
            add(f"    ! {rh['longest_tiny_run']} consecutive sentences under 8 words.")
            add("      A run of fragments reads as manufactured emphasis, which is")
            add("      its own template. A high share of short sentences on its own")
            add("      is fine, and normal in conversational registers.")
        add("      No peer-reviewed source gives a target standard deviation for")
        add("      sentence length. Treat stdev and coef.var as description only.")
    else:
        add("    too short to analyse")
    add("")

    dn = r["density"]
    add("[4b] REGISTER DENSITY")
    add(f"    nominalisations {dn['nominalizations']:>4}  ({dn['nominalizations_per_1000w']}/1k)"
        f"   light verbs {dn['light_verbs']:>3}  ({dn['light_verbs_per_1000w']}/1k)")
    add(f"    prepositions {dn['prepositions_per_1000w']}/1k   of-chains {dn['of_chains']}")
    if dn["top_nominalizations"]:
        add(f"    most common: {', '.join(f'{w}({c})' for w, c in dn['top_nominalizations'][:8])}")
    if dn["nominalizations_per_1000w"] > 55:
        add("    ! Noun-heavy register. Instruction-tuned models drift toward this")
        add("      and apply it to every genre. Correct for policy and legal prose,")
        add("      wrong for most else. Put the action back in the verb where the")
        add("      sentence is about someone doing something.")
    if dn["of_chains"] >= 2:
        add(f"    ! {dn['of_chains']} chains of three or more 'of' phrases.")
    add("")

    sx = r["syntax"]
    add("[4c] GRAMMATICAL FEATURES WITH MEASURED EFFECT SIZES")
    add("     Reinhart et al. (PNAS 2025) compared instruction-tuned models with")
    add("     matched human corpora. Ratios below are model over human rate.")
    add(f"    participial clauses      {sx['participial_clauses']:>4}"
        f"  ({sx['participial_per_1000w']}/1k)   models run 5.3x human, d=1.38")
    add(f"    'that' clause as subject {sx['that_subject']:>4}"
        f"                 models run 2.6x human, d=0.77")
    add(f"    phrasal coordination     {sx['phrasal_coord']:>4}"
        f"                 models run 1.9x human, d=0.81")
    add(f"    agentless passive        {sx['agentless_passive']:>4}"
        f"  ({sx['agentless_passive_per_1000w']}/1k)   models run about HALF human")
    add(f"    modal verbs              {sx['modals']:>4}  ({sx['modals_per_1000w']}/1k)")
    add(f"    however/but/although/... {sx['underused_function_words']:>4}"
        f"  ({sx['underused_function_per_1000w']}/1k)")
    add(f"    sensing verbs (say/see/hear/feel)  ({sx['sensing_verbs_per_1000w']}/1k)")
    add(f"    questions                {sx['questions']:>4}"
        f"                 models ask ~half the human rate")
    if sx["participial_per_1000w"] > 12:
        add("    ! High participial-clause rate. This is the single largest measured")
        add("      grammatical gap. Turn the strongest ones into finite clauses.")
    add("    ! Note the direction on passives. Aligned models use agentless passive")
    add("      LESS than humans, so 'avoid the passive' is the wrong correction here.")
    add("      Change a passive only when it hides an actor who matters.")
    add("")

    cl = r["closers"]
    echoing = [c for c in cl if c["echoes_previous"]]
    add(f"[4e] ONE-LINE CLOSERS: {len(cl)} short standalone paragraphs, "
        f"{len(echoing)} echo the paragraph above")
    for c in echoing[:6]:
        add(f"    {c['text']}")
    if echoing:
        add("    ! A closer that repeats adds emphasis without adding anything.")
        add("      Cut it, or give it something the reader does not already have.")
    add("")

    pg = r["paragraph_shape"]
    add("[5] PARAGRAPH SHAPE")
    if pg.get("n_paragraphs", 0) >= 2:
        add(f"    {pg['n_paragraphs']} prose paragraphs, sentences each: {pg['sentences_per_para']}")
        add(f"    mean {pg['mean']}  stdev {pg['stdev']}")
        if pg["stdev"] < 0.6 and pg["n_paragraphs"] >= 4:
            add("    ! Near-identical paragraph lengths. Check whether each paragraph")
            add("      also runs the same internal template: claim, two examples,")
            add("      significance sentence, transition.")
    else:
        add("    too few prose paragraphs to analyse")
    add("")

    op = r["openers"]
    add("[6] OPENINGS")
    add(f"    sentence-initial transition adverbs: {op['sentence_initial_transitions_total']}"
        f"  {op['sentence_initial_transitions'] or ''}")
    add(f"    paragraph-initial transition adverbs: {op['paragraph_initial_transitions_total']}"
        f"  {op['paragraph_initial_transitions'] or ''}")
    if op["repeated_first_word"]:
        add(f"    repeated first words: {op['repeated_first_word']}")
    if op["repeated_first_bigram"]:
        add(f"    repeated first bigrams: {op['repeated_first_bigram']}")
    if op["paragraph_initial_transitions_total"] >= 2:
        add("    ! Paragraphs joined by adverbs rather than by argument. Name the")
        add("      actual relationship, or use no connective at all.")
    add("")

    tr = r["triads"]
    add(f"[7] THREE-ITEM LISTS: {len(tr)}")
    for t in tr[:10]:
        add(f"    L{t['line']:<5} {t['match']}")
    if len(tr) >= 3:
        add("    ! Three is a real number. It is also the number reached for when")
        add("      the writer does not know how many items there are. For each one,")
        add("      check that all three items carry a distinct idea.")
    add("")

    ty = r["typography"]
    add("[8] TYPOGRAPHY AND INVISIBLE CHARACTERS")
    if ty:
        for t in ty:
            add(f"    {t['label']:<24}{t['count']:>4}  {t['per_1000w']:>6}/1k")
            add(f"    {'':<24}      {t['note']}")
    else:
        add("    clean")
    add("")

    fm = r["formatting"]
    add("[9] FORMATTING")
    add(f"    headings {fm['headings']}  bold spans {fm['bold_spans']}"
        f"  list items {fm['list_items']}  prose paragraphs {fm['prose_paragraphs']}"
        f"  rules {fm['thematic_breaks']}")
    if fm["title_case_headings"]:
        add(f"    ! Title Case headings: {fm['title_case_headings']}")
        add("      Most publications use sentence case.")
    if fm["emoji_headings"]:
        add(f"    ! Emoji in headings: {fm['emoji_headings']}")
    if fm["bold_led_bullets"] >= 3:
        add(f"    ! {fm['bold_led_bullets']} bullets open with a bold label and a colon.")
        add("      This is the strongest formatting tell in anything meant as prose.")
    if fm["bold_spans"] >= 6:
        add(f"    ! {fm['bold_spans']} bold spans. Bold marks the exception, not the argument.")
    if fm["heading_echoes"]:
        add(f"    ! {fm['heading_echoes']} heading(s) restated by the line below them.")
    if fm["thematic_breaks"] >= 3:
        add(f"    ! {fm['thematic_breaks']} horizontal rules. A markdown-output habit.")
    if fm["skips_h2"]:
        add("    ! Document starts sections at level 3 with no level 2.")
    if fm["h1_count"] >= 2:
        add(f"    ! {fm['h1_count']} level-1 headings.")
    if fm["list_items"] > 2 * fm["prose_paragraphs"] and fm["list_items"] > 8:
        add("    ! Far more list items than prose paragraphs. Check whether the")
        add("      lists are carrying reasoning that belongs in sentences.")
    add("")

    oc = r["overcorrection"]
    total_oc = (len(oc["meta_evidential"]) + len(oc["preemptive_critique"])
                + len(oc["contrarian_no_opponent"]) + len(oc["voice_template"]))
    add("[9b] OVER-CORRECTION (the second template)")
    add("     Only meaningful on a rewrite. These read as intelligent, which is")
    add("     why they survive review.")
    for k, label in [("meta_evidential", "evidence-about-evidence"),
                     ("preemptive_critique", "pre-emptive self-critique"),
                     ("contrarian_no_opponent", "contrarian, no opponent named"),
                     ("voice_template", "voice by template")]:
        if oc[k]:
            add(f"    {label}: {len(oc[k])}")
            for h in oc[k][:4]:
                add(f"      {h}")
    if oc["n_paragraphs"] >= 4:
        share = round(100 * oc["punchy_paragraph_endings"] / oc["n_paragraphs"])
        add(f"    paragraphs ending on a short quotable line: "
            f"{oc['punchy_paragraph_endings']}/{oc['n_paragraphs']} ({share}%)")
        if share >= 60:
            add("    ! Aphorism on a schedule. One is a good instinct; five is a")
            add("      rhythm, and a reader who notices the rhythm sees the machinery.")
    if total_oc == 0 and oc["n_paragraphs"] >= 4:
        add("    no lexical over-correction markers")
    add("    Substance gate: count concrete claims in the original and in this")
    add("    rewrite. Fewer here means the edit failed, unless cuts were asked for.")
    add("")

    rp = r["repetition"]
    add("[10] REPETITION")
    add(f"    type-token ratio {rp['type_token_ratio']}"
        f"  ({rp['unique_words']} unique / {rp['total_words']} total)")
    if rp["repeated_4grams"]:
        add("    repeated 4-grams:")
        for g, c in rp["repeated_4grams"]:
            add(f"      {c}x  {g}")
    add("")
    add("=" * 72)
    return "\n".join(L)


SUMMARY_HEADER = (
    "  short%  = sentences of 15 words or fewer. Human news prose 32-33%;\n"
    "            2025 instruction-tuned models 1-4%.\n"
    "  nom/1k  = nominalisations per 1000 words.\n"
    "  ptcp/1k = participial clauses per 1000 words. Models run 5.3x human.\n"
    "  para sd = spread of paragraph lengths. Near zero means one template.\n"
    "  spec    = dates, figures, quantities, named times. Zero is a warning.\n"
    "  No column has a target value. Compare drafts; do not chase numbers.\n\n"
    f"{'file':<20}{'words':>6}{'stock':>6}{'vocab':>7}{'short%':>8}"
    f"{'nom/1k':>8}{'ptcp/1k':>9}{'para sd':>9}{'spec':>6}{'artf':>6}\n"
    + "-" * 85)


def summary_row(r, name):
    ph = r["phrases"]
    rh = r["rhythm"]
    hs = r["human_signals"]
    spec = (hs["numerals"]["count"] + hs["years"]["count"]
            + hs["spelled_numbers"]["count"] + hs["named_times"]["count"])
    return (f"{name[:19]:<20}{r['total_words']:>6}"
            f"{len([h for h in ph if h['severity'] == 'act']):>6}"
            f"{r['vocab']['per_1000w']:>7}"
            f"{rh.get('pct_short_le15', 0):>7}%"
            f"{r['density']['nominalizations_per_1000w']:>8}"
            f"{r['syntax']['participial_per_1000w']:>9}"
            f"{r['paragraph_shape'].get('stdev', 0):>9}"
            f"{spec:>6}{len(r['artifacts']):>6}")


def emit(s):
    try:
        print(s)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(s.encode("utf-8", "replace") + b"\n")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="files to scan, or - for stdin")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary", action="store_true",
                    help="one line per file, for comparing drafts")
    a = ap.parse_args()

    results = []
    for p in a.paths:
        raw = sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
        results.append((p, analyse(raw)))

    if a.json:
        emit(json.dumps({p: r for p, r in results}, indent=2, ensure_ascii=False))
    elif a.summary:
        emit(SUMMARY_HEADER)
        for p, r in results:
            emit(summary_row(r, p.split("/")[-1].split("\\")[-1]))
    else:
        for p, r in results:
            emit(render(r, p if len(results) > 1 else ""))


if __name__ == "__main__":
    main()

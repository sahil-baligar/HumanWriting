# Quoting a supplied work

Load this when the writer has supplied a text (a novel, a play, an article, a chapter, a
poem, a transcript) and wants an essay or response that quotes from it. The short version
is in SKILL.md. This file covers the cases that come up in practice.

The rule does not bend. A quotation is evidence, and the reader is trusting that the words
between the marks are the author's. One altered word turns evidence into fabrication.

## What "exact" means

Everything between the quotation marks matches the supplied text character for character.

| Keep exactly as printed | Why it matters |
|---|---|
| Spelling, including British, archaic, dialect, and the author's own errors | *colour*, *shew*, *'tis*, *ain't* are the author's choices |
| Capital letters | A capital can be the point: *Nature*, *the Party* |
| Punctuation, including dashes, semicolons, colons | The punctuation rule does not apply inside quotations |
| Apostrophe and quote characters (’ vs ') | Copy the character the source uses |
| Italics and emphasis | Reproduce them. If you cannot, say *emphasis in original* |
| Numbers as words or digits | *twenty-one* and *21* are different text |

Line breaks from a PDF or a hard-wrapped file are not part of the text. Join the lines.
Watch for a hyphen that exists only because a word was split across a line (*remem-
bered*). If the word is one word in the printed book, join it without the hyphen. If you
are unsure, check the page image or ask.

## Fitting a quotation into a sentence

Build the sentence around the quotation.

> ✗ Okafor says the harbour "swallowed boats one by one" (Okafor, 42).
> *(source: "a grey mouth that swallowed the boats one by one")*

The source has *the boats*. Dropping *the* is an alteration.

> ✓ Okafor describes the harbour as "a grey mouth that swallowed the boats one by one"
> (Okafor, 42).

> ✓ The harbour "swallowed the boats one by one" (Okafor, 42).

Choose a contiguous run of words. If the part you need is broken up by material you do not
want, use two short quotations with your own words between them, each cited, rather than
splicing.

Do not use brackets or ellipses to repair a quotation into fitting. They are legitimate in
academic style, but they are exactly where alterations hide, and this rule is stricter than
general style. If the writer's course or style guide requires them and the writer asks for
them, follow the guide and mark every change.

A quotation must not start or end in the middle of a word.

## The citation

Directly after the closing quotation mark, a space, then parentheses holding the author's
surname, a comma, and the page number. The sentence's full stop comes after the
parenthesis.

> "a grey mouth that swallowed the boats one by one" (Okafor, 42).

- **Author.** The surname as the source prints it. For an edited collection, the author of
  the piece being quoted, not the editor.
- **Page.** The page in the copy the writer supplied, since that is the copy you checked
  against. A span across two pages is written *42-43*.
- **Every quotation gets its own citation**, even when several in a row come from the same
  page. Repetition is fine. A missing citation is not.
- If the writer asks for a different citation style (MLA without the comma, APA with the
  year, Chicago footnotes), use theirs. The exact-text rule does not change.

## Pages you cannot find

- **The source has no page numbers** (a web page, an e-book file, a pasted excerpt). Do not
  invent them. Ask the writer which edition they are citing, or use a locator the source
  really has (chapter, paragraph, line, act and scene) and say you did so.
- **You cannot tell which page a passage falls on**, for example in extracted text where the
  page breaks were lost. Cite `(Author, page ?)` and say so in your note. Never guess.
- **The printed page number differs from the PDF page number**, because of front matter.
  Cite the printed number. With the verifier, pass `--page-offset` equal to the PDF page
  minus the printed page.

## Paraphrase

A paraphrase has no quotation marks and is in your own words throughout. It can still take
a citation, and in an essay about a text it usually should. Do not write a paraphrase that
keeps a distinctive phrase of the author's without quoting it. Either quote the phrase
exactly or rephrase it fully.

## Checking

Before returning the essay, check every quotation against the source one at a time. Do not
check from memory of the text, because memory is where the small substitutions come from.

When the source is available as a file:

```bash
pdftotext -layout book.pdf book.txt                        # if the source is a PDF
python scripts/verify_quotes.py essay.md book.txt           # text and citations
python scripts/verify_quotes.py essay.md book.txt --pages   # also check page numbers
```

The verifier reports each quotation as one of:

| Status | Meaning |
|---|---|
| `exact` | Found in the source, character for character |
| `typography` | Found only if quote marks, apostrophes, or dashes are normalised. Copy the source's characters |
| `not found` | Not in the source. It shows the closest passage so you can see what changed |
| `no citation` | Found, but not followed by (Author, page) |
| `wrong page` | Found on a different page from the one cited |
| `short` | Under three words. Treated as a scare quote or title and not failed |

Any status other than `exact` or `short` is a failure, and the script exits with status 1.
Fix every failure before returning the essay. If a quotation cannot be made to match,
turn it into a cited paraphrase or cut it.

## What to tell the writer

In the note that goes with the essay, list any quotation you could not verify, any page you
could not determine, and any place where you paraphrased instead of quoting because the
exact text did not fit. Do not bury these. They are the things the writer needs to check
before handing the essay in.

# Reviewing a Machaque unit

You are a native-level Peninsular Spanish teacher reviewing one unit of drill items written by someone else. Read `/home/claude/machaque/WRITING.md` (the rules the writer followed) and then the unit file you were given. Fix problems **directly in that file**; change nothing else.

Check every item:
1. Every accepted answer is grammatical, natural Spain Spanish and actually means the English prompt. Remove or fix wrong ones.
2. Missing accepted answers: add any natural translation a competent Spain speaker would plausibly type that respects the cue (synonyms, word order, pronoun placement, optional words). This matters most: a correct answer marked wrong is the learner's biggest frustration. Don't add variants that differ only in capitalization, punctuation, accents, subject pronouns, or -se/-ra (the checker already ignores those).
3. Ambiguous prompts: if "you" or the verb is open, add or fix the cue. If an English sentence could fairly be translated with a different mood or tense, either add that answer or rewrite the English so only one reading fits.
4. Gap items: the context must force the expected form; if another form is also correct, add it to the answers or change the sentence.
5. Multiple choice: the first option is correct and NO other option is also correct. Replace any defensible distractor.
6. Notes are one line, in Spanish, and true.
7. `fs`/`fe`: every accepted answer must start with fs and end with fe exactly.

Afterwards run the import check:
`cd /home/claude/machaque && python3 -c "import sys; sys.path.insert(0,'units'); import uNN; print(len(uNN.UNIT['items']))"`

Reply in under 120 words: how many items you changed, and the most notable fixes.

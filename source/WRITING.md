# Machaque: how to write a unit

You are writing drill items for a personal Spanish app for one advanced learner (B1+ → C1, American, finished Duolingo). The app is text-only. It drills one grammatical structure per unit, hard and repetitively, with many variations: every person (yo, tú, él/ella/usted, nosotros, **vosotros**, ellos/ustedes), affirmative/negative, statements and questions, varied verbs (regular, stem-changing, irregular: ser, ir, haber, hacer, tener, poner, venir, decir, saber, poder, salir, traer, conocer, oír, caber, dar, estar…).

The model to imitate is `/home/claude/machaque/items.py` (units 33 and 35, already reviewed). Read it first. Use the same helper functions.

## Output

Write ONE file: `/home/claude/machaque/units/uNN.py` (two-digit unit number), containing exactly:

```python
from items import T, G, M
UNIT = {
    "n": NN,
    "title": "<a short model sentence in Spanish, like 'Espero que lleguéis a tiempo'>",
    "struct": "<the structure in a few Spanish words>",
    "note": "<default one-line feedback in Spanish explaining the rule>",
    "items": [ ... 50 items ... ],
}
```

Then run `cd /home/claude/machaque && python3 -c "import sys; sys.path.insert(0,'units'); import uNN; print(len(uNN.UNIT['items']))"` to make sure it imports.

## Item types (mix: about 32 T, 10 G, 8 M)

- `T(english_prompt, accepted, cue="", note="", w=False, fs="", fe="")` — translate English → Spanish.
  - `accepted` is a list of every natural correct Spanish answer, first = the model answer. Be thorough: synonyms (coger/tomar, acabar/terminar, enfadarse/molestarse where natural), word-order variants, pronoun placement variants (se lo tengo que decir / tengo que decírselo), with/without optional "que" omissions that are actually grammatical, tú vs usted only if the cue allows both. A learner who writes correct, natural Peninsular Spanish that respects the cue must be accepted. Do NOT list variants that differ only in: capitalization, punctuation, accents, explicit subject pronouns (yo/tú/él…), or -se vs -ra subjunctive — the checker already handles those.
  - `cue` pins anything the English leaves open: "tú", "usted", "vosotros", "ustedes", or a verb to use ("use esperar"), or a register "(a un amigo, coloquial)". If the English "you" is ambiguous, ALWAYS give a cue.
  - `fs` / `fe`: Spanish words given pre-filled at the start / end of the answer because they test nothing (names, places, set objects: fe="el Vega Sicilia."). Every accepted answer must start with fs and end with fe exactly. Use on ~6–10 items where the tail is just vocabulary.
- `G(spanish_with_blank, answer, note="", w=False)` — fill in the blank. Format the blank as `___ (infinitive, subject)` e.g. `"Espero que ___ (venir, vosotros) pronto."`. `answer` = only the text of the blank (string or list of acceptable strings). The context must force the answer: no other tense/mood should also be grammatical.
- `M(spanish_or_english_stem, options, note="", w=False, cue="")` — multiple choice, 4 options, FIRST is correct. Distractors must be clearly wrong (wrong mood, wrong person, wrong tense), never a second correct answer. Use for fine distinctions (indicative vs subjunctive, infinitive vs que + subjunctive, que vs de que, etc.).

## Content rules

- Spain Spanish only: vosotros (in at least 8 items), Peninsular vocabulary (coche, ordenador, móvil, piso, coger, vale, zumo, gafas, aparcar, conducir, el metro, la nevera…). "Le" for male persons is fine (also accept "lo").
- Past subjunctive, when it appears, uses -ra forms.
- Every English prompt must be natural English an American would say. Many present-subjunctive prompts are naturally English infinitive constructions ("I want you to come" → "Quiero que vengas"). Mix in "I hope…", "I'd rather…", "Tell her to…", etc.
- Vocabulary is a broad mix: daily life in Spain, food and wine, restaurants and bars, travel, work, family, friends, news, neighbours, the doctor, shopping. Not mostly wine.
- About 5 items per unit in everyday colloquial register (cue "(a un amigo, coloquial)" or similar), using things like "vale", "venga", "es que", "tío", "a ver si", "¡Ojalá!", "me da igual que…".
- Contrast items: include several items where the SAME trigger family takes the indicative or infinitive, so the learner must decide (e.g. "Quiero ir" vs "Quiero que vayas"; "Creo que viene" vs "No creo que venga").
- Weaving (units 2 and up): about 6 items with `w=True` that combine this unit's structure with a structure from an EARLIER unit (list of earlier units below). Put them at the end of the list.
- `note`: one short line in Spanish, explaining the point of THAT item (irregular form, trigger, why subjunctive). Leave it "" to use the unit's default note. Never write English in notes.
- Sentences: 6–18 words. Vary sentence length and person. Don't repeat the same verb more than 3 times in the unit.
- Order the list so types are mixed (not all T then all G), with weaving items last.

## The syllabus (units 1–12, Block A — present subjunctive)

1. Wishes and hopes: querer, preferir, esperar, desear que — Espero que lleguéis a tiempo.
2. Influence: pedir, aconsejar, exigir, recomendar, decir (command), prohibir, dejar que — Os pido que no hagáis ruido.
3. Emotion: alegrarse de que, molestar que, temer que, encantar que, sentir que, dar miedo/pena que — Me molesta que siempre llegue tarde.
4. Impersonal judgments: es lógico / raro / importante / necesario / mejor / una pena que; vs es verdad / está claro / es obvio que + indicative — Es lógico que estén cansados.
5. Doubt and denial vs belief: no creo que, dudo que, no es cierto que, no pienso que vs creo que / pienso que / estoy seguro de que + indicative; ¿crees que…? — No creo que tenga razón.
6. Probability: quizás, tal vez, posiblemente, probablemente (subj.) vs a lo mejor, igual (ind., colloquial) — Tal vez venga mañana.

"""
Decides whether an answer was right, so run_eval.py can mark pass/fail.

`judge` is what run_eval.py looks for. It checks criterion 5: the answer has to
contain every practical detail named in the question's `expects` string.

`expects` holds comma-separated phrases ("Marine Terrace, Corry Lane"). A
phrase counts as found when all of its content words appear in the text, in
any order, so "90 minutes away by road" still matches "90 minutes by road".
All phrases have to be found — naming Corry Lane but not Marine Terrace is
half an answer, and half an answer is a fail.

The other two helpers cover criteria 1 and 2 and use the same matching, so all
three criteria are judged the same way every run.
"""

import re

STOPWORDS = {"the", "and", "for", "along", "from", "with", "about"}


def _words(text: str) -> set[str]:
    text = text.lower().replace("’", "'")
    text = re.sub(r"'s\b", "", text)
    return set(re.findall(r"[a-z0-9]+", text))


def _phrases(expects: str) -> list[set[str]]:
    phrases = []
    for part in expects.split(","):
        words = {w for w in _words(part) if w not in STOPWORDS and (len(w) > 2 or w.isdigit())}
        if words:
            phrases.append(words)
    return phrases


def contains_all(expects: str, text: str) -> bool:
    """Every phrase in `expects` is present in `text`."""
    found = _words(text)
    phrases = _phrases(expects)
    return bool(phrases) and all(p <= found for p in phrases)


def retrieved_has_answer(expects: str, results) -> bool:
    """Criterion 1: a single retrieved chunk holds everything `expects` names."""
    return any(contains_all(expects, r.text) for r in results)


def names_source(answer: str) -> bool:
    """Criterion 2: the answer cites at least one corpus file by name."""
    return re.search(r"\b[\w-]+\.(md|txt)\b", answer) is not None


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Criterion 5: the answer includes the requested location, route or detail."""
    return contains_all(expects, answer)

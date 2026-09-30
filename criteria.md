# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
The city guides contain direct answers to my transport, cycling, and food
questions, but they are spread across different towns and guides. A target of
four allows one difficult retrieval while still requiring the system to find
answer-bearing text for most questions.

> **Revised in unit 2:** For at least 5 of my 6 test questions, one retrieved
> chunk contains every phrase in that question's `expects` string.
>
> **Why revised:** Two measurement problems, not a missed number. First, the
> `questions.py` I committed in unit 1 has **six** questions (the airport
> question from my Sample Answer is the sixth), so "4 of my 5" had nothing to
> be 4 of. I kept the same bar — 80% — which is 5 of 6; 4 of 6 would have
> quietly lowered it. Second, "contains the answer" was a judgment call. Tying
> it to the `expects` phrases I wrote before any results existed makes it
> something `scorer.py::retrieved_has_answer` checks the same way every time.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Every chunk retains its source filename and the grounding instruction requires
the model to name it. Since each answer is generated from retrieved chunks,
every in-scope answer should be able to cite at least one source.

> **Revised in unit 2:** Every answer names at least one source document by
> its filename (e.g. `guide_brightwater.md`) — 6 of 6 on every run.
>
> **Why revised:** "Names a source" didn't say what counts. "According to the
> Brightwater guide" and "(guide_brightwater.md)" are both arguably a source,
> and I'd have scored them differently on different days. The grounding
> instruction asks for the filename, so the filename is what I check
> (`scorer.py::names_source`). The count is 6, not 5, because `questions.py`
> has six questions.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
My in-corpus distances ranged from 0.522 to 0.667, while the five unrelated
questions ranged from 0.839 to 1.056. The 0.75 cutoff sits in that gap, so I
expect all five unrelated questions to be refused; the 4-of-5 target leaves
room for one borderline result in later runs.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks contain complete `##` guide sections and do not
cut a section in the middle.



**Why this target:**
The city guides are structured by topic headings, so a complete section keeps
the facts needed for a travel question together. The 1,120-character maximum
is approximately 280 tokens, while allowing shorter chunks when a complete
section is smaller.


---

## 5. Your choice

For at least 4 of 5 travel questions about transport, routes, or local food,
the answer includes the requested location, route, or practical detail.



**Why this target:**
These are the main questions a visitor would ask of this corpus. The guides
state many of these details directly, but a small number require retrieval from
one specific town guide rather than a regional overview.

> **Revised in unit 2:** For at least 5 of my 6 test questions, the answer
> contains every phrase in that question's `expects` string.
>
> **Why revised:** Same two problems as criterion 1. There are six questions,
> so 80% is 5 of 6. And "includes the requested detail" needed a fixed
> definition: the `expects` strings I committed in unit 1, before any
> results, checked by `scorer.py::judge`.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

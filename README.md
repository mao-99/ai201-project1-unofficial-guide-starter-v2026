# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project answers practical travel questions using the `city_guides` corpus,
which contains guides to towns and regional services. It can answer questions
about transport, walking and cycling, food, attractions, accommodation, and
when to visit. It retrieves the most relevant guide excerpts before generating
an answer, cites the source file, and refuses questions the guides do not cover.

## Chunking Strategy

**Chunk size:** 1,120 characters maximum (approximately 280 tokens)

**Overlap:** None

The city guides are organised around `##` headings, and each heading introduces
a distinct topic such as transport, accommodation, or practical information.
My chunker keeps each heading and the content below it together, then merges
consecutive complete sections only while the combined chunk stays within about
1,120 characters. This is approximately 280 tokens using the rough estimate
of four characters per token. This avoids the starter chunker's arbitrary mid-section cuts
while still preventing one chunk from covering too many topics. I chose no
overlap because the chunks end at complete section boundaries rather than in
the middle of a thought.

## Sample Chunks

**Chunk 1** - source: `guide_accessibility.md#0` - produced by: `chunker.py::header_split`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```


**Chunk 2** - source: `guide_corry_vale.md#0` - produced by: `chunker.py::header_split`

```
# Corry Vale

Corry Vale is not a town but a valley containing four villages strung along eleven miles of road. Visitors treat it as one destination and locals emphatically do not. The largest village has 900 people and the smallest has 140.



##  Getting there

There is no public transport into the valley beyond a school bus that will carry passengers if there is room. Driving from Brightwater takes 35 minutes on a good road as far as the valley mouth and then 20 more on a poor one. Cycling in is a serious undertaking; the road climbs 400 metres in the first four miles.
```


**Chunk 3** - source: `guide_elder_ness.md#2` - produced by: `chunker.py::header_split`

```
 When to go

April to May and September to October for birds, which is what most visitors come for. Midsummer is pleasant and quiet. Winter is severe, the road floods more often, and the pub reduces to weekends only.



##  Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 4** - source: `guide_kestrelford.md#2` - produced by: `chunker.py::header_split`

```
 When to go

Late spring and early autumn. The Saturday market runs year-round but is much reduced from November to February. August is busy with walkers. The single-track approachroad is genuinely difficult in snow and the town can be cut off for a day or two most winters.



##  Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 5** - source: `guide_regional_transport.md#0` - produced by: `chunker.py::header_split`

```
# Getting around the region



##  The railway

The line runs along the river valley, connecting Brightwater to the regional
hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line
north of Brightwater closed in 1963 and everything beyond it is bus or car.

Tickets are cheaper booked the day before than on the day, and considerably
cheaper than that booked a week ahead. There is no ticket office at
Brightwater station outside weekday mornings; the machine on the platform takes
cards only. 
```

## Sample Answer

**Question:** How far is the closest airport?

**Answer:**

```
The nearest airport to Brightwater is 90 minutes away by road
(guide_brightwater.md).
```

**My relevance cutoff:** `0.75`

Lower distances are better. My six in-corpus questions ranged from `0.522` to
`0.667`; the five out-of-corpus questions ranged from `0.839` to `1.056`.
I set the cutoff to `0.75`, in the gap between those groups. This allows the
weakest relevant result through while still refusing the closest unrelated
question by `0.089`.

| Question | In corpus? | Best distance |
|---|---|---|
| Where do long-distance coaches stop? | Yes | 0.664 |
| How far is the closest airport? | Yes | 0.667 |
| Where should I ride my bike along? Where shouldn't I? | Yes | 0.608 |
| Where do I get fish and chips? Ice cream? | Yes | 0.644 |
| I'm a tourist, where do I find food with scenery? | Yes | 0.576 |
| I haven't met locals yet; where do they go to eat? | Yes | 0.522 |
| What is the capital of Mongolia? | No | 0.863 |
| How do I change the oil in a diesel engine? | No | 0.899 |
| Who won the 1994 World Cup? | No | 1.056 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.839 |
| How do I write a for loop in Rust? | No | 0.883 |

## How I Used AI

**1.** I asked Copilot whether the starter's character-based chunking should be
replaced with paragraph or heading boundaries. It explained that `##` headings
were meaningful topic boundaries in the city-guide corpus, while a character
limit could be a maximum rather than a target. I implemented a heading-based
chunker that merges consecutive complete sections without splitting them in
the middle.

**2.** I asked Copilot why valid questions were being refused after indexing
the city guides. It helped distinguish the relevance gate from retrieval and
explained that this project reports distance, where lower is better. I compared
my in-corpus and out-of-corpus distances, then changed the cutoff from `0.6`
to `0.75` because that value fell in the observed gap.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Produced by `python run_eval.py --label before --corpus city_guides` →
[`results/run_2026-09-29_2319_before.md`](results/run_2026-09-29_2319_before.md).
Six questions (the five from unit 1 plus the airport question from my Sample
Answer — see the criterion revisions in `criteria.md`), three runs each,
caching off, top-k 5, cutoff 0.75, chunks from `chunker.py::header_split`.

Criteria 1, 2 and 5 are scored by `scorer.py` on every run. Criteria 3 and 4
are deterministic — retrieval, the gate, and the chunker have no randomness —
so one measurement goes in all three columns.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 5 of 6 (was 4 of 5) | 6/6 | 6/6 | 6/6 | MET |
| 2. Every answer names a source | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are whole `##` sections | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answer includes the requested detail | 5 of 6 (was 4 of 5) | 4/6 | 5/6 | 5/6 | MISSED |

### Real output, per criterion

**Criterion 1** — retrieval for *"How far is the closest airport?"*, run 1.
Produced by `store.py::search`, checked by `scorer.py::retrieved_has_answer`.
The answer sentence is in `guide_brightwater.md#0`, third of five:

```
- Best distance: 0.6673 (passed the gate)
- Chunks retrieved: guide_corry_vale.md#0 (0.667), guide_marchwood.md#0 (0.700), guide_brightwater.md#0 (0.725), guide_regional_transport.md#1 (0.757), guide_walking.md#1 (0.769)
- Criterion 1 (a chunk holds the answer): True

guide_brightwater.md#0 contains:
"Long-distance coaches stop on Verrill Street rather than at the station, which
catches people out. There is no airport; the nearest is 90 minutes by road."
```

**Criterion 2** — *"Where should I ride my bike along? Where shouldn't I?"*,
run 3. Produced by `generate.py::answer_from_chunks`, checked by
`scorer.py::names_source`:

```
Based on the documents, cycling is pleasant on the **Brightwater river path** and the **old railway trackbed from Kestrelford**, but it is unpleasant on **Mill Road** and the **coast road** (neither of which has a shoulder). 

Source: `guide_regional_transport.md`
```

**Criterion 3** — produced by `run_eval.py::check_out_of_scope`, cutoff 0.75:

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.863)  What is the capital of Mongolia?
  refused  (best distance 0.899)  How do I change the oil in a diesel engine?
  refused  (best distance 1.056)  Who won the 1994 World Cup?
  refused  (best distance 0.839)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.883)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4** — produced by `run_eval.py::check_chunks` over chunks from
`chunker.py::header_split` (five chunks, seed 201). A chunk passes when every
`##` piece of it is, word for word, a whole section of its source file. As a
check on the checker, the same function scores `fallback_split` 0/5.

```
| Chunk | `##` sections | Characters | Whole sections only? |
|---|---|---|---|
| guide_brightwater.md#1 | 3 | 960 | yes |
| guide_marchwood.md#1 | 3 | 870 | yes |
| guide_regional_transport.md#1 | 2 | 914 | yes |
| guide_accessibility.md#0 | 2 | 892 | yes |
| guide_kestrelford.md#1 | 4 | 1120 | yes |
```

**Criterion 5** — produced by `generate.py::answer_from_chunks`, scored by
`scorer.py::judge`. A pass, then the two failures.

*"Where do long distance coaches stop?"* — run 1, expects `Verrill Street`, **pass**:

```
Long-distance coaches stop on Verrill Street (guide_brightwater.md).
```

*"I havent met any locals yet - where do they go to eat? Good food and great
value"* — run 1, expects `Marine Terrace, Corry Lane`, **fail**:

```
Across the region, locals go one street back from where the visitors are, as good cooking is typically found there for about a third less than the tourist spots (e.g., Corry Lane in Brightwater). (Source: guide_eating.md and guide_brightwater.md)
```

*"I'm a tourist, where do I find the food for me - with the scenery to match?"*
— run 2, expects `Brightwater's riverside`, **fail (all three runs)**:

```
Based on the provided documents, the good cooking is typically found one street back from the visitors and scenery. For example, in Pellew Sands, the seafront offers chips and ice cream, while the better cooking is on Marine Terrace one street back (`guide_pellew_sands.md`, `guide_eating.md`). Similarly, in Halden Bay, the harbour front prices are higher, and better food can be found on Fell Street, one level up (`guide_eating.md`).
```

## Verdicts

Targets are the unit 1 targets. Three of them (1, 2, 5) are revised in
`criteria.md` for *measurement* reasons only: `questions.py` had six
questions, not five, so "4 of 5" became "5 of 6" (the same 80% bar, not a
lower one), and "contains the answer" / "names a source" were pinned to
checks I can repeat. The originals are still there, above the revisions.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | **MET** | 6/6 on all three runs against a target of 5 of 6. Not close, but it's weaker than it looks: for the airport question the answer chunk is only third of five, behind two chunks with no answer in them. |
| 2 | Every answer names a source | **MET** | 18 of 18 answers include a `.md` filename. The target was "every answer", so one miss would have been a MISS; there wasn't one. |
| 3 | Gate stops out-of-corpus questions | **MET** | 5/5 refused against a target of 4 of 5. The closest one (ibuprofen, 0.839) still clears the 0.75 cutoff by 0.089. It's one deterministic measurement, repeated across the columns. |
| 4 | Sampled chunks are whole `##` sections | **MET** | 5/5 sampled chunks are made only of complete sections. Honestly, this holds by construction: `header_split` only ever cuts at `##`, so this target couldn't be missed (see *What I'd Do Differently*). |
| 5 | Answer includes the requested detail | **MISSED** | 4/6, 5/6, 5/6 against a target of 5 of 6. It held on two runs and broke on one, and the target has to hold every time, so this is a MISS. It is also the closest call in the table. The tourist question failed all three runs, so one bad run on any other question drops the count below target. |

**Arguing the opposite verdict on 5.** The strongest case for MET is that the
tourist question's `expects` is too narrow: Pellew Sands' seafront and Halden
Bay's harbour front are also "food with scenery", so an answer naming those
could fairly count. I checked: no run names *any* tourist-facing place as the
recommendation. All three steer the tourist *away* from the scenic front to
the cheaper street behind it. So even a generous scorer fails it, and the
verdict stays MISSED. I'm also not changing that `expects` string now,
because it would be moving the target after seeing the result.

**Where the scorer is too generous.** Run 3 of the locals question passes
criterion 5 but says "two levels up from Halden Bay's harbour front". The
guide says *one* level. Run 1 of the tourist question (a fail anyway) puts
"Marine Terrace in Halden Bay", but Marine Terrace is in Pellew Sands. So
`scorer.py` checks that the expected phrases are present, not that nothing
false was added. The 5/6 runs are, if anything, generous.

## Diagnoses

One criterion missed: **5**. It comes from two questions: the tourist
question (fails 3/3) and the locals question (fails 1/3).

**The backwards check first.** For both questions, the chunk that holds the
full answer, `guide_eating.md#0`, is retrieved at **rank 1** (0.576 and
0.522), and criterion 1 is 6/6. The answer was sitting in the prompt every
time. So the failure is after retrieval: **the generation stage.**

`guide_eating.md#0` says:

```
Almost everywhere in this region, the good cooking is one street back from
wherever the visitors are. Brightwater's riverside strip is priced for people
who walked there from the hotels; Corry Lane, two streets inland, serves
comparable food for about a third less. Halden Bay's harbour front is roughly
double Fell Street, one level up. Pellew Sands's seafront is chips and ice
cream, and Marine Terrace behind it is where the actual restaurants are.
```

**Locals question: generation, compression to one example.** The chunk
lists four "go here instead" streets, one per town. The grounding instruction
in `generate.py` ends with *"Be brief. Two or three sentences is usually
enough."* On run 1 the model met that by stating the general rule ("one
street back") and giving a single `e.g.` (Corry Lane). Marine Terrace was
dropped. On runs 2 and 3 it happened to give two examples and passed. The
list was in the prompt; the brevity rule let the model cut it down to one
item, and whether it cut to one or two varied from run to run.

**Tourist question: generation, answering the chunk's thesis instead of
the question.** The question asks where the tourist-facing food *is*, with a
view. The retrieved chunk is framed as advice *against* those places (the
riverside is "priced for people who walked there from the hotels"). All three
answers repeat the chunk's argument, "the good cooking is one street back",
and send the user away from the scenic front. None names the riverside, the
seafront, or the harbour front as the answer. The model took the chunk's main
point as the answer and never answered the question actually asked. Brevity
makes this worse: with two or three sentences, the model only has room for
the chunk's headline point.

**The pattern.** These are the only two questions whose answer is a
**list across towns inside one regional chunk** (`guide_eating.md`). Every
single-fact question (coaches, airport, fish and chips) and the bike question
pass 3/3. So it's one problem, not two: when the answer is a list, the
generation step turns it into a general rule plus at most one or two
examples, because the prompt asks for two or three sentences and doesn't ask
it to list every place the documents name.

**Ruled out:**
- *Chunking*: `guide_eating.md#0` holds the whole "pattern worth knowing"
  section in one piece. Nothing was split.
- *Embedding / retrieval*: the right chunk is the closest match for both
  questions.
- *Loading*: the text in the index matches the source file.

**A near-miss that didn't fail but is worth noting.** For the airport
question, the answer chunk is third, behind Corry Vale (no airport content) and
Marchwood ("the airport is 20 minutes out"). All three answers hedge with
both. It passes because the scorer only checks for "90 minutes by road", but
a user asking "the closest airport" would get two numbers with no way to
choose between them. That's retrieval pulling in a same-topic chunk about a
different town.

## The Improvement

**What I changed:** One thing: the last rule of `GROUNDING_INSTRUCTION` in
`generate.py`. Retrieval, chunking, top-k, the cutoff, the questions and the
`expects` strings are all unchanged.

```diff
- - Be brief. Two or three sentences is usually enough.
+ - Answer the question the user actually asked, even if the documents recommend something else. You can add that advice after the answer.
+ - When the documents name several places, routes or options that answer the question (for example one per town), list every one of them rather than giving a general rule with a single example.
+ - Otherwise be brief.
```

**Why I picked it:** The diagnosis put both criterion 5 failures at
generation, with the right chunk already at rank 1. The "two or three
sentences" rule was squeezing a four-town list down to a rule plus one example,
so I replaced it with an instruction to list every option and to answer the
question as asked. Hybrid search or re-chunking would have changed retrieval,
and retrieval was already 6/6.

### Run Log — After

`python run_eval.py --label after --corpus city_guides` →
[`results/run_2026-09-29_2323_after.md`](results/run_2026-09-29_2323_after.md).
Same six questions, three runs, caching off, same index.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 5 of 6 (was 4 of 5) | 6/6 | 6/6 | 6/6 | MET |
| 2. Every answer names a source | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are whole `##` sections | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answer includes the requested detail | 5 of 6 (was 4 of 5) | 5/6 | 6/6 | 5/6 | MET |

Before and after, side by side, for the only criterion that moved:

| Criterion 5, per question | Before (runs 1/2/3) | After (runs 1/2/3) |
|---|---|---|
| Coaches, airport, bike, fish and chips | pass pass pass | pass pass pass |
| Locals — "where do they go to eat?" | **fail** pass pass | pass pass pass |
| Tourist — "food with the scenery to match" | **fail fail fail** | **fail** pass\* **fail** |
| **Total** | 4/6 · 5/6 · 5/6 | 5/6 · 6/6 · 5/6 |

\* A false pass. See below.

*Locals question, run 1, after* (`generate.py::answer_from_chunks`). Before,
this run named only Corry Lane:

```
Based on the provided documents, good food at better value is generally found one street or level back from where the visitors go:

* **Brightwater:** Corry Lane, which is two streets inland from the riverside strip, serves comparable food for about a third less (*guide_eating.md* and *guide_brightwater.md*).
* **Corry Lane (Brightwater):** Guesthouses here offer better value than the obvious riverside hotels (*guide_brightwater.md*).
* **Halden Bay:** Fell Street, one level up from the harbour front (*guide_eating.md*).
* **Pellew Sands:** Marine Terrace, which is behind the seafront (*guide_eating.md*).
* **Marchwood:** The good district is Northgate, which is a tram ride away, while the station area is uniformly poor (*guide_eating.md*). 
```

*Tourist question, run 3, after*. It fails in a new way: it now refuses:

```
I don't have enough information to answer your question about where to find food with the scenery to match. 

*(Note: The provided documents do contain information about where to find good food in relation to visitor spots—such as Marine Terrace in Pellew Sands, Corry Lane in Brightwater, Fell Street in Halden Bay, and Northgate in Marchwood (guide_eating.md, guide_pellew_sands.md)—but they do not mention scenery matching these food locations.)*
```

**Did it help?** Partly. It fixed the problem the diagnosis was about. The
locals question went from 2/3 to 3/3, and every answer that was cut down to
one example now lists all the towns. That moved criterion 5 from MISSED to
MET. It did **not** fix the tourist question. That one went from "answers a
different question" to "says it doesn't have enough information" (runs 1 and
3). The new "answer the question actually asked" rule seems to have made
the model more literal: the chunk never uses the word "scenery", so the
model now decides it can't answer. The run 2 "pass" is a false positive from
the scorer. The answer mentions "Brightwater's riverside strip" only as the
expensive place to avoid, which is the same failure as before. Re-scored by
reading it, criterion 5 is 5/6 on all three runs. That still holds the
5-of-6 target, so the verdict stays MET, but only just.

It also had side effects. Answers are 3–4× longer (the bike answer went
from one sentence to two bullet lists), and two locals answers now include
padding: a "Corry Lane" bullet listed as if it were a town, and a line about
guesthouses, which isn't food. Criterion 2 held at 6/6, so the longer answers
didn't lose their citations.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

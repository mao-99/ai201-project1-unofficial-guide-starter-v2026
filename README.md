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

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

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

#!/usr/bin/env python3
"""
Run your test questions repeatedly and write the results down.

    python run_eval.py                 three runs, the default
    python run_eval.py --runs 5        more runs
    python run_eval.py --label after   name this run, e.g. before/after a fix

This does the mechanical half of unit 2 for you: it asks each of your questions
the same way three separate times, with caching turned off so you get three
real answers, and writes everything into results/ as a table with one row per
question.

It also puts every question in `OUT_OF_SCOPE` through retrieval and the gate
and records what happened, so criterion 3 — the one about out-of-corpus
questions — has evidence in the same file as the other four. That part costs
nothing: a question the gate refuses never reaches the model.

That table is the raw material for your run log, not the run log itself. The
submission template wants one row per *criterion* — aggregating your questions
up into your criteria is your work, not the script's.

⚠️ What it does NOT do is decide whether an answer was right.

That judgment is yours, and you'll build it in class in unit 2 as `scorer.py`.
Until that file exists, the Run columns carry the raw answers and you read them
yourself. Once it exists — a file called `scorer.py`, with a function
`judge(question, expects, answer, results) -> bool` — this script finds it
automatically and the Run columns carry verdicts instead.

Deciding what counts as correct is the actual lesson. It would be easy to hand
you a scorer; you'd learn nothing from it.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

import config
import questions as qs


def load_scorer():
    """Use scorer.py if the student has built it. Otherwise run unscored."""
    try:
        import scorer  # noqa: PLC0415
    except ImportError:
        return None
    judge = getattr(scorer, "judge", None)
    return judge if callable(judge) else None


def check_chunks(corpus, sample=5, seed=201):
    """Criterion 4: are sampled chunks made of whole `##` sections?

    A chunk passes when every `##` piece of it is, word for word, a complete
    section of its source document — nothing cut off at either end. The sample
    is seeded so every run checks the same five chunks.
    """
    import random
    from ingest import load_documents
    from chunker import split_documents

    documents = load_documents(corpus)
    sections = {
        d.source: {s.strip() for s in d.text.split("##") if s.strip()} for d in documents
    }
    chunks = split_documents(documents)
    picked = random.Random(seed).sample(chunks, min(sample, len(chunks)))

    rows = []
    for chunk in picked:
        pieces = [s.strip() for s in chunk.text.split("##") if s.strip()]
        whole = all(piece in sections[chunk.source] for piece in pieces)
        rows.append({"label": chunk.label, "sections": len(pieces),
                     "chars": len(chunk.text), "whole": whole,
                     "produced_by": chunk.produced_by})
    return rows


def run_once(question: str, top_k, threshold, corpus, variant):
    """One question, one run. Returns the answer and what retrieval gave us."""
    from store import search
    import gate
    from generate import answer_from_chunks

    results = search(question, top_k=top_k, corpus=corpus, variant=variant)
    decision = gate.check(results, threshold=threshold)

    if not decision.passed:
        return gate.REFUSAL, results, decision

    # cache=False on purpose. Three runs have to be three real answers.
    answer = answer_from_chunks(question, results, cache=False)
    return answer, results, decision


def main():
    parser = argparse.ArgumentParser(description="Run the test questions and log the results.")
    parser.add_argument("--runs", type=int, default=3, help="runs per question (default 3)")
    parser.add_argument("--label", default="", help="a name for this run, e.g. 'before'")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--variant", default="default")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    top_k = args.top_k or config.TOP_K
    threshold = config.THRESHOLD if args.threshold is None else args.threshold

    items = qs.answered()
    if not items:
        print(
            "questions.py has no questions in it yet.\n"
            "Milestone 2 asks you to write five. Fill them in and run this again.",
            file=sys.stderr,
        )
        sys.exit(1)

    judge = load_scorer()
    if judge is None:
        print("No scorer.py found — running unscored. Verdict column will be blank.")
        print("You'll build scorer.py in class in unit 2.\n")

    if args.runs < 3:
        print(f"⚠️  {args.runs} run(s). The submission asks for three.\n")

    transcript = []
    rows = []

    for item in items:
        question = item["question"]
        expects = item.get("expects", "")
        print(f"\n{question}")

        run_results = []
        for run in range(1, args.runs + 1):
            answer, results, decision = run_once(
                question, top_k, threshold, corpus, args.variant
            )
            passed = judge(question, expects, answer, results) if judge else None
            run_results.append(passed)

            import scorer
            has_answer = scorer.retrieved_has_answer(expects, results)
            cites = scorer.names_source(answer)

            mark = {True: "pass", False: "fail", None: "—"}[passed]
            print(f"  run {run}: {mark}  (best distance {decision.best_distance:.3f})")

            transcript.append(
                {
                    "question": question,
                    "run": run,
                    "answer": answer,
                    "sources": sorted({r.source for r in results}),
                    "best_distance": decision.best_distance,
                    "gate_passed": decision.passed,
                    "retrieved_has_answer": has_answer,
                    "names_source": cites,
                    "answer_correct": passed,
                    "chunks": [f"{r.label} ({r.distance:.3f})" for r in results],
                }
            )

        rows.append({"question": question, "expects": expects, "runs": run_results})

    gate_rows = check_out_of_scope(top_k, threshold, corpus, args.variant)
    chunk_rows = check_chunks(corpus)

    write_report(
        rows, transcript, gate_rows, args, corpus, top_k, threshold,
        scored=judge is not None, chunk_rows=chunk_rows,
    )


def check_out_of_scope(top_k, threshold, corpus, variant):
    """Put every OUT_OF_SCOPE question through retrieval and the gate.

    Criterion 3 in criteria.md is about questions the corpus doesn't cover, and
    it needs evidence in the run log like the other four. This costs nothing:
    a question the gate refuses never reaches the model, so there is no API
    call and no reason to run it three times — retrieval is deterministic and
    the gate is a comparison against a fixed number.
    """
    from store import search
    import gate

    questions = getattr(qs, "OUT_OF_SCOPE", [])
    if not questions:
        return []

    print("\nOut-of-scope questions (the gate should refuse these):")
    rows = []
    for question in questions:
        results = search(question, top_k=top_k, corpus=corpus, variant=variant)
        decision = gate.check(results, threshold=threshold)
        refused = not decision.passed
        print(f"  {'refused' if refused else 'LET THROUGH'}  "
              f"(best distance {decision.best_distance:.3f})  {question}")
        rows.append(
            {
                "question": question,
                "refused": refused,
                "best_distance": decision.best_distance,
            }
        )

    kept = sum(r["refused"] for r in rows)
    print(f"  -> gate refused {kept} of {len(rows)}")
    return rows


def criterion_summary(transcript, gate_rows, chunk_rows, runs):
    """One row per criterion, one column per run — the shape the README wants."""
    def per_run(key):
        cells = []
        for run in range(1, runs + 1):
            entries = [e for e in transcript if e["run"] == run]
            cells.append(f"{sum(bool(e[key]) for e in entries)}/{len(entries)}")
        return cells

    refused = f"{sum(r['refused'] for r in gate_rows)}/{len(gate_rows)}"
    whole = f"{sum(r['whole'] for r in chunk_rows)}/{len(chunk_rows)}"
    return [
        ("1. Retrieved chunk contains the answer", per_run("retrieved_has_answer")),
        ("2. Every answer names a source", per_run("names_source")),
        ("3. Gate stops out-of-corpus questions", [refused] * runs),
        ("4. Sampled chunks are whole `##` sections", [whole] * runs),
        ("5. Answer includes the requested detail", per_run("answer_correct")),
    ]


def write_report(rows, transcript, gate_rows, args, corpus, top_k, threshold, scored,
                 chunk_rows=()):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = len(rows[0]["runs"]) if rows else 0
    run_headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    run_divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        f"- Produced by: `run_eval.py::main`",
        f"- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`",
        f"- Corpus: `{corpus}` (index variant `{args.variant}`)",
        f"- top-k: {top_k} · relevance cutoff: {threshold}",
        f"- Runs per question: {n}, caching off",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "This table is one row per QUESTION. The run log your README asks for is",
        "one row per CRITERION, so aggregate these into it — criterion 1 is how many",
        "of your questions had the answer in the retrieved chunks, and so on.",
        "",
        f"| Question | {run_headers} |",
        f"|---|{run_divider}|",
    ]

    for row in rows:
        cells = []
        for passed in row["runs"]:
            cells.append({True: "pass", False: "fail", None: " "}[passed])
        question = row["question"].replace("|", "\\|")
        lines.append(f"| {question} | {' | '.join(cells)} |")

    if not scored:
        lines += [
            "",
            "> The Run columns are blank because `scorer.py` doesn't exist yet.",
            "> Judge each question yourself by reading the output below, or build",
            "> the scorer first and re-run.",
        ]

    lines += [
        "",
        "## Per criterion",
        "",
        "Criteria 1, 2 and 5 are scored by `scorer.py` on every run. Criteria 3",
        "and 4 are deterministic (retrieval, the gate, and the chunker have no",
        "randomness), so their single measurement is repeated in each column.",
        "",
        f"| Criterion | {run_headers} |",
        f"|---|{run_divider}|",
    ]
    for name, cells in criterion_summary(transcript, gate_rows, chunk_rows, n):
        lines.append(f"| {name} | {' | '.join(cells)} |")

    if chunk_rows:
        lines += [
            "",
            "### Criterion 4 — sampled chunks",
            "",
            f"Produced by `run_eval.py::check_chunks` over chunks from "
            f"`{chunk_rows[0]['produced_by']}`, seed 201.",
            "",
            "| Chunk | `##` sections | Characters | Whole sections only? |",
            "|---|---|---|---|",
        ]
        for row in chunk_rows:
            lines.append(f"| {row['label']} | {row['sections']} | {row['chars']} | "
                         f"{'yes' if row['whole'] else '**no**'} |")

    if gate_rows:
        refused = sum(r["refused"] for r in gate_rows)
        lines += [
            "",
            "---",
            "",
            "## The relevance gate on out-of-corpus questions",
            "",
            f"Produced by `run_eval.py::check_out_of_scope`, cutoff {threshold}. "
            f"Refused {refused} of {len(gate_rows)}.",
            "",
            "Retrieval is deterministic and the gate is a comparison against a",
            "fixed number, so these do not vary between runs — one pass over the",
            "list is the whole measurement.",
            "",
            "| Out-of-scope question | Best distance | Gate |",
            "|---|---|---|",
        ]
        for row in gate_rows:
            question = row["question"].replace("|", "\\|")
            verdict = "refused" if row["refused"] else "**let through**"
            lines.append(f"| {question} | {row['best_distance']:.3f} | {verdict} |")

    lines += ["", "---", "", "## Real output", "",
              "This is what the system actually produced. Paste the relevant parts",
              "into your README underneath the table — the rubric asks for real",
              "output as text, not a description of it.", ""]

    for entry in transcript:
        lines += [
            f"### {entry['question']} — run {entry['run']}",
            "",
            f"- Best distance: {entry['best_distance']:.4f} "
            f"({'passed' if entry['gate_passed'] else 'refused by'} the gate)",
            f"- Sources retrieved: {', '.join(entry['sources']) or 'none'}",
            f"- Chunks retrieved: {', '.join(entry['chunks']) or 'none'}",
            f"- Criterion 1 (a chunk holds the answer): {entry['retrieved_has_answer']} · "
            f"criterion 2 (names a source): {entry['names_source']} · "
            f"criterion 5 (answer has the detail): {entry['answer_correct']}",
            "",
            "```",
            entry["answer"],
            "```",
            "",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")

    import generate as gen

    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print(gen.usage())
    print("\nCommit this file. It's the evidence the run actually happened.")


if __name__ == "__main__":
    main()

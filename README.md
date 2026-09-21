# The Unofficial Guide

Rohan Raj — corpus: `campus_life`

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

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This is a retrieval-augmented Q&A system built on the `campus_life` corpus —
88 short, first-person student write-ups about dining halls, housing,
courses, and campus services. It answers specific factual questions like
dining hall hours, room types, noise levels in a particular building, or
when the laundry room is least busy, and every answer names the exact
document it came from. Questions outside the corpus — general knowledge,
unrelated domains — get an honest "I don't have enough information" instead
of a guess.

## Chunking Strategy

**Chunk size:** no fixed size — split on paragraph breaks, with an 800-character cap as a safety net for the rare oversized paragraph.
**Overlap:** 120 characters, but only applies if that safety net kicks in.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

The starter's fixed 800-character chunker barely touched `campus_life` — 88
documents produced 88 chunks, since almost no post reaches 800 characters.
But reading the actual chunks showed a real problem anyway: a full, correctly
punctuated sentence like "Hours are 11:00am to 7:00pm weekdays" is a complete
thought grammatically, but meaningless on its own if you don't know it's
about North Kitchen. Character count wasn't the issue — the missing title
was.

Every post in this corpus turned out to follow the same shape: a short
title-only opening line ("North Kitchen", "On the housing lottery"), a blank
line, then one to four content paragraphs. So `split_documents` now splits on
paragraph breaks and prefixes that title onto every paragraph that follows
it, instead of emitting the title as a chunk of its own. That turned 88
one-chunk documents into 183 chunks averaging 167 characters, each one
readable without needing anything before or after it. The 800-character cap
with 120-character overlap only exists as a fallback for a paragraph that
runs unusually long — it never actually fires on this corpus, since the
longest paragraph is 373 characters, but it's there so a chunk can't grow
unbounded if I ever add documents that don't follow the title/paragraph
pattern.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline: You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
CS 340 Databases — assessment: Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics: People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`

```
Re: Verrill Street Grill: Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like: The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Should I expect noise at Fenwick Court?

**Answer:**

```
Yes, you can expect noise at Fenwick Court due to thin walls between suites and kitchenettes that carry sound (housing_fenwick_court_noise.txt).
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

I kept the starter's default, **0.6**. In-scope best distances ranged 0.132
to 0.286; every out-of-scope question scored 0.787 to 0.915 — a clean gap of
roughly 0.5 with nothing in between, and 0.6 sits in the middle of it rather
than close to either edge.

| Question | In corpus? | Best distance |
|---|---|---|
| What are the timings for North Kitchen? | Yes | 0.286 |
| What is the room type in Aldridge Hall? | Yes | 0.277 |
| Should I expect noise at Fenwick Court? | Yes | 0.275 |
| What is the best time to do laundry at Tamsin Court? | Yes | 0.132 |
| What are the timings for the campus shuttle? | Yes | 0.248 |
| What is the capital of Mongolia? | No | 0.787 |
| How do I change the oil in a diesel engine? | No | 0.915 |
| Who won the 1994 World Cup? | No | 0.846 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.848 |
| How do I write a for loop in Rust? | No | 0.863 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to design a chunker that would keep a post's subject
(its title line, e.g. "North Kitchen") attached to the content chunks that
follow it, since a full sentence like "Hours are 11:00am to 7:00pm weekdays"
means nothing without knowing which building it's about. It offered two
designs: bake the title into each chunk's text as a prefix, or store it as
Chroma metadata for later filtering. I picked the text-prefix version —
metadata filtering was more scope than Milestone 3 asked for, and baking it
into the text was the simpler fix for the actual problem I'd found.

**2.** While writing criterion #2's "why," I claimed the source-citation
rule was "enforced in the prompt template itself." Claude checked
`generate.py` and pointed out that's not true — the grounding instruction
only *asks* the model to name a file; there's no code that checks the
response actually contains one. I changed the wording from "enforced" to
"instructed" so the criterion's reasoning matched what the code actually
guarantees, instead of overstating it.

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

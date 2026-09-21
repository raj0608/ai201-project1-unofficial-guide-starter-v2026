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
My corpus has some topics covered by multiple documents (e.g., dining halls
come up in several student write-ups) and some covered by just one mention
(e.g., one specific professor's grading style). I expect the single-mention
questions to be harder to retrieve reliably, since there's only one chunk in
the whole corpus that could possibly answer them — if that chunk isn't
embedded well or gets outranked by something more generic, retrieval misses
it entirely.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
My generation prompt instructs the model to include a source filename before
giving an answer — it's a prompt-level instruction, not a code-enforced
constraint, so it's not guaranteed the model always complies. Since this is a
formatting requirement rather than a content judgment, I'm betting it holds
every time the pipeline completes without erroring, which is why I'm setting
this at 5 of 5 instead of 4 of 5.

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
When I measured distances in Milestone 4, the gap between in-corpus and
out-of-scope questions was unusually clean — no overlap at all. In-scope
questions (timings, room details, noise complaints) had best distances
ranging from 0.132 to 0.286, while every out-of-scope question (general
knowledge, unrelated domains like Rust or medicine) scored between 0.787 and
0.915. That's a gap of roughly 0.5, with nothing landing in the middle. I set
my threshold at 0.6 — the starter's default — since it sits comfortably in
the center of that gap rather than close to either edge.

Given how wide and clean this separation is, I'd actually expect the gate to
catch close to 5 of 5 out-of-scope questions in practice. I'm still
targeting 4 of 5 rather than 5 of 5 because my test set is small — only five
out-of-scope questions — and a topic I haven't tested yet (something that
shares more vocabulary with my corpus than "Mongolia" or "diesel engines" do)
could plausibly score closer to the boundary than anything I've measured so
far.

---

## 4. Chunks read as complete thoughts

At least 4 out of 5 sampled chunks read as a complete thought, with no
sentence cut in half.

**Why this target:**
I switched from a fixed-character chunker to splitting on paragraph breaks in
Milestone 3. Most entries in my corpus are short, self-contained write-ups —
one paragraph per opinion or fact (e.g., one paragraph about a dining hall,
one about a professor) — so paragraph boundaries should naturally align with
complete thoughts. I'm not claiming 5 of 5 because a few entries in my corpus
run to multiple paragraphs on one topic, and my chunk size cap could still
split one of those mid-thought.

---

## 5. Citations point to the right source, not just any source

When the system cites a source, that source actually contains the specific
fact used in the answer — not just any retrieved document — in at least 4 of
5 answered questions.

**Why this target:**
My corpus has several documents that touch the same general subject — for
example, multiple entries mention dining halls, or multiple entries mention
housing. That means the system can retrieve a document that's topically
related but doesn't actually contain the specific fact it's citing. Criterion
2 only checks that a source is named at all; this one checks whether it's the
correct source. I set the bar at 4 of 5 rather than 5 of 5 because when two
retrieved chunks are semantically close, the higher-ranked one isn't always
the one holding the exact fact.


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

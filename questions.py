"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "What are the timings for North Kitchen?", "expects": "11:00am to 7:00pm"},
    {"question": "What is the room type in Aldridge Hall?", "expects": "doubles with a shared bathroom"},
    {"question": "Should I expect noise at Fenwick Court?", "expects": "thin walls"},
    {"question": "What is the best time to do laundry at Tamsin Court?", "expects": "Tuesday or Wednesday morning"},
    {"question": "What are the timings for the campus shuttle?", "expects": "every 20 minutes"},
]

# ─── Unit 1's original OUT_OF_SCOPE, preserved for the record ───────────────
#
# All five obviously-different-domain questions. The gate refused all five by
# a wide margin (best distances 0.787-0.915 vs. the 0.6 cutoff) — a real
# measurement, but one that never seriously tested the boundary. Kept here,
# commented out rather than deleted, as evidence of what Milestone 4's
# original cutoff was measured against.
#
# ORIGINAL_OUT_OF_SCOPE = [
#     "What is the capital of Mongolia?",
#     "How do I change the oil in a diesel engine?",
#     "Who won the 1994 World Cup?",
#     "What is the recommended dosage of ibuprofen for a headache?",
#     "How do I write a for loop in Rust?",
# ]

# ─── Unit 2's harder OUT_OF_SCOPE, tightening criterion 3 ───────────────────
#
# Each one names a real building/place/service that IS in the corpus, and
# asks a specific fact that ISN'T covered by it — unlike the originals above,
# which were unrelated to the corpus in every way. This is deliberately the
# hard case: distance-based retrieval can't tell "this chunk is about the
# same building" from "this chunk actually answers the question," so a real
# entity name pulls the distance down regardless of whether the fact is
# there. `run_eval.py` runs these through retrieval and the gate and records
# what happened, so criterion 3 has evidence in the run log alongside the
# other four. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "Does the health center offer dental care?",
    "Does North Kitchen have vegan options?",
    "Does Aldridge Hall have wifi in the dorm rooms?",
    "Is there parking available at Fenwick Court?",
    "Is the campus shuttle wheelchair accessible?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]

"""
Unit 2's scorer: decides whether an answer counts as correct.

`run_eval.py` finds this automatically once it exists and uses `judge()` to
mark each run pass/fail instead of leaving the column blank.
"""


def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    True if `answer` contains the `expects` phrase, case-insensitive.

    This is the check questions.py's own docstring describes: `expects` is
    "a word or short phrase you'd expect a correct answer to contain." A
    refusal never contains it, so a refused question fails automatically —
    no special case needed for that.
    """
    if not expects:
        return False
    return expects.strip().lower() in answer.strip().lower()

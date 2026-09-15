import pandas as pd
from datatrust.evaluation import exact_or_numeric_match, evaluate_frame, is_abstention


PHRASES = ["insufficient information", "cannot determine"]


def test_numeric_match():
    assert exact_or_numeric_match("The answer is 26.", "26")
    assert not exact_or_numeric_match("27", "26")


def test_abstention_detection():
    assert is_abstention("Insufficient information.", PHRASES)


def test_unsupported_correct_answer_is_grounded_hallucination():
    frame = pd.DataFrame([{
        "parsed_answer": "26", "gold_answer": "26", "context": "", "self_reported_confidence": 0.9
    }])
    result = evaluate_frame(frame, PHRASES).iloc[0]
    assert result.answer_correct
    assert result.unsupported_claim
    assert result.hallucinated

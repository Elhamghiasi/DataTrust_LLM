from __future__ import annotations

import re
import pandas as pd


def normalize_answer(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9.\- ]", "", text)
    return re.sub(r"\s+", " ", text)


def is_abstention(answer: str, phrases: list[str]) -> bool:
    normalized = normalize_answer(answer)
    return any(phrase.lower() in normalized for phrase in phrases)


def exact_or_numeric_match(answer: str, gold: str) -> bool:
    normalized_answer = normalize_answer(answer)
    normalized_gold = normalize_answer(gold)
    if normalized_answer == normalized_gold:
        return True
    numbers = re.findall(r"-?\d+(?:\.\d+)?", normalized_answer)
    return len(numbers) == 1 and numbers[0] == normalized_gold


def context_supports_gold(context: str, gold: str) -> bool:
    if not str(context).strip():
        return False
    return bool(re.search(rf"atomic number\s+{re.escape(str(gold))}\b", str(context), flags=re.I))


def evaluate_frame(frame: pd.DataFrame, phrases: list[str]) -> pd.DataFrame:
    evaluated = frame.copy()
    evaluated["abstained"] = [is_abstention(a, phrases) for a in evaluated["parsed_answer"]]
    evaluated["answer_correct"] = [
        exact_or_numeric_match(a, str(g)) and not abstained
        for a, g, abstained in zip(evaluated["parsed_answer"], evaluated["gold_answer"], evaluated["abstained"])
    ]
    evaluated["context_supports_gold"] = [
        context_supports_gold(c, str(g)) for c, g in zip(evaluated["context"], evaluated["gold_answer"])
    ]
    evaluated["unsupported_claim"] = (~evaluated["abstained"]) & (~evaluated["context_supports_gold"])
    evaluated["hallucinated"] = (~evaluated["abstained"]) & (
        (~evaluated["answer_correct"]) | (~evaluated["context_supports_gold"])
    )
    evaluated["appropriate_abstention"] = evaluated["abstained"] & (~evaluated["context_supports_gold"])
    evaluated["confidence_error"] = (
        evaluated["self_reported_confidence"].fillna(0.5) - evaluated["answer_correct"].astype(int)
    ).abs()
    return evaluated

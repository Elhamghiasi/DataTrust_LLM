from __future__ import annotations

import random
import re


IRRELEVANT_FACTS = [
    "The Pacific Ocean is Earth's largest ocean.",
    "A triangle has three sides.",
    "Water freezes at 0 degrees Celsius at standard pressure.",
    "The Moon is Earth's natural satellite.",
    "A leap year normally has 366 days.",
]


def make_context(clean_context: str, gold_answer: str, condition: str, seed: int) -> str:
    rng = random.Random(seed)
    if condition == "clean":
        return clean_context
    if condition == "missing":
        return re.sub(r"has atomic number\s+\d+", "is a chemical element", clean_context)
    if condition == "irrelevant":
        noise = " ".join(rng.sample(IRRELEVANT_FACTS, k=3))
        return f"{noise} {clean_context}"
    if condition == "duplicate_noise":
        return f"### RECORD ### {clean_context} [duplicate] {clean_context} !!! metadata=null; checksum=unknown"
    if condition == "contradictory":
        wrong = int(gold_answer) + rng.choice([-3, -2, -1, 1, 2, 3])
        wrong = max(1, wrong)
        element = clean_context.split(" has atomic number")[0].replace("According to the periodic table, ", "")
        return f"Source A states: {clean_context} Source B states: {element} has atomic number {wrong}."
    if condition == "no_context":
        return ""
    raise ValueError(f"Unknown condition: {condition}")

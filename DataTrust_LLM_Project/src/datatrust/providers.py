from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
import random
import re
import time


SYSTEM_PROMPT = """Answer using only the supplied context. If the answer is not supported, say 'Insufficient information.' Return a concise answer and confidence from 0 to 1 in this exact format:
ANSWER: <answer>
CONFIDENCE: <number>"""


@dataclass
class ModelResponse:
    text: str
    latency_ms: float


class MockProvider:
    """Deterministic simulator with condition-specific error rates for a runnable demo."""

    ERROR_RATES = {
        "clean": 0.03,
        "missing": 0.18,
        "irrelevant": 0.10,
        "duplicate_noise": 0.14,
        "contradictory": 0.42,
        "no_context": 0.25,
    }

    def generate(self, question: str, context: str, condition: str, gold_answer: str, **_: object) -> ModelResponse:
        key = f"{question}|{condition}".encode()
        seed = int(hashlib.sha256(key).hexdigest()[:8], 16)
        rng = random.Random(seed)
        start = time.perf_counter()

        if condition == "missing" and rng.random() < 0.70:
            answer, confidence = "Insufficient information.", rng.uniform(0.70, 0.94)
        elif condition == "no_context" and rng.random() < 0.28:
            answer, confidence = "Insufficient information.", rng.uniform(0.55, 0.85)
        elif rng.random() < self.ERROR_RATES[condition]:
            wrong = max(1, int(gold_answer) + rng.choice([-4, -3, -2, -1, 1, 2, 3, 4]))
            answer, confidence = str(wrong), rng.uniform(0.60, 0.95)
        else:
            answer = gold_answer
            confidence = rng.uniform(0.82, 0.99) if condition == "clean" else rng.uniform(0.65, 0.94)

        text = f"ANSWER: {answer}\nCONFIDENCE: {confidence:.2f}"
        return ModelResponse(text=text, latency_ms=(time.perf_counter() - start) * 1000 + rng.uniform(15, 80))


class OpenAIProvider:
    def __init__(self, model: str, temperature: float = 0.0, max_tokens: int = 120):
        from openai import OpenAI

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, question: str, context: str, **_: object) -> ModelResponse:
        user_prompt = f"CONTEXT:\n{context or '[NO CONTEXT PROVIDED]'}\n\nQUESTION:\n{question}"
        start = time.perf_counter()
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        elapsed = (time.perf_counter() - start) * 1000
        return ModelResponse(text=response.choices[0].message.content or "", latency_ms=elapsed)


def parse_answer_and_confidence(text: str) -> tuple[str, float | None]:
    answer_match = re.search(r"ANSWER:\s*(.+?)(?:\n|$)", text, flags=re.I)
    confidence_match = re.search(r"CONFIDENCE:\s*([01](?:\.\d+)?)", text, flags=re.I)
    answer = answer_match.group(1).strip() if answer_match else text.strip()
    confidence = float(confidence_match.group(1)) if confidence_match else None
    return answer, confidence

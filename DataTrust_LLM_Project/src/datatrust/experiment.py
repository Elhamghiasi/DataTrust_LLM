from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

from .corruption import make_context
from .providers import MockProvider, OpenAIProvider, parse_answer_and_confidence


def build_provider(settings: dict):
    if settings["provider"] == "mock":
        return MockProvider()
    if settings["provider"] == "openai":
        return OpenAIProvider(
            model=settings["model"],
            temperature=settings.get("temperature", 0.0),
            max_tokens=settings.get("max_tokens", 120),
        )
    raise ValueError(f"Unsupported provider: {settings['provider']}")


def run_experiment(questions: pd.DataFrame, config: dict) -> pd.DataFrame:
    settings = config["experiment"]
    provider = build_provider(settings)
    sample = questions.head(int(settings.get("sample_size", len(questions))))
    rows = []
    seed = int(config["project"]["seed"])

    for row_index, question in sample.iterrows():
        for condition_index, condition in enumerate(settings["conditions"]):
            context = make_context(
                question.clean_context,
                str(question.gold_answer),
                condition,
                seed + row_index * 10 + condition_index,
            )
            response = provider.generate(
                question=question.question,
                context=context,
                condition=condition,
                gold_answer=str(question.gold_answer),
            )
            parsed_answer, confidence = parse_answer_and_confidence(response.text)
            rows.append(
                {
                    **question.to_dict(),
                    "condition": condition,
                    "context": context,
                    "provider": settings["provider"],
                    "model": settings["model"],
                    "raw_response": response.text,
                    "parsed_answer": parsed_answer,
                    "self_reported_confidence": confidence,
                    "latency_ms": round(response.latency_ms, 2),
                    "response_chars": len(response.text),
                    "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
                }
            )
    return pd.DataFrame(rows)


def save_results(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns


CONDITION_ORDER = ["clean", "irrelevant", "duplicate_noise", "contradictory", "missing", "no_context"]


def bootstrap_rate_ci(values: pd.Series, iterations: int, confidence: float, seed: int = 42) -> tuple[float, float]:
    array = values.astype(float).to_numpy()
    rng = np.random.default_rng(seed)
    boot = np.array([rng.choice(array, len(array), replace=True).mean() for _ in range(iterations)])
    alpha = 1 - confidence
    return float(np.quantile(boot, alpha / 2)), float(np.quantile(boot, 1 - alpha / 2))


def summarize(frame: pd.DataFrame, iterations: int, confidence: float) -> pd.DataFrame:
    rows = []
    for index, (condition, group) in enumerate(frame.groupby("condition", sort=False)):
        low, high = bootstrap_rate_ci(group["hallucinated"], iterations, confidence, seed=42 + index)
        rows.append(
            {
                "condition": condition,
                "n": len(group),
                "accuracy_rate": group["answer_correct"].mean(),
                "hallucination_rate": group["hallucinated"].mean(),
                "hallucination_ci_low": low,
                "hallucination_ci_high": high,
                "abstention_rate": group["abstained"].mean(),
                "unsupported_claim_rate": group["unsupported_claim"].mean(),
                "mean_confidence": group["self_reported_confidence"].mean(),
                "mean_confidence_error": group["confidence_error"].mean(),
                "mean_latency_ms": group["latency_ms"].mean(),
            }
        )
    result = pd.DataFrame(rows)
    result["condition"] = pd.Categorical(result["condition"], CONDITION_ORDER, ordered=True)
    return result.sort_values("condition").reset_index(drop=True)


def statistical_tests(frame: pd.DataFrame) -> dict:
    table = pd.crosstab(frame["condition"], frame["hallucinated"])
    chi2, p_value, dof, _ = chi2_contingency(table)
    n = table.to_numpy().sum()
    cramers_v = float(np.sqrt(chi2 / (n * max(1, min(table.shape) - 1))))
    clean_rate = frame.loc[frame.condition == "clean", "hallucinated"].mean()
    risk_ratios = {}
    for condition, group in frame.groupby("condition"):
        rate = group["hallucinated"].mean()
        risk_ratios[condition] = None if clean_rate == 0 else float(rate / clean_rate)

    model = smf.logit("hallucinated.astype(int) ~ C(condition, Treatment(reference='clean'))", data=frame).fit(disp=False)
    odds_ratios = {name: float(np.exp(value)) for name, value in model.params.items()}
    return {
        "chi_square": float(chi2),
        "degrees_of_freedom": int(dof),
        "p_value": float(p_value),
        "cramers_v": cramers_v,
        "risk_ratio_vs_clean": risk_ratios,
        "logistic_regression_odds_ratios": odds_ratios,
        "interpretation_rule": "p < 0.05 indicates evidence of association; Cramer's V describes effect size.",
    }


def save_figures(frame: pd.DataFrame, summary: pd.DataFrame, output_dir: Path) -> None:
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")
    palette = ["#1B998B", "#66A182", "#A6C36F", "#F4A261", "#E76F51", "#9D4EDD"]

    fig, ax = plt.subplots(figsize=(11, 6))
    ordered = summary.copy()
    errors = np.vstack([
        ordered.hallucination_rate - ordered.hallucination_ci_low,
        ordered.hallucination_ci_high - ordered.hallucination_rate,
    ])
    ax.bar(ordered.condition.astype(str), ordered.hallucination_rate, color=palette, yerr=errors, capsize=5)
    ax.set(title="Hallucination Rate by Data-Quality Condition", xlabel="Context condition", ylabel="Hallucination rate", ylim=(0, 1))
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(figures / "hallucination_by_condition.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=frame, x="self_reported_confidence", y="answer_correct", hue="condition", alpha=0.55, ax=ax)
    ax.set(title="Confidence vs. Correctness", xlabel="Self-reported confidence", ylabel="Correct answer (0/1)")
    fig.tight_layout()
    fig.savefig(figures / "confidence_vs_correctness.png", dpi=180)
    plt.close(fig)

    metrics = summary.set_index("condition")[["accuracy_rate", "hallucination_rate", "abstention_rate", "unsupported_claim_rate"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(metrics, annot=True, fmt=".2f", cmap="RdYlGn_r", vmin=0, vmax=1, ax=ax)
    ax.set(title="Outcome Profile by Context Condition", xlabel="Metric", ylabel="Condition")
    fig.tight_layout()
    fig.savefig(figures / "outcome_heatmap.png", dpi=180)
    plt.close(fig)


def write_outputs(frame: pd.DataFrame, output_dir: Path, iterations: int, confidence: float) -> tuple[pd.DataFrame, dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize(frame, iterations, confidence)
    tests = statistical_tests(frame)
    summary.to_csv(output_dir / "analysis_summary.csv", index=False)
    with (output_dir / "statistical_tests.json").open("w", encoding="utf-8") as handle:
        json.dump(tests, handle, indent=2)
    save_figures(frame, summary, output_dir)
    return summary, tests

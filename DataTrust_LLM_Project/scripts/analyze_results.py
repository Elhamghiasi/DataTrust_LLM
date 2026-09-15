from pathlib import Path
import pandas as pd

from datatrust.analysis import write_outputs
from datatrust.config import load_config, project_path


def percent(value: float) -> str:
    return f"{100 * value:.1f}%"


def main() -> None:
    config = load_config()
    results_path = project_path(config["project"]["results_path"])
    output_dir = project_path(config["project"]["outputs_dir"])
    frame = pd.read_csv(results_path)
    if "hallucinated" not in frame:
        raise SystemExit("Run scripts/evaluate_results.py before analysis.")
    boolean_columns = ["answer_correct", "hallucinated", "abstained", "unsupported_claim", "appropriate_abstention"]
    for column in boolean_columns:
        frame[column] = frame[column].astype(str).str.lower().map({"true": True, "false": False})
    summary, tests = write_outputs(
        frame,
        output_dir,
        int(config["evaluation"]["bootstrap_iterations"]),
        float(config["evaluation"]["confidence_level"]),
    )
    worst = summary.loc[summary.hallucination_rate.idxmax()]
    clean = summary.loc[summary.condition.astype(str) == "clean"].iloc[0]
    report = f"""# Executive Analysis Report

## Objective

Measure whether controlled degradation of retrieved context is associated with LLM hallucination and related reliability outcomes.

## Dataset

- {frame.question_id.nunique()} verified questions
- {frame.condition.nunique()} context conditions
- {len(frame)} total model responses
- Provider: `{frame.provider.iloc[0]}`
- Model: `{frame.model.iloc[0]}`

## Headline findings

- The clean-context hallucination rate was **{percent(clean.hallucination_rate)}** (95% bootstrap CI: {percent(clean.hallucination_ci_low)}–{percent(clean.hallucination_ci_high)}).
- The highest observed hallucination rate occurred under **{str(worst.condition)}** at **{percent(worst.hallucination_rate)}**.
- The chi-square association test produced **χ²={tests['chi_square']:.2f}**, **p={tests['p_value']:.4g}**, with **Cramer's V={tests['cramers_v']:.3f}**.
- Results indicate that source-data condition is associated with response reliability in this experimental run. Statistical significance does not by itself establish general-world causality.

## Interpretation

Contradictory evidence is expected to be especially risky because a model must select between competing claims. Missing or absent evidence creates a different challenge: a well-behaved system should abstain, while an unsupported definite answer is counted as a hallucination. Therefore, accuracy and abstention must be read together.

## Recommendations

1. Add contradiction detection before context reaches the model.
2. Require evidence-grounded answers and permit explicit abstention.
3. Track unsupported-claim rate in addition to conventional accuracy.
4. Monitor confidence calibration; confident errors are operationally more dangerous.
5. Repeat the experiment across domains and models before making deployment decisions.

## Limitations

- The benchmark covers one structured factual domain.
- Demo mode simulates plausible behavior and validates the analytics workflow; it does not make claims about a production LLM.
- The automated evaluator is transparent but cannot capture every semantic nuance.
- One response per question-condition pair does not measure generation variance.
- Self-reported confidence is not a calibrated probability.

## Next study

Use at least three domains, two models, and five repeated generations per cell; add blinded dual-human annotation and Cohen's kappa.
"""
    (Path(output_dir) / "executive_report.md").write_text(report, encoding="utf-8")
    print(f"Saved analysis, tests, charts, and report to {output_dir}")


if __name__ == "__main__":
    main()

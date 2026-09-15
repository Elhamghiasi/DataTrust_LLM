# DataTrust LLM: Data Quality vs. Hallucination

An end-to-end data science project that measures how source-data quality changes the factual reliability of retrieval-augmented LLM answers.

## Portfolio question

> How do missing, irrelevant, duplicated, noisy, and contradictory contexts affect answer accuracy, hallucination, abstention, and confidence?

The project is intentionally optimized for a one-week portfolio build. It runs offline in deterministic demo mode, or against an OpenAI-compatible API for a real experiment.

## What is included

- A reproducible 100-question benchmark based on stable chemistry facts
- Six controlled context conditions: `clean`, `missing`, `irrelevant`, `duplicate_noise`, `contradictory`, and `no_context`
- A deterministic mock LLM for a zero-cost, fully reproducible demonstration
- An optional OpenAI provider for real model calls
- Rule-based response evaluation with transparent labels
- Bootstrap confidence intervals, chi-square test, Cramer's V, risk ratios, and logistic regression
- Publication-ready charts and a Streamlit dashboard
- Unit tests, data dictionary, methodology, limitations, and an executive report

## Project structure

```text
llm-hallucination-data-quality/
├── app.py
├── config.yaml
├── requirements.txt
├── Makefile
├── data/
│   ├── raw/questions.csv
│   └── processed/results.csv
├── outputs/
│   ├── figures/
│   ├── analysis_summary.csv
│   ├── statistical_tests.json
│   └── executive_report.md
├── scripts/
│   ├── generate_data.py
│   ├── run_experiment.py
│   ├── evaluate_results.py
│   └── analyze_results.py
├── src/datatrust/
│   ├── analysis.py
│   ├── config.py
│   ├── corruption.py
│   ├── data.py
│   ├── evaluation.py
│   ├── experiment.py
│   └── providers.py
├── tests/
└── docs/
```

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make all
streamlit run app.py
```

`make all` creates the questions, runs all 600 experiment rows in deterministic demo mode, evaluates them, produces the statistical analysis, and saves the charts.

## Run a real LLM experiment

Copy `.env.example` to `.env`, add your API key, and change `provider` in `config.yaml`:

```yaml
experiment:
  provider: openai
  model: gpt-4.1-mini
```

Then run:

```bash
python scripts/run_experiment.py --overwrite
python scripts/evaluate_results.py
python scripts/analyze_results.py
```

API calls may cost money. Start with `sample_size: 10`, inspect the output, and only then increase it.

## Experimental design

Each question has one authoritative answer and one clean supporting context. The corruption engine transforms that context while keeping the question fixed. This isolates the independent variable—data quality condition—as much as possible.

| Condition | Controlled change | Expected failure mode |
|---|---|---|
| Clean | Correct fact only | Baseline |
| Missing | Key answer removed | Abstention or unsupported answer |
| Irrelevant | Unrelated facts added | Distraction |
| Duplicate/noise | Repetition and formatting noise | Attention dilution |
| Contradictory | Correct and incorrect claims coexist | Conflict resolution failure |
| No context | Context removed | Reliance on parametric memory |

The primary outcome is `hallucinated`: the response makes a definite factual claim that is wrong or unsupported by the supplied context. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for exact operational definitions.

## Responsible interpretation

This is a controlled benchmark, not a universal ranking of LLMs. Its chemistry questions are intentionally stable and easy to verify, but narrow in subject matter. The rule-based evaluator is auditable but imperfect. For a publication-quality study, use blinded human annotations, multiple domains, repeated generations, multiple models, and inter-annotator agreement.

## Suggested résumé bullet

> Built a reproducible analytics pipeline evaluating 600 LLM responses across six source-data quality conditions; quantified hallucination risk using confidence intervals, chi-square tests, effect sizes, and logistic regression, and communicated findings through an interactive Streamlit dashboard.

## License

MIT. See [LICENSE](LICENSE).

# Executive Analysis Report

## Objective

Measure whether controlled degradation of retrieved context is associated with LLM hallucination and related reliability outcomes.

## Dataset

- 100 verified questions
- 6 context conditions
- 600 total model responses
- Provider: `mock`
- Model: `deterministic-demo-v1`

## Headline findings

- The clean-context hallucination rate was **3.0%** (95% bootstrap CI: 0.0%–7.0%).
- The highest observed hallucination rate occurred under **no_context** at **72.0%**.
- The chi-square association test produced **χ²=169.69**, **p=8.481e-35**, with **Cramer's V=0.532**.
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

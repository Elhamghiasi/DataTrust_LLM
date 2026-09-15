# Methodology

## 1. Study design

This is a within-question controlled experiment. Every benchmark question is evaluated under every data-quality condition. Because the question and gold answer remain constant, observed outcome differences can be associated with changes in the supplied context.

The benchmark uses the first 100 chemical elements and their atomic numbers. These facts are stable, unambiguous, compact, and easy to verify. The narrow domain strengthens labeling reliability but limits external validity.

## 2. Variables

### Independent variable

`condition` is a six-level categorical variable:

- `clean`: one accurate supporting statement
- `missing`: the answer-bearing value is removed
- `irrelevant`: three unrelated true statements precede the accurate statement
- `duplicate_noise`: the accurate statement is duplicated and surrounded by formatting noise
- `contradictory`: accurate and inaccurate values are both presented
- `no_context`: no supporting evidence is supplied

### Outcomes

- `answer_correct`: parsed answer matches the gold answer.
- `abstained`: answer includes a predefined uncertainty/refusal phrase.
- `context_supports_gold`: context explicitly contains the verified gold claim.
- `unsupported_claim`: model gives a definite answer without gold-supporting context.
- `hallucinated`: model gives a definite answer that is incorrect or unsupported.
- `appropriate_abstention`: model abstains when gold support is unavailable.
- `confidence_error`: absolute difference between self-reported confidence and binary correctness.

The hallucination definition is deliberately strict and retrieval-grounded. A factually correct answer produced with no supporting context is still an unsupported claim. Analysts who want a fact-only definition can replace it with `~answer_correct & ~abstained`.

## 3. Hypotheses

- **H0:** Hallucination is independent of context condition.
- **H1:** Hallucination is associated with context condition.

The primary inferential analysis uses a chi-square independence test. Cramer's V summarizes effect size. Bootstrap intervals quantify uncertainty around each condition's observed hallucination rate. A logistic regression estimates odds ratios relative to clean context.

## 4. Reproducibility

The data-corruption and mock-generation processes use fixed seeds. The mock provider derives a stable seed from each question-condition pair. Re-running demo mode therefore produces equivalent outcome data.

Real API runs may vary because provider infrastructure and model versions can change even when temperature is zero. Preserve the raw response, model name, provider, configuration, and timestamp.

## 5. Quality assurance

Before interpreting a real experiment:

1. Randomly sample at least 10% of rows.
2. Have two people independently label correctness, support, abstention, and hallucination.
3. Calculate Cohen's kappa for each label.
4. Adjudicate disagreements and update evaluator rules if needed.
5. Report both automated and human-reviewed metrics.

## 6. Ethics

Do not use this benchmark to claim that one model is universally safe or unsafe. Avoid sending sensitive or proprietary data to third-party APIs. Report negative and null results, disclose prompt and evaluation choices, and distinguish simulated demo findings from real-model findings.

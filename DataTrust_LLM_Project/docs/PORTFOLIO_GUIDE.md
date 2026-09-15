# Portfolio and Interview Guide

## 30-second explanation

I built a controlled experiment to measure how source-data quality affects LLM reliability. I held 100 questions constant, generated six versions of the supporting context, and measured accuracy, hallucination, unsupported claims, abstention, and confidence. I used bootstrap confidence intervals, a chi-square test, effect size, and logistic regression, then presented the findings in a Streamlit dashboard.

## What this demonstrates

- Experimental design and data generation
- Data cleaning and validation
- Exploratory data analysis
- Statistical inference and uncertainty communication
- Python package organization and testing
- Interactive data visualization
- Responsible interpretation of AI evaluation

## GitHub presentation checklist

- Replace demo results with real-model results if budget permits.
- Add one dashboard screenshot near the top of the README.
- Include the headline finding in one sentence.
- Keep the generated CSV and summary outputs so reviewers see immediate results.
- Add repository topics such as `data-science`, `llm`, `hallucination`, `rag`, `streamlit`, and `responsible-ai`.
- Record a 60–90 second dashboard walkthrough.

## Strong discussion points

- Why unsupported but factually correct answers count as hallucinations in a grounded RAG setting
- Why abstention is desirable when evidence is missing
- Why effect size and confidence intervals matter in addition to p-values
- Why self-reported confidence should not be treated as calibrated probability
- How repeated generations and human annotation would improve the next version

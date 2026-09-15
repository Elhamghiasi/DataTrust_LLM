from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).parent
RESULTS = ROOT / "data/processed/results.csv"
SUMMARY = ROOT / "outputs/analysis_summary.csv"
TESTS = ROOT / "outputs/statistical_tests.json"

st.set_page_config(page_title="DataTrust LLM", page_icon="🔎", layout="wide")
st.title("DataTrust LLM")
st.caption("How source-data quality changes hallucination, accuracy, abstention, and confidence")

if not RESULTS.exists() or not SUMMARY.exists():
    st.error("Results are not available. Run `make all` in the project directory first.")
    st.stop()

results = pd.read_csv(RESULTS)
summary = pd.read_csv(SUMMARY)
for column in ["answer_correct", "hallucinated", "abstained", "unsupported_claim"]:
    results[column] = results[column].astype(str).str.lower().map({"true": True, "false": False})

condition_options = summary["condition"].tolist()
selected = st.sidebar.multiselect("Context conditions", condition_options, default=condition_options)
filtered = results[results.condition.isin(selected)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Responses", f"{len(filtered):,}")
c2.metric("Accuracy", f"{filtered.answer_correct.mean():.1%}")
c3.metric("Hallucination", f"{filtered.hallucinated.mean():.1%}")
c4.metric("Abstention", f"{filtered.abstained.mean():.1%}")

left, right = st.columns(2)
with left:
    chart_data = summary[summary.condition.isin(selected)]
    fig = px.bar(
        chart_data,
        x="condition",
        y="hallucination_rate",
        error_y=chart_data.hallucination_ci_high - chart_data.hallucination_rate,
        error_y_minus=chart_data.hallucination_rate - chart_data.hallucination_ci_low,
        color="condition",
        title="Hallucination rate with 95% bootstrap CI",
        labels={"condition": "Context condition", "hallucination_rate": "Hallucination rate"},
    )
    fig.update_yaxes(tickformat=".0%", range=[0, 1])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    melted = summary[summary.condition.isin(selected)].melt(
        id_vars="condition",
        value_vars=["accuracy_rate", "abstention_rate", "unsupported_claim_rate"],
        var_name="metric",
        value_name="rate",
    )
    fig = px.bar(melted, x="condition", y="rate", color="metric", barmode="group", title="Reliability outcomes")
    fig.update_yaxes(tickformat=".0%", range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Confidence and correctness")
fig = px.strip(
    filtered,
    x="condition",
    y="self_reported_confidence",
    color=filtered["answer_correct"].map({True: "Correct", False: "Incorrect"}),
    hover_data=["question_id", "parsed_answer", "gold_answer"],
    labels={"color": "Outcome", "self_reported_confidence": "Self-reported confidence"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Inspect individual responses")
question = st.selectbox("Question", filtered.question_id.unique())
inspection = filtered[filtered.question_id == question][
    ["condition", "question", "context", "gold_answer", "parsed_answer", "self_reported_confidence", "answer_correct", "hallucinated"]
]
st.dataframe(inspection, use_container_width=True, hide_index=True)

with st.expander("Statistical test details"):
    if TESTS.exists():
        st.json(json.loads(TESTS.read_text(encoding="utf-8")))

st.info("Demo-mode results validate the workflow but should not be interpreted as measurements of a production LLM. Switch to the OpenAI provider for a real model experiment.")

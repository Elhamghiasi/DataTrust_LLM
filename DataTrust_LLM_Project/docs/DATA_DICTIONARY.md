# Data Dictionary

## Questions dataset

| Field | Type | Description |
|---|---|---|
| `question_id` | string | Stable question identifier |
| `domain` | string | Knowledge domain |
| `difficulty` | category | Coarse difficulty label |
| `question` | string | Prompted factual question |
| `gold_answer` | string | Verified reference answer |
| `clean_context` | string | Correct source passage |
| `source` | string | Source attribution |

## Results dataset

The result file contains the question fields plus:

| Field | Type | Description |
|---|---|---|
| `condition` | category | Applied context-quality treatment |
| `context` | string | Final context supplied to the model |
| `provider` | string | Mock or API provider |
| `model` | string | Model identifier |
| `raw_response` | string | Complete model response |
| `parsed_answer` | string | Extracted answer |
| `self_reported_confidence` | float | Model-provided confidence, 0–1 |
| `latency_ms` | float | Request latency in milliseconds |
| `response_chars` | integer | Response length in characters |
| `run_timestamp_utc` | datetime | UTC generation time |
| `abstained` | boolean | Detected abstention |
| `answer_correct` | boolean | Gold-answer match |
| `context_supports_gold` | boolean | Gold claim appears in context |
| `unsupported_claim` | boolean | Definite answer lacks supporting context |
| `hallucinated` | boolean | Definite answer incorrect or unsupported |
| `appropriate_abstention` | boolean | Abstention when context lacks support |
| `confidence_error` | float | Absolute confidence/correctness difference |

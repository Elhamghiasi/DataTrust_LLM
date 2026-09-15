.PHONY: data experiment evaluate analyze all test dashboard clean

data:
	python scripts/generate_data.py

experiment: data
	python scripts/run_experiment.py --overwrite

evaluate: experiment
	python scripts/evaluate_results.py

analyze: evaluate
	python scripts/analyze_results.py

all: analyze

test:
	pytest -q

dashboard:
	streamlit run app.py

clean:
	rm -f data/raw/questions.csv data/processed/results.csv
	rm -rf outputs

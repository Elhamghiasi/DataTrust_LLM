import pandas as pd

from datatrust.config import load_config, project_path
from datatrust.evaluation import evaluate_frame


def main() -> None:
    config = load_config()
    path = project_path(config["project"]["results_path"])
    frame = pd.read_csv(path, dtype={"gold_answer": str, "parsed_answer": str})
    evaluated = evaluate_frame(frame, config["evaluation"]["abstention_phrases"])
    evaluated.to_csv(path, index=False)
    print(f"Evaluated {len(evaluated)} rows and updated {path}")


if __name__ == "__main__":
    main()

import argparse
import pandas as pd

from datatrust.config import load_config, project_path
from datatrust.experiment import run_experiment, save_results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the data-quality experiment.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing results file.")
    args = parser.parse_args()
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    config = load_config()
    questions_path = project_path(config["project"]["questions_path"])
    results_path = project_path(config["project"]["results_path"])
    if results_path.exists() and not args.overwrite:
        raise SystemExit(f"{results_path} exists. Use --overwrite to replace it.")
    questions = pd.read_csv(questions_path, dtype={"gold_answer": str})
    results = run_experiment(questions, config)
    save_results(results, results_path)
    print(f"Saved {len(results)} experiment rows to {results_path}")


if __name__ == "__main__":
    main()

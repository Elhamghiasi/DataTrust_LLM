from datatrust.config import load_config, project_path
from datatrust.data import save_questions


def main() -> None:
    config = load_config()
    path = project_path(config["project"]["questions_path"])
    frame = save_questions(path)
    print(f"Saved {len(frame)} verified questions to {path}")


if __name__ == "__main__":
    main()

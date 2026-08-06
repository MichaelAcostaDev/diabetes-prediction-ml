from pathlib import Path

from predictor import DiabetesPredictor


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "diabetes.csv"
    model_path = base_dir / "model.pkl"

    predictor = DiabetesPredictor(data_path=data_path, model_path=model_path)
    predictor.train_if_needed()
    print(f"Model trained and saved to {model_path}")


if __name__ == "__main__":
    main()

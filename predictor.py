import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils.validation import check_array
from typing import Dict, List, Optional


class DiabetesPredictor:
    def __init__(self, data_path: Path, model_path: Path) -> None:
        self.data_path = data_path
        self.model_path = model_path
        self.scaler: Optional[StandardScaler] = None
        self.model: Optional[SVC] = None
        self.feature_names: List[str] = []
        self._load_dataset()
        self._load_model()

    def _load_dataset(self) -> None:
        df = pd.read_csv(self.data_path)
        if "Outcome" not in df.columns:
            raise ValueError("Dataset must contain the Outcome column.")
        self.feature_names = [col for col in df.columns if col != "Outcome"]
        self._dataset = df

    def _load_model(self) -> None:
        if self.model_path.exists():
            try:
                loaded = joblib.load(self.model_path)
                self.scaler = loaded["scaler"]
                self.model = loaded["model"]
            except Exception as error:
                raise RuntimeError(f"Failed to load model artifact: {error}")

    def train_if_needed(self) -> None:
        if self.model is not None and self.scaler is not None:
            return
        self._train_model()

    def _train_model(self) -> None:
        df = self._dataset.copy()
        x = df.drop(columns="Outcome")
        y = df["Outcome"]
        self.scaler = StandardScaler()
        self.scaler.fit(x)
        x_scaled = self.scaler.transform(x)
        x_train, _, y_train, _ = train_test_split(x_scaled, y, test_size=0.2)
        self.model = SVC(kernel="linear", probability=True)
        self.model.fit(x_train, y_train)
        joblib.dump({"scaler": self.scaler, "model": self.model}, self.model_path)

    def validate_inputs(self, values: Dict[str, str]) -> Dict[str, str]:
        errors: Dict[str, str] = {}
        for field in self.feature_names:
            raw_value = values.get(field)
            if raw_value is None or str(raw_value).strip() == "":
                errors[field] = "required"
                continue
            try:
                value = float(raw_value)
            except ValueError:
                errors[field] = "invalid"
                continue
            if value < 0:
                errors[field] = "negative"
        return errors

    def predict(self, values: Dict[str, str]) -> Dict[str, object]:
        if self.scaler is None or self.model is None:
            raise RuntimeError("Model is not trained or loaded.")
        raw_features = [float(values[field]) for field in self.feature_names]
        features = check_array([raw_features], ensure_2d=True, dtype=float)
        scaled_features = self.scaler.transform(features)
        predicted = int(self.model.predict(scaled_features)[0])
        probability = float(self.model.predict_proba(scaled_features).max())
        return {
            "label": predicted,
            "confidence": round(probability * 100.0, 1),
            "raw_probability": probability,
        }

import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from predictor import DiabetesPredictor
from translations import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE, TRANSLATIONS

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "diabetes.csv"
MODEL_PATH = BASE_DIR / "model.pkl"


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    predictor = DiabetesPredictor(data_path=DATA_PATH, model_path=MODEL_PATH)
    predictor.train_if_needed()

    @app.route("/")
    def index() -> Any:
        lang = request.args.get("lang", DEFAULT_LANGUAGE)
        if lang not in AVAILABLE_LANGUAGES:
            lang = DEFAULT_LANGUAGE
        translation = TRANSLATIONS[lang]
        return render_template(
            "index.html",
            lang=lang,
            translations=translation,
            languages=AVAILABLE_LANGUAGES,
            feature_names=predictor.feature_names,
            field_labels=translation["fields"],
            placeholders=translation["placeholders"],
        )

    @app.route("/predict", methods=["POST"])
    def predict() -> Any:
        request_data = request.json or {}
        values = request_data.get("data", {})
        lang = request_data.get("lang", DEFAULT_LANGUAGE)
        if lang not in AVAILABLE_LANGUAGES:
            lang = DEFAULT_LANGUAGE
        translation = TRANSLATIONS[lang]

        validation_errors = predictor.validate_inputs(values)
        if validation_errors:
            translated_errors = {}
            for field, error_code in validation_errors.items():
                if error_code == "required":
                    translated_errors[field] = translation["required_field"]
                else:
                    translated_errors[field] = translation["invalid_number"]
            return jsonify({"success": False, "errors": translated_errors}), 400

        result = predictor.predict(values)
        message = (
            translation["result_positive"] if result["label"] == 1 else translation["result_negative"]
        )
        explanation = (
            translation["explanation_positive"] if result["label"] == 1 else translation["explanation_negative"]
        )

        return jsonify(
            {
                "success": True,
                "prediction_label": message,
                "confidence": result["confidence"],
                "explanation": explanation,
                "probability_text": translation["probability_text"],
                "confidence_text": translation["confidence_text"],
            }
        )

    @app.route("/health")
    def health() -> Any:
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    try:
        webbrowser.open(server_url)
    except Exception:
        pass

    app.run(host="0.0.0.0", port=5000)

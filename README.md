# Diabetes Terminal Predictor

A polished Flask application with a cyberpunk terminal interface for predicting diabetes using a trained Scikit-Learn model.

## Architecture

- `app.py`: Flask web server and template rendering.
- `predictor.py`: Model training, loading, validation, and prediction logic.
- `translations.py`: Centralized translation dictionary for Spanish and English.
- `templates/index.html`: User interface with dynamic form generation.
- `static/css/style.css`: Cyberpunk terminal design.
- `static/js/app.js`: Frontend interactivity, validation, language switching, and progress animation.
- `diabetes.csv`: Dataset used for training.
- `model.pkl`: Serialized trained model and scaler.
- `requirements.txt`: Python dependencies.
- `vercel.json`: Vercel deployment configuration.

## Features

- Uses the exact preprocessing pipeline from the notebook:
  - Drops `Outcome` from input features.
  - Standardizes input values with `StandardScaler`.
  - Trains an `SVC(kernel='linear')` model.
- Two languages supported: English and Español.
- Terminal-inspired cyberpunk UI.
- Input validation for required and non-negative values.
- Shows predicted label, confidence, and explanation.
- Progress bar and clear button.

## Local setup

1. Create and activate a Python environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000` in the browser.

## Notes

- The notebook remains unchanged and is only used as reference.
- The model train happens once if necessary and is saved to `model.pkl`.
- The form fields are generated automatically from the CSV headers.

## License

MIT License

## 🧑‍💻 Owner
MichaelAcostaDev

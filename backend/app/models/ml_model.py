import joblib
import pandas as pd
import os
from typing import Any
import traceback
from fastapi import FastAPI

# Define path for the saved ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'carbon_score_predictor.joblib')

def load_ml_model(app: FastAPI):
    """
    Loads the pre-trained ML model pipeline and stores it in app.state.
    """
    print(f"Attempting to load ML model from: {MODEL_PATH}")
    print(f"[DEBUG] Model file exists? {os.path.exists(MODEL_PATH)}")
    
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            app.state.ml_model_pipeline = model  # ✅ Store in app state
            print("ML model pipeline loaded successfully!")
        except Exception as e:
            print(f"Error loading ML model: {e}")
            traceback.print_exc()
            raise RuntimeError(f"Could not load ML model: {e}")
    else:
        print(f"ML model file not found at {MODEL_PATH}")
        raise FileNotFoundError(f"ML model file not found at {MODEL_PATH}")

def predict_carbon_score_with_model(product_data: pd.DataFrame, model: Any) -> float:
    """
    Uses the provided ML model to predict the carbon score.
    """
    if model is None:
        raise RuntimeError("ML model not loaded. Please ensure it's passed to the function.")

    predicted_score = model.predict(product_data)[0]
    return predicted_score

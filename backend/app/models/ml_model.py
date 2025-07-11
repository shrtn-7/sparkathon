import joblib
import pandas as pd
import os
from typing import Any

# Define path for the saved ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'carbon_score_predictor.joblib')

ml_model_pipeline: Any = None # Type hint as Any because joblib.load returns a generic object

def load_ml_model():
    """
    Loads the pre-trained ML model pipeline.
    """
    global ml_model_pipeline
    print(f"Attempting to load ML model from: {MODEL_PATH}")
    if os.path.exists(MODEL_PATH):
        try:
            ml_model_pipeline = joblib.load(MODEL_PATH)
            print("ML model pipeline loaded successfully!")
            return ml_model_pipeline
        except Exception as e:
            print(f"Error loading ML model: {e}")
            raise RuntimeError(f"Could not load ML model: {e}")
    else:
        print(f"ML model file not found at {MODEL_PATH}")
        raise FileNotFoundError(f"ML model file not found at {MODEL_PATH}")

def predict_carbon_score_with_model(product_data: pd.DataFrame) -> float:
    """
    Uses the loaded ML model to predict the carbon score for a given product.
    Args:
        product_data (pd.DataFrame): A DataFrame containing the product's features.
                                     Ensure column names match the training data.
    Returns:
        float: The predicted carbon score.
    Raises:
        RuntimeError: If the ML model is not loaded.
    """
    if ml_model_pipeline is None:
        raise RuntimeError("ML model not loaded. Please ensure it's loaded on startup.")
    
    # The pipeline's preprocessor will handle feature selection and transformation
    predicted_score = ml_model_pipeline.predict(product_data)[0]
    return predicted_score

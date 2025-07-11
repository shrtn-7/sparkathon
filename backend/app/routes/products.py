from fastapi import APIRouter, HTTPException, status
import pandas as pd

from app.schemas.product import ProductInput, CarbonScoreOutput
from app.models.ml_model import ml_model_pipeline, predict_carbon_score_with_model

router = APIRouter()

@router.post("/predict-score", response_model=CarbonScoreOutput, summary="Predict Carbon Score for a Product")
async def predict_score(product: ProductInput):
    """
    Accepts product attributes as JSON and returns the predicted carbon score.
    The prediction is made using the pre-trained ML model.
    """
    if ml_model_pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not loaded. Server is still initializing or encountered an error."
        )

    # Convert Pydantic model to pandas DataFrame for prediction
    product_df = pd.DataFrame([product.model_dump()])

    # Make prediction
    try:
        predicted_score = predict_carbon_score_with_model(product_df)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {e}"
        )

    return CarbonScoreOutput(carbon_score=predicted_score)
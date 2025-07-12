from fastapi import APIRouter, HTTPException, status, Request
import pandas as pd
from app.schemas.product import ProductInput, CarbonScoreOutput
from app.models import ml_model

router = APIRouter()

@router.post("/predict-score", response_model=CarbonScoreOutput)
async def predict_score(product: ProductInput, request: Request):
    print("[DEBUG] predict_score endpoint called")

    if not hasattr(request.app.state, "ml_model_pipeline"):
        print("[DEBUG] app.state has no ml_model_pipeline")
    else:
        print("[DEBUG] app.state.ml_model_pipeline exists")

    model = getattr(request.app.state, "ml_model_pipeline", None)

    if model is None:
        print("[ERROR] ml_model_pipeline is None at request time")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not loaded. Server is still initializing or encountered an error."
        )

    try:
        product_df = pd.DataFrame([product.model_dump()])
        print("[DEBUG] DataFrame prepared for prediction")
        predicted_score = ml_model.predict_carbon_score_with_model(product_df, model)
        print("[DEBUG] Prediction completed successfully")
        return CarbonScoreOutput(carbon_score=predicted_score)
    except Exception as e:
        print(f"[ERROR] Exception during prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {e}"
        )

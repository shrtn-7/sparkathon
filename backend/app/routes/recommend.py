from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
import pandas as pd

from app.schemas.product import (
    ProductInput, ProductIdInput, AlternativesOutput,
    AlternativeProduct, CatalogProduct
)
from app.data.catalog import get_all_products, get_product_by_id
from app.models.ml_model import ml_model_pipeline, predict_carbon_score_with_model

router = APIRouter()

@router.post("/get-alternatives", response_model=AlternativesOutput, summary="Get Greener Alternatives for a Product")
async def get_greener_alternatives(
    product_input: Optional[ProductInput] = None,
    product_id_input: Optional[ProductIdInput] = None
):
    """
    Accepts either a product ID or full product JSON, and returns up to 3 greener alternatives
    from the loaded product catalog. Alternatives must be in the same category and have a lower carbon score.
    """
    product_catalog_df = get_all_products() # Ensure catalog is loaded
    if product_catalog_df is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product catalog not loaded. Server is still initializing or encountered an error."
        )

    original_product_carbon_score: float
    original_product_category: str
    original_product_details: Optional[CatalogProduct] = None
    original_product_id_val: Optional[int] = None
    message: str = ""

    if product_id_input and product_id_input.product_id:
        original_product_id_val = product_id_input.product_id
        original_product_series = get_product_by_id(original_product_id_val)

        if original_product_series is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {original_product_id_val} not found in the catalog."
            )
        
        original_product_carbon_score = original_product_series['carbon_score']
        original_product_category = original_product_series['category']
        
        # Create a CatalogProduct object for response
        original_product_details = CatalogProduct(
            product_id=original_product_id_val,
            product_name=original_product_series['product_name'],
            category=original_product_series['category'],
            origin_country=original_product_series['origin_country'],
            weight_kg=original_product_series['weight_kg'],
            packaging=original_product_series['packaging'],
            delivery_method=original_product_series['delivery_method'],
            delivery_distance_km=original_product_series['delivery_distance_km'],
            delivery_speed=original_product_series['delivery_speed'],
            carbon_score=original_product_series['carbon_score']
        )
        message = f"Alternatives for product ID {original_product_id_val} (Category: {original_product_category}, Carbon Score: {original_product_carbon_score:.2f})."

    elif product_input:
        # Predict carbon score for the provided product JSON
        if ml_model_pipeline is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model not loaded. Cannot predict score for new product."
            )
        
        product_df_for_prediction = pd.DataFrame([product_input.model_dump()])
        try:
            original_product_carbon_score = predict_carbon_score_with_model(product_df_for_prediction)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error predicting carbon score for input product: {e}"
            )
        
        original_product_category = product_input.category
        message = f"Alternatives for provided product (Category: {original_product_category}, Predicted Carbon Score: {original_product_carbon_score:.2f})."

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'product_id_input' or 'product_input' must be provided."
        )

    # Filter for greener alternatives
    # Ensure we don't include the original product itself if it came from the catalog
    alternatives_query = (
        (product_catalog_df['category'] == original_product_category) &
        (product_catalog_df['carbon_score'] < original_product_carbon_score)
    )
    
    # If the original product came from the catalog, exclude it from alternatives
    if original_product_id_val is not None:
        alternatives_query &= (product_catalog_df.index != original_product_id_val)

    greener_alternatives = product_catalog_df[alternatives_query].sort_values(
        by='carbon_score', ascending=True
    ).head(3)

    if greener_alternatives.empty:
        message += " No greener alternatives found in the catalog."
        return AlternativesOutput(
            original_product_id=original_product_id_val,
            original_product_details=original_product_details,
            original_product_carbon_score=original_product_carbon_score,
            alternatives=[],
            message=message
        )
    
    # Format alternatives for response
    formatted_alternatives: List[AlternativeProduct] = []
    for product_id, row in greener_alternatives.iterrows():
        formatted_alternatives.append(
            AlternativeProduct(
                product_id=product_id,
                product_name=row['product_name'],
                category=row['category'],
                origin_country=row['origin_country'],
                weight_kg=row['weight_kg'],
                packaging=row['packaging'],
                delivery_method=row['delivery_method'],
                delivery_distance_km=row['delivery_distance_km'],
                delivery_speed=row['delivery_speed'],
                carbon_score=row['carbon_score'],
                is_predicted_score=False # These are actual scores from the catalog
            )
        )
    
    message += f" Found {len(formatted_alternatives)} greener alternative(s)."
    return AlternativesOutput(
        original_product_id=original_product_id_val,
        original_product_details=original_product_details,
        original_product_carbon_score=original_product_carbon_score,
        alternatives=formatted_alternatives,
        message=message
    )

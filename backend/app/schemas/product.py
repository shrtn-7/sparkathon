from pydantic import BaseModel, Field
from typing import List, Optional

# Base model for product attributes used in prediction
class ProductBase(BaseModel):
    category: str = Field(..., example="Electronics", description="Category of the product")
    origin_country: str = Field(..., example="China", description="Country of origin")
    weight_kg: float = Field(..., gt=0, example=0.5, description="Weight of the product in kilograms")
    packaging: str = Field(..., example="Plastic", description="Type of packaging (e.g., Plastic, Cardboard, Recycled)")
    delivery_method: str = Field(..., example="Air", description="Method of delivery (e.g., Air, Sea, Road)")
    delivery_distance_km: int = Field(..., ge=0, example=5000, description="Delivery distance in kilometers")
    # delivery_speed is in the original dataset but was not used in the ML model features
    # Keeping it here for completeness if the frontend sends it, but it will be dropped by the preprocessor.
    delivery_speed: str = Field(..., example="Standard", description="Speed of delivery (e.g., Standard, Express)")

# Input model for predicting carbon score
class ProductInput(ProductBase):
    pass # Inherits all fields from ProductBase

# Output model for predicted carbon score
class CarbonScoreOutput(BaseModel):
    carbon_score: float = Field(..., description="Predicted carbon score of the product")

# Model for a product in the catalog (including ID and actual score)
class CatalogProduct(ProductBase):
    product_id: int = Field(..., example=1001, description="Unique identifier for the product")
    product_name: str = Field(..., example="EcoPhone X", description="Name of the product")
    carbon_score: float = Field(..., description="Actual carbon score of the product")

# Input model for getting alternatives by product ID
class ProductIdInput(BaseModel):
    product_id: int = Field(..., example=1001, description="ID of the product to find alternatives for")

# Output model for alternative products
class AlternativeProduct(ProductBase): # Inherit ProductBase for common fields
    product_id: int
    product_name: str
    carbon_score: float
    is_predicted_score: bool = False # Indicates if this is a predicted score or actual (from catalog)

# Response model for alternatives endpoint
class AlternativesOutput(BaseModel):
    original_product_id: Optional[int] = Field(None, description="ID of the original product if provided")
    original_product_details: Optional[CatalogProduct] = Field(None, description="Details of the original product from catalog")
    original_product_carbon_score: float = Field(..., description="Carbon score of the original product (actual or predicted)")
    alternatives: List[AlternativeProduct] = Field(..., description="List of greener alternative products")
    message: str = Field(..., description="A message regarding the alternatives found")

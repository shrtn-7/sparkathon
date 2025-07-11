from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Import functions to load ML model and product catalog
from app.models.ml_model import load_ml_model
from app.data.catalog import load_product_catalog

# Import routers directly from their respective modules
# Using 'as' alias to avoid naming conflicts and make it clear these are router objects

from app.routes.products import router as products_router
from app.routes.recommend import router as recommend_router

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Carbon-Aware Product Recommendation Engine API",
    description="API for predicting product carbon scores and recommending greener alternatives.",
    version="0.1.0"
)

# --- CORS Middleware ---
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup Event: Load ML Model and Product Catalog ---
@app.on_event("startup")
async def startup_event():
    print("Application startup event triggered. Loading resources...")
    try:
        load_ml_model()
        load_product_catalog()
        print("All resources loaded successfully!")
    except Exception as e:
        print(f"Failed to load resources on startup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Backend failed to initialize: {e}"
        )

# --- Include Routers ---
app.include_router(products_router, prefix="/api", tags=["Products"])
app.include_router(recommend_router, prefix="/api", tags=["Recommendations"])

# --- Root Endpoint (Optional, for basic health check) ---
@app.get("/", summary="API Health Check")
async def read_root():
    return {"message": "Carbon-Aware Product Recommendation Engine API is running!"}


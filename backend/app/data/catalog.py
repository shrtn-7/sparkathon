import pandas as pd
import os
from typing import Optional

# Define path for the product catalog CSV
# Corrected path: Go up three levels from app/data/ to carbon-aware/, then into 'data' folder
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'carbon_aware_products_1000.csv')

product_catalog_df: pd.DataFrame = None

def load_product_catalog():
    """
    Loads the product catalog CSV into a pandas DataFrame.
    Sets 'product_id' as the index for efficient lookups.
    """
    global product_catalog_df
    print(f"Attempting to load product catalog from: {DATA_PATH}")
    if os.path.exists(DATA_PATH):
        try:
            product_catalog_df = pd.read_csv(DATA_PATH)
            # Set product_id as index for quick lookup
            product_catalog_df.set_index('product_id', inplace=True)
            print("Product catalog loaded successfully!")
            return product_catalog_df
        except Exception as e:
            print(f"Error loading product catalog: {e}")
            raise RuntimeError(f"Could not load product catalog: {e}")
    else:
        print(f"Product catalog file not found at {DATA_PATH}")
        raise FileNotFoundError(f"Product catalog file not found at {DATA_PATH}")

def get_product_by_id(product_id: int) -> Optional[pd.Series]:
    """Retrieves a product from the catalog by its ID."""
    if product_catalog_df is None:
        # This call ensures the catalog is loaded if it hasn't been yet by the startup event
        load_product_catalog() 

    if product_id in product_catalog_df.index:
        return product_catalog_df.loc[product_id]
    return None

def get_all_products() -> pd.DataFrame:
    """Returns the entire product catalog DataFrame."""
    if product_catalog_df is None:
        # This call ensures the catalog is loaded if it hasn't been yet by the startup event
        load_product_catalog() 
    return product_catalog_df

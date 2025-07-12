import uvicorn
import os
import sys

# For debugging: Print the current working Directory and sys.path
print(f"Current Working Directory: {os.getcwd()}")
print(f"Python System Path {sys.path}:")
for p in sys.path:
    print(f"  - {p}")

if __name__ == "__main__":
    # Ensure the current directory (backend/) is in the Python path
    # This is crucial for 'app.main' to be found when Uvicorn starts
    # If not already present, add it to the beginning of sys.path
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    
    # Get the port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Run the FastAPI app located at app/main.py
    # REMOVED: reload=True to bypass multiprocessing issues potentially related to Python 3.13
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, workers=1)

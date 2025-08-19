from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from sentence_transformers import SentenceTransformer, util
app = FastAPI(title="HR Resource Chatbot API",
              description="API for searching and recommending employees")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load model and data (same as before)
model = SentenceTransformer('all-MiniLM-L6-v2')
def load_employees():
    with open("employees_dataset.json", "r") as f:
        return json.load(f)["employees"]
employees = load_employees()
# (Keep all the existing backend code from previous implementation)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
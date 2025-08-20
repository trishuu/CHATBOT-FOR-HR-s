# app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
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

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load employee data from JSON file
def load_employees():
    try:
        with open("employees_dataset.json", "r") as f:
            return json.load(f)["employees"]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Employee dataset not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON data.")

employees = load_employees()

# Pydantic model for chat requests
class ChatRequest(BaseModel):
    text: str

# Pydantic model for employee responses
class EmployeeResponse(BaseModel):
    name: str
    skills: List[str]
    experience_years: int
    past_projects: List[str]
    availability: str

# Helper function to find employees by query
def find_employees_by_query(query_text: str) -> List[EmployeeResponse]:
    """Find employees using semantic similarity"""
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    employee_skills = ["; ".join(emp["skills"]) for emp in employees]
    employee_embeddings = model.encode(employee_skills, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(query_embedding, employee_embeddings)
    top_results = similarities[0].topk(min(5, len(employees)))
    return [employees[idx] for idx in top_results[1]]

# Helper function to filter employees by criteria
def filter_employees(skill: Optional[str] = None, 
                     min_experience: Optional[int] = None,
                     project: Optional[str] = None) -> List[EmployeeResponse]:
    """Filter employees by exact criteria"""
    results = employees
    
    if skill:
        results = [e for e in results if skill.lower() in [s.lower() for s in e["skills"]]]
    if min_experience is not None:
        results = [e for e in results if e["experience_years"] >= min_experience]
    if project:
        results = [e for e in results if any(project.lower() in p.lower() for p in e["past_projects"])]
    
    return results

# Root endpoint
@app.get("/")
async def read_root():
    return FileResponse('Frontend/index.html')

# Endpoint for chat queries
@app.post("/chat", response_model=dict)
async def chat_query(request: ChatRequest):
    """
    Handle natural language queries about employees
    Example: {"text": "Find Python developers with 3+ years experience"}
    """
    print(f"Received query: {request.text}")
    matched = find_employees_by_query(request.text)
    print(f"Found {len(matched)} matches")
    
    return {
        "query": request.text,
        "results": matched,
        "count": len(matched)
    }

# Endpoint for searching employees
@app.get("/employees/search", response_model=dict)
async def search_employees(
    skill: Optional[str] = Query(None, description="Filter by skill"),
    min_experience: Optional[int] = Query(None, ge=0, description="Minimum years of experience"),
    project: Optional[str] = Query(None, description="Filter by project")
):
    """
    Search employees using exact criteria filters
    Example: /employees/search?skill=Python&min_experience=3
    """
    results = filter_employees(skill, min_experience, project)
    return {
        "filters": {
            "skill": skill,
            "min_experience": min_experience,
            "project": project
        },
        "results": results,
        "count": len(results)
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

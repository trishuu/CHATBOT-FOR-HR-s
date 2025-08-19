from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import json
from typing import List, Dict

app = FastAPI()

# Load employee data from JSON file
def load_employees() -> List[Dict]:
    with open("employees_dataset.json", "r") as f:
        data = json.load(f)
    return data["employees"]

employees = load_employees()

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

class Query(BaseModel):
    text: str

def process_query(query_text: str) -> str:
    """Integrated RAG pipeline"""
    # 1. Retrieval - Find relevant employees
    employee_skills = ["; ".join(emp['skills']) for emp in employees]
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    employee_embeddings = model.encode(employee_skills, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, employee_embeddings)
    top_results = similarities[0].topk(min(5, len(employees)))
    relevant_employees = [employees[idx] for idx in top_results[1]]
    
    if not relevant_employees:
        return "No matching employees found."

    # 2 & 3. Augmentation & Generation - Create natural language response
    response = f"Recommendations for '{query_text}':\n"
    for i, emp in enumerate(relevant_employees, 1):
        projects = ", ".join(emp['past_projects']) if emp['past_projects'] else "No project history"
        response += (
            f"\n{i}. {emp['name']}\n"
            f"   Skills: {', '.join(emp['skills'])}\n"
            f"   Experience: {emp['experience_years']} years\n"
            f"   Projects: {projects}\n"
            f"   Availability: {emp['availability']}\n"
        )
    
    return response

@app.get("/")
def home():
    return {"message": "HR Chatbot API", "docs": "/docs"}

@app.post("/query")
async def handle_query(query: Query):
    response = process_query(query.text)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

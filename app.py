from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Prompt Engineering System")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Import PromptEngineeringCrew conditionally to handle missing dependencies
try:
    from main import PromptEngineeringCrew
    prompt_crew = PromptEngineeringCrew()
    CREW_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not initialize PromptEngineeringCrew: {str(e)}")
    print("Using mock data instead. Make sure GROQ_API_KEY is set in .env file.")
    CREW_AVAILABLE = False

# Pydantic models for requests
class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query_id: int
    effectiveness_rating: int
    clarity_rating: int
    comments: Optional[str] = None

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "crew_available": CREW_AVAILABLE}

@app.post("/api/optimize")
async def optimize_prompt(query_req: QueryRequest):
    """Process a query and return optimized prompt"""
    try:
        if CREW_AVAILABLE:
            # Use the actual crew if available
            result = prompt_crew.optimize_prompt(query_req.query)
            return result
        else:
            # Return mock data for testing/demonstration
            return {
                "query_id": 1,
                "research": f"Sample research for query: {query_req.query}\n\nThis is a detailed analysis of your query '{query_req.query}'.\n\n1. Core Requirements:\n   - Functionality needed\n   - User interactions\n   - Expected outputs\n\n2. Architecture Components:\n   - Frontend interface\n   - Backend processing\n   - Database requirements\n\n3. Recommended Libraries:\n   - CrewAI for agent orchestration\n   - FastAPI for web interface\n   - SQLAlchemy for database\n\n4. Key Functions Needed:\n   - Query analysis\n   - Template matching\n   - Response generation\n   - Feedback processing",
                "optimized_prompt": f"OPTIMIZED PROMPT:\n\nDesign and implement a {query_req.query} system with the following specifications:\n\n1. Architecture:\n   - Create a modular system with clear separation of concerns\n   - Implement an intuitive user interface for interaction\n   - Build a robust backend for data processing\n\n2. Implementation Requirements:\n   - Use modern libraries and frameworks for efficiency\n   - Ensure scalability through proper design patterns\n   - Implement comprehensive error handling\n   - Add detailed logging for debugging\n\n3. Features to Include:\n   - User authentication and authorization\n   - Data validation and sanitization\n   - Responsive design for multiple devices\n   - Performance optimization\n\n4. Deliverables:\n   - Complete source code with documentation\n   - Installation and usage instructions\n   - Testing suite for verification\n\nProvide a comprehensive solution with code examples for key components and explanations of design decisions.",
                "evaluation": "Evaluation of the optimized prompt:\n\nStrengths:\n- The prompt provides clear structure and organization\n- Requirements are well-defined and comprehensive\n- Implementation guidance is specific yet flexible\n\nWeaknesses:\n- Could benefit from more specific examples\n- Some technical requirements could be more detailed\n- Consider adding constraints on solution complexity\n\nSuggested improvements:\n- Add example input/output scenarios\n- Specify preferred programming languages or frameworks\n- Include performance benchmarks or requirements\n\nOverall rating: 8/10",
                "summary": "Process complete."
            }
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Save user feedback on a prompt"""
    try:
        if CREW_AVAILABLE:
            success = prompt_crew.save_feedback(
                feedback.query_id,
                feedback.effectiveness_rating,
                feedback.clarity_rating,
                feedback.comments
            )
            if not success:
                return {"success": False, "message": "Failed to save feedback"}
        return {"success": True, "message": "Feedback recorded successfully"}
    except Exception as e:
        print(f"Error saving feedback: {str(e)}")
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
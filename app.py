import os
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from services.gemini_service import generate_answer
from services.tavily_service import search_evidence
from services.verifier_service import verify_answer
import asyncio

app = FastAPI(
    title="AI Hallucination Confidence Labeler",
    description="Phase 3: Ask questions, get answers from Gemini, verify with Tavily Search, and label hallucination confidence.",
    version="3.0.0"
)

# Serve static files (CSS, JS)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Pydantic model for validating the incoming request body
class AskRequest(BaseModel):
    question: str = Field(..., description="The question to ask Gemini", min_length=1)

# Endpoint to serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frontend index.html template file not found."
        )
    return FileResponse(index_path)

# Endpoint to process the question
@app.post("/ask")
async def ask_question(request: AskRequest):
    # Validate the question string is not just whitespace
    question_stripped = request.question.strip()
    if not question_stripped:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be blank. Please enter a valid question."
        )

    try:
        # 1. Query Gemini and Tavily concurrently
        answer_task = generate_answer(question_stripped)
        sources_task = search_evidence(question_stripped)
        
        answer, sources = await asyncio.gather(answer_task, sources_task)
        
        # 2. Compare answer against evidence using verifier service
        verification = await verify_answer(question_stripped, answer, sources)
        
        return {
            "question": question_stripped,
            "answer": answer,
            "sources": sources,
            "verification": verification
        }
    except ValueError as val_err:
        # Catch configuration errors (e.g. GEMINI_API_KEY missing) or bad request input
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Gemini API Free Tier daily requests quota exceeded (429). Please add/change the 'GEMINI_MODEL' environment variable in your .env file to a model with remaining daily requests quota (e.g. 'gemini-1.5-flash' or 'gemini-2.5-flash-8b') and restart the server, or wait for your daily quota to reset."
            )
        # Catch unexpected API errors or network issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )

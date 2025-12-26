"""FastAPI application for English to Spanish translation."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .model import translate_text, load_model
from .config import API_HOST, API_PORT
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="English to Spanish Translation API",
    description="Translation service using Helsinki-NLP transformer model",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="English text to translate")


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str


class HealthResponse(BaseModel):
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    """Load model on application startup."""
    print("Starting up translation service...")
    try:
        load_model()
        print("Service ready!")
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Translation service is running"
    )


@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate English text to Spanish.
    
    Args:
        request: TranslationRequest containing English text
        
    Returns:
        TranslationResponse with original and translated text
    """
    try:
        translated = translate_text(request.text)
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


# Mount static files (frontend) - must be after all API routes
frontend_path = "/app/frontend"
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)


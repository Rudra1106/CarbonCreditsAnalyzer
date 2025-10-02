from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Carbon Credit Analyzer API",
    description="AI-powered analysis of farmland for carbon credit potential",
    version="1.0.0"
)

# CORS middleware (allows frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - Welcome message
@app.get("/")
async def root():
    return {
        "message": "Welcome to Carbon Credit Analyzer API",
        "status": "running",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_keys_loaded": {
            "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY"))
        }
    }

# Test endpoint to verify your setup
@app.get("/test")
async def test():
    return {
        "message": "FastAPI is working correctly!",
        "tips": [
            "Visit /docs for interactive API documentation",
            "Visit /health to check API key configuration",
            "Next: We'll add image upload capability"
        ]
    }
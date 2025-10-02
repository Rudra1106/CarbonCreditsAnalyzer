from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uuid

# Import our custom modules
from utils.image_processor import ImageProcessor
from utils.ai_client import AIClient
from models.schemas import UploadResponse, VisionAnalysis

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Carbon Credit Analyzer API",
    description="AI-powered analysis of farmland for carbon credit potential",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI client
ai_client = AIClient()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Carbon Credit Analyzer API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Upload and analyze farmland image",
            "GET /health": "Check API health and configuration",
            "GET /test-ai": "Test AI connection",
            "GET /docs": "Interactive API documentation"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_keys_loaded": {
            "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "cerebras": bool(os.getenv("CEREBRAS_API_KEY"))
        }
    }

# Test AI connection
@app.get("/test-ai")
async def test_ai_connection():
    """Test if OpenRouter API is working"""
    try:
        result = await ai_client.test_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main image analysis endpoint
@app.post("/analyze", response_model=dict)
async def analyze_land(
    file: UploadFile = File(..., description="Image of farmland/agricultural area")
):
    """
    Upload an image of farmland for carbon credit potential analysis
    
    Accepts: JPEG, PNG, WebP (max 10MB)
    Returns: Detailed analysis with carbon credit estimates
    """
    
    try:
        # Generate unique ID for this analysis
        analysis_id = str(uuid.uuid4())
        
        # Step 1: Process the image
        print(f"[{analysis_id}] Processing image: {file.filename}")
        base64_image, metadata = await ImageProcessor.process_image(file)
        image_quality = ImageProcessor.estimate_image_quality(metadata)
        
        print(f"[{analysis_id}] Image processed: {metadata}")
        
        # Step 2: Analyze with Llama Vision
        print(f"[{analysis_id}] Sending to Llama Vision for analysis...")
        vision_result = await ai_client.analyze_image_with_llama_vision(
            base64_image, 
            metadata
        )
        
        print(f"[{analysis_id}] Vision analysis complete")
        
        # Step 3: Add image quality to result
        vision_result["image_quality"] = image_quality
        
        # Step 4: Return comprehensive result
        return {
            "analysis_id": analysis_id,
            "status": "success",
            "image_metadata": metadata,
            "vision_analysis": vision_result,
            "message": "Analysis complete! Next step: Carbon calculations (Day 2)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# Quick upload test endpoint
@app.post("/upload-test")
async def upload_test(file: UploadFile = File(...)):
    """Simple endpoint to test file upload without AI processing"""
    try:
        await ImageProcessor.validate_image(file)
        return {
            "status": "success",
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "File upload working correctly!"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🌱 Carbon Credit Analyzer API Starting...")
    print("=" * 50)
    print(f"✅ FastAPI server initialized")
    print(f"✅ CORS enabled for all origins")
    
    # Check API keys
    if os.getenv("OPENROUTER_API_KEY"):
        print(f"✅ OpenRouter API key loaded")
    else:
        print(f"⚠️  OpenRouter API key missing!")
    
    print("=" * 50)
    print("📚 Visit http://localhost:8000/docs for API documentation")
    print("=" * 50)
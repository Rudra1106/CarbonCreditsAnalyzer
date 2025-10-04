from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
from typing import Optional, List, Dict

# Import our custom modules
from utils.image_processor import ImageProcessor
from utils.ai_client import AIClient
from utils.carbon_calculator import CarbonCalculator
from utils.report_generator import ReportGenerator
from utils.location_service import LocationService
from utils.chatbot_service import ChatbotService
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

# Initialize services
ai_client = AIClient()
carbon_calculator = CarbonCalculator()
report_generator = ReportGenerator()
location_service = LocationService()
chatbot_service = ChatbotService()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Carbon Credit Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /analyze": "Complete analysis with image + location + report",
            "POST /chat": "Ask questions about carbon credits or your analysis",
            "GET /chat/suggestions": "Get suggested questions",
            "GET /states": "Get list of Indian states",
            "GET /health": "API health check",
            "GET /docs": "Interactive documentation"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "weather": bool(os.getenv("OPENWEATHER_API_KEY"))
        }
    }

# Get states list
@app.get("/states")
async def get_states():
    return {
        "states": LocationService.get_state_list(),
        "total": len(LocationService.get_state_list())
    }

# Test chatbot connection
@app.get("/test-chatbot")
async def test_chatbot():
    """Test if Mistral chatbot is working via OpenRouter"""
    try:
        result = await chatbot_service.test_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chatbot endpoint
@app.post("/chat")
async def chat(
    message: str = Body(..., embed=True, description="Your question"),
    conversation_history: Optional[List[Dict[str, str]]] = Body(None, description="Previous messages"),
    user_analysis: Optional[Dict] = Body(None, description="Your complete analysis data for context")
):
    """
    Chat with AI assistant about carbon credits
    
    Features:
    - Full knowledge of your analysis report
    - Web search for current information
    - Personalized answers based on your land
    
    Ask questions like:
    - "What are carbon credits?"
    - "How was my revenue calculated?"
    - "Why is my confidence level medium?"
    - "What are the latest carbon credit prices in India?"
    - "Are there programs specific to Gujarat?"
    
    Provide your complete analysis data for personalized answers.
    """
    
    try:
        print(f"\n[CHAT] User: {message[:100]}...")
        
        result = await chatbot_service.chat(
            user_message=message,
            conversation_history=conversation_history,
            user_analysis=user_analysis
        )
        
        if result.get('search_performed'):
            print(f"[CHAT] Web search performed")
        
        print(f"[CHAT] Response: {result.get('response', '')[:100]}...")
        
        return {
            "status": result["status"],
            "response": result["response"],
            "tokens": result.get("tokens", {}),
            "model": result.get("model"),
            "search_performed": result.get("search_performed", False)
        }
        
    except Exception as e:
        print(f"[CHAT] Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )

# Get suggested questions
@app.post("/chat/suggestions")
async def get_suggestions(
    user_analysis: Optional[Dict] = Body(None, description="Your analysis data")
):
    """
    Get suggested questions based on your analysis
    
    Returns personalized question suggestions you can ask the chatbot.
    """
    
    try:
        suggestions = await chatbot_service.get_suggested_questions(user_analysis)
        return {
            "status": "success",
            "suggestions": suggestions
        }
    except Exception as e:
        return {
            "status": "error",
            "suggestions": [
                "What are carbon credits?",
                "How do I get started?",
                "What programs are available in India?"
            ]
        }

# MAIN ENDPOINT - Complete Analysis
@app.post("/analyze")
async def analyze_land(
    file: UploadFile = File(..., description="Farmland image (JPEG/PNG/WebP, max 10MB)"),
    city: Optional[str] = Form(None, description="City name (e.g., Surat)"),
    state: Optional[str] = Form(None, description="State name (e.g., Gujarat)"),
    include_report: bool = Form(True, description="Generate professional report (recommended)")
):
    """
    Complete farmland carbon credit analysis
    
    Upload image + location → Get analysis + report
    
    Parameters:
    - file: Farmland image
    - city: Your city (optional but recommended)
    - state: Your state (optional but recommended)
    - include_report: Generate reports (default: true)
    
    Returns: Complete analysis with vision, carbon calculations, and reports
    """
    
    analysis_id = str(uuid.uuid4())
    
    try:
        print(f"\n{'='*60}")
        print(f"[{analysis_id}] ANALYSIS STARTED")
        print(f"{'='*60}")
        
        # STEP 1: Process Image
        print(f"[{analysis_id}] Processing image: {file.filename}")
        base64_image, metadata = await ImageProcessor.process_image(file)
        image_quality = ImageProcessor.estimate_image_quality(metadata)
        print(f"[{analysis_id}] Image processed: {metadata['processed_dimensions']}")
        
        # STEP 2: Location Analysis (optional)
        location_data = None
        if city and state:
            print(f"[{analysis_id}] Fetching location data: {city}, {state}")
            try:
                location_data = await location_service.get_location_analysis(city, state)
                print(f"[{analysis_id}] Location multiplier: {location_data['climate_multiplier']}x")
                if location_data.get('weather_data'):
                    w = location_data['weather_data']
                    print(f"[{analysis_id}] Weather: {w['temperature']}°C, {w['humidity']}% humidity")
            except Exception as e:
                print(f"[{analysis_id}] Location fetch failed: {str(e)}")
                location_data = None
        else:
            print(f"[{analysis_id}] No location provided - using baseline")
        
        # STEP 3: AI Vision Analysis
        print(f"[{analysis_id}] Running Llama Vision analysis...")
        vision_result = await ai_client.analyze_image_with_llama_vision(
            base64_image, 
            metadata
        )
        vision_result["image_quality"] = image_quality
        
        print(f"[{analysis_id}] Vision complete:")
        print(f"[{analysis_id}]   Type: {vision_result['vegetation_type']}")
        print(f"[{analysis_id}]   Density: {vision_result['density_percentage']}%")
        print(f"[{analysis_id}]   Condition: {vision_result['land_condition']}")
        
        # STEP 4: Carbon Calculations
        print(f"[{analysis_id}] Calculating carbon potential...")
        carbon_analysis = carbon_calculator.calculate_complete_analysis(
            vision_result,
            metadata,
            location_data
        )
        
        carbon_est = carbon_analysis["carbon_estimate"]
        print(f"[{analysis_id}] Carbon calculations complete:")
        print(f"[{analysis_id}]   Annual CO2: {carbon_est['annual_sequestration_tons']} tons")
        print(f"[{analysis_id}]   Revenue (mid): ₹{carbon_est['potential_revenue_inr']['1_year']['mid']:,.0f}/year")
        
        # Build response
        response = {
            "analysis_id": analysis_id,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "image_metadata": metadata,
            "location_data": location_data,
            "vision_analysis": vision_result,
            "carbon_analysis": carbon_analysis,
            "summary": {
                "vegetation_type": vision_result["vegetation_type"],
                "land_condition": vision_result["land_condition"],
                "location": f"{city}, {state}" if (city and state) else "Not provided",
                "estimated_annual_revenue_inr": {
                    "conservative": carbon_est['potential_revenue_inr']['1_year']['min'],
                    "mid_range": carbon_est['potential_revenue_inr']['1_year']['mid'],
                    "optimistic": carbon_est['potential_revenue_inr']['1_year']['max']
                },
                "estimated_land_area_hectares": carbon_est['estimated_land_area_hectares'],
                "annual_co2_sequestration_tons": carbon_est['annual_sequestration_tons'],
                "confidence": carbon_est['confidence_level']
            }
        }
        
        # STEP 5: Generate Reports (if requested)
        if include_report:
            print(f"[{analysis_id}] Generating reports...")
            try:
                full_report = await report_generator.generate_full_report(response)
                exec_summary = await report_generator.generate_executive_summary(response)
                text_summary = await report_generator.generate_simple_text_summary(response)
                
                response["reports"] = {
                    "full_report_markdown": full_report,
                    "executive_summary": exec_summary,
                    "text_summary": text_summary
                }
                print(f"[{analysis_id}] Reports generated")
            except Exception as e:
                print(f"[{analysis_id}] Report generation failed: {str(e)}")
                response["reports"] = {"error": str(e)}
        
        print(f"[{analysis_id}] COMPLETE")
        print(f"{'='*60}\n")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[{analysis_id}] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("Carbon Credit Analyzer API")
    print("=" * 60)
    print("FastAPI server initialized")
    print("All services initialized")
    
    # Check API keys
    keys = {
        "OpenRouter (Llama Vision + Chatbot)": os.getenv("OPENROUTER_API_KEY"),
        "OpenAI (Reports)": os.getenv("OPENAI_API_KEY"),
        "OpenWeather (Location)": os.getenv("OPENWEATHER_API_KEY")
    }
    
    for service, key in keys.items():
        status = "OK" if key else "MISSING"
        print(f"{service}: {status}")
    
    print("=" * 60)
    print("Visit http://localhost:8000/docs")
    print("=" * 60)
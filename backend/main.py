from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Import our custom modules
from utils.image_processor import ImageProcessor
from utils.ai_client import AIClient
from utils.carbon_calculator import CarbonCalculator
from utils.report_generator import ReportGenerator
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

# Initialize AI client, calculator, and report generator
ai_client = AIClient()
carbon_calculator = CarbonCalculator()
report_generator = ReportGenerator()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Carbon Credit Analyzer API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Upload and analyze farmland image",
            "POST /analyze-with-report": "Complete pipeline: Analyze + Generate report",
            "POST /generate-report": "Generate report from existing analysis",
            "POST /generate-summary": "Generate executive summary",
            "POST /generate-text-summary": "Generate simple text summary",
            "GET /health": "Check API health and configuration",
            "GET /test-ai": "Test AI connection",
            "GET /test-openai": "Test OpenAI connection",
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

# Main image analysis endpoint - COMPLETE PIPELINE
@app.post("/analyze", response_model=dict)
async def analyze_land(
    file: UploadFile = File(..., description="Image of farmland/agricultural area")
):
    """
    Upload an image of farmland for complete carbon credit potential analysis
    
    Pipeline:
    1. Image Processing (resize, optimize, validate)
    2. AI Vision Analysis (Llama 3.2 Vision)
    3. Carbon Calculations (sequestration, credits, revenue)
    4. Recommendations & Next Steps
    
    Accepts: JPEG, PNG, WebP (max 10MB)
    Returns: Vision analysis + Carbon credit estimates + Recommendations
    """
    
    try:
        # Generate unique ID for this analysis
        analysis_id = str(uuid.uuid4())
        
        # Step 1: Process the image
        print(f"\n{'='*60}")
        print(f"[{analysis_id}] NEW ANALYSIS STARTED")
        print(f"{'='*60}")
        print(f"[{analysis_id}] Processing image: {file.filename}")
        base64_image, metadata = await ImageProcessor.process_image(file)
        image_quality = ImageProcessor.estimate_image_quality(metadata)
        
        print(f"[{analysis_id}] ✅ Image processed: {metadata['processed_dimensions']}")
        
        # Step 2: Analyze with Llama Vision
        print(f"[{analysis_id}] 🤖 Analyzing with Llama Vision AI...")
        vision_result = await ai_client.analyze_image_with_llama_vision(
            base64_image, 
            metadata
        )
        
        # Add image quality to vision result
        vision_result["image_quality"] = image_quality
        
        print(f"[{analysis_id}] ✅ Vision analysis complete")
        print(f"[{analysis_id}]    └─ Type: {vision_result['vegetation_type']}")
        print(f"[{analysis_id}]    └─ Density: {vision_result['density_percentage']}%")
        print(f"[{analysis_id}]    └─ Condition: {vision_result['land_condition']}")
        
        # Step 3: Calculate carbon potential
        print(f"[{analysis_id}] 💰 Calculating carbon credit potential...")
        carbon_analysis = carbon_calculator.calculate_complete_analysis(
            vision_result,
            metadata
        )
        
        carbon_est = carbon_analysis["carbon_estimate"]
        print(f"[{analysis_id}] ✅ Carbon calculations complete")
        print(f"[{analysis_id}]    └─ Annual CO2: {carbon_est['annual_sequestration_tons']} tons")
        print(f"[{analysis_id}]    └─ Est. Credits: {carbon_est['potential_annual_credits']}")
        print(f"[{analysis_id}]    └─ Revenue (mid): ₹{carbon_est['potential_revenue_inr']['1_year']['mid']:,.0f}/year")
        print(f"{'='*60}\n")
        
        # Step 4: Return comprehensive result
        return {
            "analysis_id": analysis_id,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "image_metadata": metadata,
            "vision_analysis": vision_result,
            "carbon_analysis": carbon_analysis,
            "summary": {
                "vegetation_type": vision_result["vegetation_type"],
                "land_condition": vision_result["land_condition"],
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
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
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

# Test OpenAI connection
@app.get("/test-openai")
async def test_openai_connection():
    """Test if OpenAI API is working"""
    try:
        result = await report_generator.test_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate report from existing analysis
@app.post("/generate-report")
async def generate_report(analysis_data: dict):
    """
    Generate professional report from analysis data
    
    Input: Complete analysis JSON from /analyze endpoint
    Output: Professional markdown report
    """
    try:
        print(f"\n🔄 Generating report with GPT-4o...")
        
        report = await report_generator.generate_full_report(analysis_data)
        
        print(f"✅ Report generated successfully ({len(report)} characters)")
        
        return {
            "status": "success",
            "report_markdown": report,
            "report_length": len(report),
            "message": "Report generated successfully"
        }
    except Exception as e:
        print(f"❌ Report generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

# Generate executive summary only
@app.post("/generate-summary")
async def generate_summary(analysis_data: dict):
    """
    Generate brief executive summary from analysis data
    
    Input: Complete analysis JSON from /analyze endpoint
    Output: 2-3 paragraph summary
    """
    try:
        print(f"\n🔄 Generating executive summary...")
        
        summary = await report_generator.generate_executive_summary(analysis_data)
        
        print(f"✅ Summary generated")
        
        return {
            "status": "success",
            "executive_summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")

# Generate simple text summary (for WhatsApp/SMS)
@app.post("/generate-text-summary")
async def generate_text_summary(analysis_data: dict):
    """
    Generate simple text summary for sharing via WhatsApp/SMS
    
    Input: Complete analysis JSON from /analyze endpoint
    Output: Plain text summary
    """
    try:
        summary = await report_generator.generate_simple_text_summary(analysis_data)
        
        return {
            "status": "success",
            "text_summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# COMPLETE PIPELINE: Analyze + Generate Report
@app.post("/analyze-with-report")
async def analyze_with_report(
    file: UploadFile = File(..., description="Image of farmland/agricultural area")
):
    """
    Complete pipeline: Upload image → Analyze → Generate report
    
    Returns: Analysis + Professional report in one call
    """
    try:
        # Step 1-3: Standard analysis (same as /analyze endpoint)
        analysis_id = str(uuid.uuid4())
        
        print(f"\n{'='*60}")
        print(f"[{analysis_id}] COMPLETE ANALYSIS + REPORT PIPELINE")
        print(f"{'='*60}")
        
        # Image processing
        base64_image, metadata = await ImageProcessor.process_image(file)
        image_quality = ImageProcessor.estimate_image_quality(metadata)
        
        # Vision analysis
        print(f"[{analysis_id}] 🤖 Running AI vision analysis...")
        vision_result = await ai_client.analyze_image_with_llama_vision(base64_image, metadata)
        vision_result["image_quality"] = image_quality
        
        # Carbon calculations
        print(f"[{analysis_id}] 💰 Calculating carbon potential...")
        carbon_analysis = carbon_calculator.calculate_complete_analysis(vision_result, metadata)
        
        # Compile analysis data
        analysis_data = {
            "analysis_id": analysis_id,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "image_metadata": metadata,
            "vision_analysis": vision_result,
            "carbon_analysis": carbon_analysis
        }
        
        # Step 4: Generate report
        print(f"[{analysis_id}] 📄 Generating professional report...")
        full_report = await report_generator.generate_full_report(analysis_data)
        exec_summary = await report_generator.generate_executive_summary(analysis_data)
        text_summary = await report_generator.generate_simple_text_summary(analysis_data)
        
        carbon_est = carbon_analysis["carbon_estimate"]
        print(f"[{analysis_id}] ✅ COMPLETE!")
        print(f"[{analysis_id}]    └─ Revenue (mid): ₹{carbon_est['potential_revenue_inr']['1_year']['mid']:,.0f}/year")
        print(f"[{analysis_id}]    └─ Report: {len(full_report)} chars")
        print(f"{'='*60}\n")
        
        return {
            "analysis_id": analysis_id,
            "status": "success",
            "timestamp": analysis_data["timestamp"],
            "analysis": analysis_data,
            "reports": {
                "full_report_markdown": full_report,
                "executive_summary": exec_summary,
                "text_summary": text_summary
            },
            "summary": {
                "vegetation_type": vision_result["vegetation_type"],
                "land_condition": vision_result["land_condition"],
                "estimated_annual_revenue_inr": {
                    "conservative": carbon_est['potential_revenue_inr']['1_year']['min'],
                    "mid_range": carbon_est['potential_revenue_inr']['1_year']['mid'],
                    "optimistic": carbon_est['potential_revenue_inr']['1_year']['max']
                },
                "confidence": carbon_est['confidence_level']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")

# Startup event
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🌱 Carbon Credit Analyzer API Starting...")
    print("=" * 60)
    print(f"✅ FastAPI server initialized")
    print(f"✅ CORS enabled for all origins")
    print(f"✅ Carbon Calculator initialized")
    print(f"✅ Report Generator initialized")
    
    # Check API keys
    if os.getenv("OPENROUTER_API_KEY"):
        print(f"✅ OpenRouter API key loaded")
    else:
        print(f"⚠️  OpenRouter API key missing!")
    
    if os.getenv("OPENAI_API_KEY"):
        print(f"✅ OpenAI API key loaded")
    else:
        print(f"⚠️  OpenAI API key missing!")
    
    print("=" * 60)
    print("📚 Visit http://localhost:8000/docs for API documentation")
    print("🚀 Ready to analyze farmland and generate reports!")
    print("=" * 60)
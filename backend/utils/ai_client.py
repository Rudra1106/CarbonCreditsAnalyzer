import httpx
import os
import json
import re
from typing import Dict, Any

class AIClient:
    """Handles communication with AI models via OpenRouter"""
    
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    def _repair_json(self, content: str) -> str:
        """
        Repair common JSON issues in AI responses
        """
        # Remove trailing commas before closing brackets/braces
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Fix missing values - replace ", ," or ": ," with appropriate defaults
        content = re.sub(r':\s*,', ': null,', content)
        content = re.sub(r':\s*\n', ': null\n', content)
        
        # Fix trailing commas at end of objects
        content = re.sub(r',(\s*})', r'\1', content)
        
        return content
    
    def _extract_json_from_response(self, content: str) -> dict:
        """
        Extract and parse JSON from AI response, handling various formats
        """
        # Try to repair common JSON issues first
        repaired_content = self._repair_json(content)
        
        # Try direct JSON parse
        try:
            return json.loads(repaired_content)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        match = re.search(json_pattern, content, re.DOTALL)
        if match:
            try:
                repaired = self._repair_json(match.group(1))
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass
        
        # Try to find any JSON object in the text
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        match = re.search(json_pattern, content, re.DOTALL)
        if match:
            try:
                repaired = self._repair_json(match.group(0))
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass
        
        raise json.JSONDecodeError(f"Could not extract valid JSON from response", content, 0)
    
    def _validate_and_fix_analysis(self, analysis: dict) -> dict:
        """
        Validate the analysis response and provide defaults for missing fields
        """
        # Define valid enum values
        valid_veg_types = ["forest", "cropland", "grassland", "mixed", "barren", "unknown"]
        valid_densities = ["sparse", "moderate", "dense", "none"]
        valid_conditions = ["excellent", "good", "average", "degraded", "poor"]
        valid_confidence = ["high", "medium", "low"]
        
        # Ensure required fields with defaults
        result = {
            "vegetation_type": analysis.get("vegetation_type", "unknown"),
            "vegetation_density": analysis.get("vegetation_density", "moderate"),
            "density_percentage": analysis.get("density_percentage", 50.0),
            "estimated_tree_count": analysis.get("estimated_tree_count"),
            "land_condition": analysis.get("land_condition", "average"),
            "visible_features": analysis.get("visible_features", []),
            "confidence": analysis.get("confidence", "medium"),
            "reasoning": analysis.get("reasoning", "Analysis based on visible features")
        }
        
        # Handle null or invalid density_percentage
        if result["density_percentage"] is None:
            # Estimate based on density type
            density_map = {"sparse": 20.0, "moderate": 50.0, "dense": 80.0, "none": 0.0}
            result["density_percentage"] = density_map.get(result["vegetation_density"], 50.0)
        
        # Convert to float if needed
        try:
            result["density_percentage"] = float(result["density_percentage"])
        except (ValueError, TypeError):
            result["density_percentage"] = 50.0
        
        # Validate enum values
        if result["vegetation_type"] not in valid_veg_types:
            result["vegetation_type"] = "unknown"
        
        if result["vegetation_density"] not in valid_densities:
            result["vegetation_density"] = "moderate"
        
        if result["land_condition"] not in valid_conditions:
            result["land_condition"] = "average"
        
        if result["confidence"] not in valid_confidence:
            result["confidence"] = "medium"
        
        # Clamp density percentage
        result["density_percentage"] = max(0.0, min(100.0, result["density_percentage"]))
        
        # Ensure visible_features is a list
        if not isinstance(result["visible_features"], list):
            result["visible_features"] = []
        
        # Handle estimated_tree_count
        if result["estimated_tree_count"] is not None:
            try:
                result["estimated_tree_count"] = int(result["estimated_tree_count"])
            except (ValueError, TypeError):
                result["estimated_tree_count"] = None
        
        return result
    
    async def analyze_image_with_llama_vision(self, base64_image: str, image_metadata: dict) -> Dict[str, Any]:
        """
        Analyze farmland image using Llama 3.2 Vision
        
        Args:
            base64_image: Base64 encoded image string
            image_metadata: Metadata about the image
            
        Returns:
            Structured analysis dict
        """
        
        # More explicit prompt with examples
        system_prompt = """You are an expert agricultural analyst specializing in carbon sequestration and farmland assessment.

Your task: Analyze farmland images to help farmers understand their land's carbon credit potential.

CRITICAL: You MUST respond with ONLY a valid JSON object. No explanations before or after. Just the JSON.

Required JSON structure with examples:

Example 1 (Forest):
{
  "vegetation_type": "forest",
  "vegetation_density": "dense",
  "density_percentage": 85,
  "estimated_tree_count": 150,
  "land_condition": "good",
  "visible_features": ["mature trees", "healthy canopy", "natural undergrowth"],
  "confidence": "high",
  "reasoning": "Dense forest with mature trees showing strong carbon sequestration potential"
}

Example 2 (Cropland):
{
  "vegetation_type": "cropland",
  "vegetation_density": "moderate",
  "density_percentage": 60,
  "estimated_tree_count": null,
  "land_condition": "average",
  "visible_features": ["crop rows", "tilled soil", "irrigation system"],
  "confidence": "medium",
  "reasoning": "Active cropland with moderate vegetation cover"
}

Field requirements:
- vegetation_type: must be one of: "forest", "cropland", "grassland", "mixed", "barren", "unknown"
- vegetation_density: must be one of: "sparse", "moderate", "dense", "none"
- density_percentage: number from 0 to 100 (REQUIRED - never leave empty)
- estimated_tree_count: number or null (use null if no trees visible)
- land_condition: must be one of: "excellent", "good", "average", "degraded", "poor"
- visible_features: array of strings describing what you see
- confidence: must be one of: "high", "medium", "low"
- reasoning: brief explanation of your assessment

IMPORTANT: 
- ALWAYS provide a number for density_percentage (never leave it empty)
- Use null for estimated_tree_count if there are no trees
- Respond with ONLY the JSON object"""

        user_prompt = """Analyze this farmland image for carbon credit potential.

Provide detailed assessment focusing on:
1. What type of vegetation do you see? (trees, crops, grass, mixed)
2. How dense is the vegetation? Estimate coverage percentage
3. If trees are visible, approximately how many?
4. What is the overall condition of the land?
5. What specific features do you notice?

Remember: Respond with ONLY the JSON object, no other text."""

        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://carbon-credit-analyzer.local",
            "X-Title": "Carbon Credit Analyzer"
        }
        
        payload = {
            "model": "meta-llama/llama-3.2-11b-vision-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,  # Very low for consistency
            "max_tokens": 2000,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        # Make the API call
        async with httpx.AsyncClient(timeout=90.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract the content
                content = result["choices"][0]["message"]["content"].strip()
                
                # DEBUG: Print what we received
                print("=" * 50)
                print("RAW AI RESPONSE:")
                print(content)
                print("=" * 50)
                
                # Parse JSON with repair and fallback handling
                try:
                    analysis = self._extract_json_from_response(content)
                    print("✅ JSON parsed successfully")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing failed: {str(e)}")
                    print("🔧 Using fallback default response")
                    # Return a safe default response
                    analysis = {
                        "vegetation_type": "unknown",
                        "vegetation_density": "moderate",
                        "density_percentage": 50.0,
                        "estimated_tree_count": None,
                        "land_condition": "average",
                        "visible_features": ["Image analyzed but detailed parsing unavailable"],
                        "confidence": "low",
                        "reasoning": "AI response could not be parsed properly. Manual review recommended."
                    }
                
                # Validate and fix the analysis
                analysis = self._validate_and_fix_analysis(analysis)
                
                print(f"📊 Final Analysis: {analysis['vegetation_type']} - {analysis['vegetation_density']} ({analysis['density_percentage']}%)")
                
                # Add cost tracking
                usage = result.get("usage", {})
                analysis["api_usage"] = {
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                }
                
                return analysis
                
            except httpx.HTTPStatusError as e:
                error_detail = {}
                try:
                    error_detail = e.response.json()
                except:
                    error_detail = {"error": str(e)}
                raise Exception(f"OpenRouter API error: {error_detail}")
            except Exception as e:
                raise Exception(f"AI analysis failed: {str(e)}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test if OpenRouter API is accessible"""
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json={
                        "model": "meta-llama/llama-3.2-90b-vision-instruct",
                        "messages": [
                            {"role": "user", "content": "Say 'API connection successful'"}
                        ],
                        "max_tokens": 20
                    }
                )
                response.raise_for_status()
                return {"status": "success", "message": "OpenRouter API connected"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
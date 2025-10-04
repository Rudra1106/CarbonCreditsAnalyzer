import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
from serpapi import GoogleSearch

class ChatbotService:
    """
    Enhanced AI Chatbot using Mistral 8x7B via OpenRouter
    Features:
    - Full report context
    - Web search capability (SerpApi)
    - Cost-effective via OpenRouter credits
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found")
        
        # Initialize OpenAI client with OpenRouter base URL
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
        self.model = "mistralai/mixtral-8x7b-instruct"
    
    def _extract_full_report_context(self, user_analysis: Optional[Dict]) -> str:
        """Extract complete information from user's analysis including reports"""
        
        if not user_analysis:
            return ""
        
        # Vision analysis
        vision = user_analysis.get('vision_analysis', {})
        
        # Carbon analysis
        carbon = user_analysis.get('carbon_analysis', {}).get('carbon_estimate', {})
        calc_details = carbon.get('calculation_details', {})
        
        # Location data
        location = user_analysis.get('location_data', {})
        location_info = location.get('location', {})
        weather = location.get('weather_data', {})
        
        # Reports
        reports = user_analysis.get('reports', {})
        exec_summary = reports.get('executive_summary', '')
        
        # Recommendations and next steps
        carbon_analysis = user_analysis.get('carbon_analysis', {})
        recommendations = carbon_analysis.get('recommendations', [])
        next_steps = carbon_analysis.get('next_steps', [])
        
        context = f"""
USER'S COMPLETE LAND ANALYSIS:

Location Information:
- City: {location_info.get('city', 'N/A')}
- State: {location_info.get('state', 'N/A')}
- Climate Zone: {location_info.get('climate_zone', 'N/A')}
- Current Temperature: {weather.get('temperature', 'N/A')}°C
- Humidity: {weather.get('humidity', 'N/A')}%
- Climate Multiplier: {location.get('climate_multiplier', 1.0)}x

Land Characteristics:
- Vegetation Type: {vision.get('vegetation_type', 'N/A')}
- Vegetation Density: {vision.get('vegetation_density', 'N/A')} ({vision.get('density_percentage', 0)}% coverage)
- Land Condition: {vision.get('land_condition', 'N/A')}
- Estimated Tree Count: {vision.get('estimated_tree_count', 'N/A')}
- Visible Features: {', '.join(vision.get('visible_features', []))}
- Image Quality: {vision.get('image_quality', 'N/A')}
- Analysis Confidence: {vision.get('confidence', 'N/A')}

Carbon Sequestration Calculations:
- Estimated Land Area: {carbon.get('estimated_land_area_hectares', 0)} hectares
- Annual CO2 Sequestration: {carbon.get('annual_sequestration_tons', 0)} tons/year
- Annual Carbon Credits: {carbon.get('potential_annual_credits', 0)} credits/year

Calculation Methodology:
- Base Rate: {calc_details.get('base_rate', 0)} tons/hectare/year
- Density Multiplier: {calc_details.get('density_multiplier', 1.0)}x
- Condition Multiplier: {calc_details.get('condition_multiplier', 1.0)}x
- Density % Multiplier: {calc_details.get('density_percentage_multiplier', 1.0)}x
- Climate Multiplier: {calc_details.get('climate_multiplier', 1.0)}x
- Effective Rate: {calc_details.get('effective_rate_per_hectare', 0)} tons/hectare/year

Revenue Projections (INR):
1 Year:
  - Conservative: ₹{carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('min', 0):,.0f}
  - Mid-Range: ₹{carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('mid', 0):,.0f}
  - Optimistic: ₹{carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('max', 0):,.0f}

5 Year:
  - Conservative: ₹{carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('min', 0):,.0f}
  - Mid-Range: ₹{carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('mid', 0):,.0f}
  - Optimistic: ₹{carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('max', 0):,.0f}

10 Year:
  - Conservative: ₹{carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('min', 0):,.0f}
  - Mid-Range: ₹{carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('mid', 0):,.0f}
  - Optimistic: ₹{carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('max', 0):,.0f}

Confidence Level: {carbon.get('confidence_level', 'N/A')}

Expert Recommendations:
{chr(10).join('- ' + rec for rec in recommendations)}

Next Steps:
{chr(10).join(next_steps)}

Executive Summary:
{exec_summary}

Use this complete context to answer user's questions accurately and specifically about their land."""

        return context
    
    async def _web_search(self, query: str) -> str:
        """Perform web search using SerpApi"""
        
        if not self.serpapi_key:
            return "Web search unavailable (API key not configured)"
        
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.serpapi_key,
                "num": 3,
                "gl": "in",  # India
                "hl": "en"
            })
            
            results = search.get_dict()
            
            if "organic_results" not in results:
                return "No search results found"
            
            # Extract top 3 results
            search_summary = []
            for idx, result in enumerate(results["organic_results"][:3], 1):
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                link = result.get("link", "")
                search_summary.append(f"{idx}. {title}\n   {snippet}\n   Source: {link}")
            
            return "\n\n".join(search_summary)
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _create_system_prompt(self, user_analysis: Optional[Dict] = None) -> str:
        """Create enhanced system prompt with full context"""
        
        base_knowledge = """You are a helpful carbon credit expert assistant for Indian farmers.

CORE KNOWLEDGE:
- Carbon credits: 1 credit = 1 ton CO2 sequestered
- Indian programs: CAMPA (Compensatory Afforestation Fund Management and Planning Authority), State Forest Departments, Verra, Gold Standard
- Current prices: ₹1,245-4,150 per credit (₹15-50 USD at ₹83/USD exchange rate)
- Eligibility requirements: Professional land survey and soil testing required
- Typical commitments: 20-30 years for most carbon credit programs
- Verification costs in India: ₹4-17 lakhs (includes land survey, soil testing, baseline assessment, monitoring setup)
- Sequestration rates hierarchy: forest > agroforestry > cropland > grassland
- Key factors affecting sequestration: vegetation type, density, land condition, climate zone

YOUR CAPABILITIES:
1. Answer questions using the user's complete analysis report with specific numbers
2. Explain calculations, methodologies, multipliers, and all recommendations in detail
3. Search the web for current information when user asks about latest data
4. Provide personalized advice based on their specific land characteristics and location

RESPONSE GUIDELINES:
- Be conversational, helpful, and informative
- Always reference specific numbers from their analysis when relevant
- Explain technical terms in simple language suitable for farmers
- Be honest about uncertainties and limitations
- Encourage professional verification for final decisions
- Keep responses concise (2-5 sentences) unless user asks for detailed explanation
- Use INR (₹) for all monetary values

IMPORTANT: When user asks about their specific analysis, always use their exact data from the context provided."""

        # Add user's complete analysis
        if user_analysis:
            context = self._extract_full_report_context(user_analysis)
            return base_knowledge + "\n\n" + context
        
        return base_knowledge
    
    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        user_analysis: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Enhanced chat with web search capability using Mistral 8x7B
        """
        
        # Check if we need web search
        search_results = None
        needs_search = any([
            "latest" in user_message.lower(),
            "current" in user_message.lower(),
            "recent" in user_message.lower(),
            "2025" in user_message,
            "today" in user_message.lower(),
            "news" in user_message.lower(),
            "update" in user_message.lower()
        ])
        
        # Build conversation
        messages = [
            {"role": "system", "content": self._create_system_prompt(user_analysis)}
        ]
        
        # Add conversation history (last 10 messages for context management)
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        # Perform search if needed
        if needs_search and self.serpapi_key:
            print(f"[CHAT] Performing web search for: {user_message}")
            search_query = user_message + " carbon credits India"
            search_results = await self._web_search(search_query)
            
            # Add search results to context
            messages.append({
                "role": "system",
                "content": f"Current Web Search Results:\n{search_results}\n\nUse this up-to-date information to answer the user's question along with your base knowledge."
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=600,
                top_p=0.9,
                extra_headers={
                    "HTTP-Referer": "https://carbon-credit-analyzer.local",
                    "X-Title": "Carbon Credit Analyzer"
                }
            )
            
            assistant_message = response.choices[0].message.content
            
            return {
                "status": "success",
                "response": assistant_message,
                "tokens": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": self.model,
                "search_performed": needs_search and bool(search_results)
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"[CHAT] Error: {error_msg}")
            
            return {
                "status": "error",
                "response": "I'm having trouble connecting right now. Please try again.",
                "error": error_msg
            }
    
    async def get_suggested_questions(self, user_analysis: Optional[Dict] = None) -> List[str]:
        """Generate contextual suggested questions"""
        
        general_questions = [
            "What are carbon credits and how do they work?",
            "How do I get started with carbon credit programs in India?",
            "What's the difference between Verra and CAMPA?",
            "What are the latest carbon credit prices in India?",
            "How long does the verification process typically take?"
        ]
        
        if not user_analysis:
            return general_questions
        
        # Personalized questions based on complete analysis
        vision = user_analysis.get('vision_analysis', {})
        carbon = user_analysis.get('carbon_analysis', {}).get('carbon_estimate', {})
        confidence = carbon.get('confidence_level', 'medium')
        veg_type = vision.get('vegetation_type', 'unknown')
        location = user_analysis.get('location_data', {}).get('location', {})
        state = location.get('state', '')
        
        personalized = []
        
        # Confidence-based questions
        if confidence == 'high':
            personalized.append("My confidence is high - what should I do next?")
        else:
            personalized.append(f"Why is my confidence level {confidence}?")
        
        # Vegetation-based questions
        if veg_type == 'forest':
            personalized.append("How can I maximize revenue from my forest land?")
            personalized.append("What are the best forest carbon programs in India?")
        elif veg_type == 'cropland':
            personalized.append("What carbon credit options exist for cropland?")
            personalized.append("Can regenerative agriculture increase my credits?")
        elif veg_type == 'mixed':
            personalized.append("Is mixed vegetation beneficial for carbon credits?")
        
        # Location-based questions
        if state:
            personalized.append(f"Are there specific carbon programs for {state}?")
        
        # Calculation-based questions
        personalized.append("Explain how my revenue was calculated step by step")
        personalized.append("What factors could increase my carbon credit value?")
        
        return personalized[:5]
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Mistral connection via OpenRouter"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Say 'Chatbot connected successfully'"}
                ],
                max_tokens=20
            )
            return {
                "status": "success",
                "message": response.choices[0].message.content,
                "model": self.model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
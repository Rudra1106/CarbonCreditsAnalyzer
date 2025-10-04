import os
from openai import AsyncOpenAI
from typing import Dict, Any
from datetime import datetime

class ReportGenerator:
    """
    Generate professional carbon credit analysis reports using GPT-4o
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o"
    
    def _format_currency(self, amount: float) -> str:
        """Format INR currency with Indian numbering system"""
        if amount >= 10000000:  # 1 crore+
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 lakh+
            return f"₹{amount/100000:.2f} L"
        else:
            return f"₹{amount:,.0f}"
    
    def _prepare_analysis_context(self, analysis_data: Dict[str, Any]) -> str:
        """
        Prepare structured context for GPT-4o
        """
        
        vision = analysis_data.get("vision_analysis", {})
        carbon = analysis_data.get("carbon_analysis", {}).get("carbon_estimate", {})
        
        context = f"""
# Carbon Credit Analysis Data

## Land Analysis
- Vegetation Type: {vision.get('vegetation_type', 'unknown')}
- Vegetation Density: {vision.get('vegetation_density', 'unknown')} ({vision.get('density_percentage', 0)}% coverage)
- Land Condition: {vision.get('land_condition', 'unknown')}
- Estimated Tree Count: {vision.get('estimated_tree_count') or 'Not applicable'}
- Visible Features: {', '.join(vision.get('visible_features', []))}
- Analysis Confidence: {vision.get('confidence', 'medium')}

## Carbon Sequestration Potential
- Estimated Land Area: {carbon.get('estimated_land_area_hectares', 0)} hectares
- Annual CO2 Sequestration: {carbon.get('annual_sequestration_tons', 0)} tons/year
- Annual Carbon Credits: {carbon.get('potential_annual_credits', 0)} credits/year

## Revenue Projections (INR)
### 1 Year
- Conservative: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('min', 0))}
- Mid-Range: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('mid', 0))}
- Optimistic: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('1_year', {}).get('max', 0))}

### 5 Year Projection
- Conservative: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('min', 0))}
- Mid-Range: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('mid', 0))}
- Optimistic: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('5_year', {}).get('max', 0))}

### 10 Year Projection
- Conservative: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('min', 0))}
- Mid-Range: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('mid', 0))}
- Optimistic: {self._format_currency(carbon.get('potential_revenue_inr', {}).get('10_year', {}).get('max', 0))}

## Calculation Details
- Base Sequestration Rate: {carbon.get('calculation_details', {}).get('base_rate', 0)} tons/hectare/year
- Density Multiplier: {carbon.get('calculation_details', {}).get('density_multiplier', 1.0)}x
- Condition Multiplier: {carbon.get('calculation_details', {}).get('condition_multiplier', 1.0)}x
- Effective Rate: {carbon.get('calculation_details', {}).get('effective_rate_per_hectare', 0)} tons/hectare/year

## Confidence Level
{carbon.get('confidence_level', 'medium').upper()}

## Recommendations
{chr(10).join('- ' + rec for rec in analysis_data.get('carbon_analysis', {}).get('recommendations', []))}

## Next Steps
{chr(10).join(analysis_data.get('carbon_analysis', {}).get('next_steps', []))}
"""
        return context
    
    async def generate_executive_summary(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate a brief executive summary (2-3 paragraphs)
        """
        
        context = self._prepare_analysis_context(analysis_data)
        
        system_prompt = """You are an expert carbon credit consultant writing executive summaries for farmers in India.

Your task: Write a clear, concise executive summary (2-3 paragraphs) that:
1. Summarizes the land's carbon sequestration potential
2. Highlights the key revenue opportunity
3. Mentions important considerations

Tone: Professional but accessible, encouraging but realistic.
Language: Clear English suitable for Indian farmers.
Length: 150-200 words maximum."""

        user_prompt = f"""Based on this carbon credit analysis, write an executive summary:

{context}

Write a compelling but honest summary that helps the farmer understand their land's potential."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Executive summary generation failed: {str(e)}"
    
    async def generate_full_report(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate complete professional report in Markdown format
        """
        
        context = self._prepare_analysis_context(analysis_data)
        analysis_id = analysis_data.get("analysis_id", "N/A")
        timestamp = analysis_data.get("timestamp", datetime.now().isoformat())
        
        system_prompt = """You are an expert carbon credit consultant creating detailed analysis reports for Indian farmers.

Your task: Write a comprehensive, professional report that:
1. Clearly explains the analysis results
2. Provides context about carbon credits in India
3. Offers actionable recommendations
4. Maintains realistic expectations
5. Encourages professional verification

Format: Use Markdown with clear sections, headers, bullet points, and tables where appropriate.
Tone: Professional, encouraging, educational, realistic.
Style: Clear, jargon-free language suitable for farmers.
Length: Comprehensive but focused (800-1200 words)."""

        user_prompt = f"""Create a detailed carbon credit analysis report based on this data:

{context}

Structure the report with these sections:
1. Executive Summary
2. Land Analysis Results
3. Carbon Sequestration Potential
4. Revenue Projections & Economic Analysis
5. Methodology & Confidence Level
6. Recommendations for Maximizing Carbon Credits
7. Next Steps & Implementation Guide
8. Important Disclaimers

Make it professional, informative, and actionable. Use tables for financial projections."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            report_content = response.choices[0].message.content.strip()
            
            # Add header with metadata
            header = f"""---
# Carbon Credit Analysis Report
**Analysis ID:** {analysis_id}  
**Generated:** {datetime.fromisoformat(timestamp).strftime('%B %d, %Y at %I:%M %p')}  
**Powered by:** Carbon Credit Analyzer AI

---

"""
            
            return header + report_content
            
        except Exception as e:
            return f"# Report Generation Failed\n\nError: {str(e)}"
    
    async def generate_simple_text_summary(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate a simple text summary (for quick sharing via WhatsApp/SMS)
        """
        
        vision = analysis_data.get("vision_analysis", {})
        carbon = analysis_data.get("carbon_analysis", {}).get("carbon_estimate", {})
        revenue = carbon.get('potential_revenue_inr', {}).get('1_year', {})
        
        summary = f"""🌱 Carbon Credit Analysis Summary

📊 Your Land:
• Type: {vision.get('vegetation_type', 'N/A').title()}
• Condition: {vision.get('land_condition', 'N/A').title()}
• Vegetation Density: {vision.get('density_percentage', 0)}%
• Estimated Area: {carbon.get('estimated_land_area_hectares', 0)} hectares

💰 Annual Revenue Potential:
• Conservative: {self._format_currency(revenue.get('min', 0))}
• Mid-Range: {self._format_currency(revenue.get('mid', 0))}
• Optimistic: {self._format_currency(revenue.get('max', 0))}

🌍 Carbon Impact:
• {carbon.get('annual_sequestration_tons', 0)} tons CO2 captured/year
- Equivalent to taking ~{max(1, int(carbon.get('annual_sequestration_tons', 0) / 4.6))} car(s) off the road!

⚠️ Important: This is a preliminary estimate. Professional land survey required for carbon credit enrollment.

📞 Next Step: Contact verified carbon programs for official assessment."""

        return summary
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Say 'OpenAI API connected successfully'"}
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
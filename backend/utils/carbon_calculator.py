from typing import Dict, Any, Tuple
from models.schemas import VisionAnalysis, CarbonEstimate, ConfidenceLevel

class CarbonCalculator:
    """
    Calculate carbon sequestration potential and credit estimates
    based on vision analysis of farmland
    """
    
    # Base sequestration rates (tons CO2/hectare/year)
    BASE_SEQUESTRATION_RATES = {
        "forest": 10.0,      # Dense forest baseline
        "cropland": 2.0,     # Regenerative agriculture
        "grassland": 3.5,    # Managed pasture
        "mixed": 6.0,        # Agroforestry
        "barren": 0.1,       # Minimal
        "unknown": 2.5       # Conservative estimate
    }
    
    # Density multipliers
    DENSITY_MULTIPLIERS = {
        "dense": 1.3,
        "moderate": 1.0,
        "sparse": 0.6,
        "none": 0.1
    }
    
    # Condition multipliers
    CONDITION_MULTIPLIERS = {
        "excellent": 1.2,
        "good": 1.1,
        "average": 1.0,
        "degraded": 0.7,
        "poor": 0.5
    }
    
    # Carbon credit market prices (INR per ton CO2)
    # International prices: $15-50 USD, converted at ₹83/USD (Oct 2025)
    CREDIT_PRICE_RANGE = {
        "min": 1245,   # Voluntary market, lower quality (~$15 USD)
        "mid": 2490,   # Average verified credits (~$30 USD)
        "max": 4150    # Premium verified credits (~$50 USD)
    }
    
    # Exchange rate for reference
    USD_TO_INR_RATE = 83.0
    
    def __init__(self):
        pass
    
    def estimate_land_area(self, image_metadata: dict, vision_analysis: dict) -> Tuple[float, str]:
        """
        Estimate visible land area from image
        
        This is a ROUGH estimation based on image dimensions and typical
        aerial photo patterns. Real measurements require GPS/surveying.
        
        Returns:
            (estimated_hectares, explanation)
        """
        
        # Parse image dimensions
        dimensions = image_metadata.get("processed_dimensions", "1920x1080")
        width, height = map(int, dimensions.split('x'))
        
        # Total pixels
        total_pixels = width * height
        
        # Estimation logic (very approximate):
        # - High res images of farmland are typically aerial/drone shots
        # - Average drone height: 50-100m captures ~1-2 hectares
        # - Ground-level photos: much less
        
        # Check for indicators of aerial vs ground-level
        features = vision_analysis.get("visible_features", [])
        features_str = " ".join(features).lower()
        
        # Heuristics
        is_likely_aerial = any([
            "rows" in features_str,
            "field" in features_str,
            vision_analysis.get("estimated_tree_count", 0) and vision_analysis["estimated_tree_count"] > 20,
            total_pixels > 1000000  # High resolution suggests aerial
        ])
        
        if is_likely_aerial:
            # Aerial photo estimate: 0.5 - 3 hectares visible
            base_area = 1.5
            explanation = "Estimated from aerial perspective indicators"
        else:
            # Ground level: 0.1 - 0.5 hectares visible
            base_area = 0.3
            explanation = "Estimated from ground-level perspective"
        
        # Adjust by image quality/resolution
        if total_pixels > 2000000:
            base_area *= 1.3  # High res = potentially larger area captured
        elif total_pixels < 500000:
            base_area *= 0.7  # Low res = smaller area or cropped
        
        return round(base_area, 2), explanation
    
    def calculate_sequestration(self, vision_analysis: dict, estimated_area: float) -> Dict[str, Any]:
        """
        Calculate annual CO2 sequestration based on vision analysis
        
        Args:
            vision_analysis: Dict with vegetation type, density, condition
            estimated_area: Estimated land area in hectares
            
        Returns:
            Dict with sequestration calculations
        """
        
        # Get base rate
        veg_type = vision_analysis.get("vegetation_type", "unknown")
        base_rate = self.BASE_SEQUESTRATION_RATES.get(veg_type, 2.5)
        
        # Apply multipliers
        density = vision_analysis.get("vegetation_density", "moderate")
        density_mult = self.DENSITY_MULTIPLIERS.get(density, 1.0)
        
        condition = vision_analysis.get("land_condition", "average")
        condition_mult = self.CONDITION_MULTIPLIERS.get(condition, 1.0)
        
        # Additional adjustment based on density percentage
        density_pct = vision_analysis.get("density_percentage", 50.0)
        density_pct_mult = 0.5 + (density_pct / 100.0)  # Scale from 0.5 to 1.5
        
        # Final calculation
        effective_rate = base_rate * density_mult * condition_mult * density_pct_mult
        annual_tons = effective_rate * estimated_area
        
        return {
            "base_rate": round(base_rate, 2),
            "density_multiplier": density_mult,
            "condition_multiplier": condition_mult,
            "density_percentage_multiplier": round(density_pct_mult, 2),
            "effective_rate_per_hectare": round(effective_rate, 2),
            "estimated_area_hectares": estimated_area,
            "annual_co2_tons": round(annual_tons, 2)
        }
    
    def calculate_credits_and_revenue(self, annual_tons: float) -> Dict[str, Any]:
        """
        Calculate potential carbon credits and revenue in INR
        
        Args:
            annual_tons: Annual CO2 sequestration in tons
            
        Returns:
            Dict with credit and revenue estimates in INR
        """
        
        # 1 ton CO2 = 1 carbon credit
        annual_credits = annual_tons
        
        # Revenue projections in INR (conservative, mid, optimistic)
        revenue_conservative = annual_credits * self.CREDIT_PRICE_RANGE["min"]
        revenue_mid = annual_credits * self.CREDIT_PRICE_RANGE["mid"]
        revenue_optimistic = annual_credits * self.CREDIT_PRICE_RANGE["max"]
        
        # 5-year and 10-year projections
        # Note: Real carbon projects typically have 20-30 year commitments
        projections = {
            "1_year": {
                "min": round(revenue_conservative, 2),
                "mid": round(revenue_mid, 2),
                "max": round(revenue_optimistic, 2)
            },
            "5_year": {
                "min": round(revenue_conservative * 5, 2),
                "mid": round(revenue_mid * 5, 2),
                "max": round(revenue_optimistic * 5, 2)
            },
            "10_year": {
                "min": round(revenue_conservative * 10, 2),
                "mid": round(revenue_mid * 10, 2),
                "max": round(revenue_optimistic * 10, 2)
            }
        }
        
        return {
            "annual_credits": round(annual_credits, 2),
            "credit_price_range_inr": self.CREDIT_PRICE_RANGE,
            "revenue_projections_inr": projections,
            "exchange_rate_reference": {
                "usd_to_inr": self.USD_TO_INR_RATE,
                "note": "International carbon credits priced in USD, converted to INR"
            }
        }
    
    def determine_confidence(self, vision_analysis: dict, image_quality: str) -> ConfidenceLevel:
        """
        Determine overall confidence level for the carbon estimate
        
        Factors:
        - Vision analysis confidence
        - Image quality
        - Data completeness
        """
        
        vision_confidence = vision_analysis.get("confidence", "medium")
        
        # Start with vision confidence as base
        confidence_score = {
            "high": 3,
            "medium": 2,
            "low": 1
        }.get(vision_confidence, 2)
        
        # Adjust for image quality
        if "excellent" in image_quality or "good" in image_quality:
            confidence_score += 0.5
        elif "poor" in image_quality:
            confidence_score -= 0.5
        
        # Adjust for data completeness
        if vision_analysis.get("estimated_tree_count") is not None:
            confidence_score += 0.25  # Tree count adds detail
        
        if len(vision_analysis.get("visible_features", [])) >= 3:
            confidence_score += 0.25  # Rich feature set
        
        # Convert score to level
        if confidence_score >= 3:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 2:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def generate_recommendations(self, vision_analysis: dict, carbon_estimate: dict) -> list:
        """Generate actionable recommendations based on analysis"""
        
        recommendations = []
        
        veg_type = vision_analysis.get("vegetation_type")
        condition = vision_analysis.get("land_condition")
        density = vision_analysis.get("vegetation_density")
        
        # Vegetation-specific recommendations
        if veg_type == "cropland":
            recommendations.append("Consider adopting regenerative agriculture practices (cover crops, no-till) to increase carbon sequestration")
            recommendations.append("Explore agroforestry - integrating trees can boost carbon credits significantly")
        
        elif veg_type == "grassland":
            recommendations.append("Implement rotational grazing to improve soil carbon storage")
            recommendations.append("Consider planting native perennial grasses for better carbon capture")
        
        elif veg_type == "forest":
            recommendations.append("Maintain forest health through sustainable management practices")
            recommendations.append("Forest carbon projects typically offer the highest credit values")
        
        # Condition-based recommendations
        if condition in ["degraded", "poor"]:
            recommendations.append("⚠️ Land restoration could significantly increase carbon potential")
            recommendations.append("Soil health improvement should be priority before enrolling in carbon programs")
        
        # Density-based recommendations
        if density == "sparse":
            recommendations.append("Increasing vegetation density through reforestation/replanting could 2-3x carbon potential")
        
        # General recommendations
        recommendations.append("Get a professional land survey for accurate area measurements")
        recommendations.append("Contact verified carbon credit programs: Verra, Gold Standard, or Indian programs like CAMPA")
        
        return recommendations
    
    def generate_next_steps(self) -> list:
        """Generate next steps for farmers"""
        
        return [
            "1. Get professional land survey and soil testing",
            "2. Research carbon credit programs in India (CAMPA, State Forest Departments)",
            "3. Understand program requirements (usually 20-30 year commitments)",
            "4. Consider consulting with carbon project developers",
            "5. Evaluate costs: verification, monitoring, administrative fees (₹4-17 lakhs)",
            "6. Compare multiple carbon programs for best fit"
        ]
    
    def calculate_complete_analysis(
        self, 
        vision_analysis: dict, 
        image_metadata: dict
    ) -> Dict[str, Any]:
        """
        Main method: Complete carbon analysis pipeline
        
        Args:
            vision_analysis: Output from Llama Vision
            image_metadata: Image processing metadata
            
        Returns:
            Complete carbon estimate with all calculations
        """
        
        # Step 1: Estimate land area
        estimated_area, area_explanation = self.estimate_land_area(
            image_metadata, 
            vision_analysis
        )
        
        # Step 2: Calculate sequestration
        sequestration = self.calculate_sequestration(
            vision_analysis,
            estimated_area
        )
        
        # Step 3: Calculate credits and revenue
        revenue_data = self.calculate_credits_and_revenue(
            sequestration["annual_co2_tons"]
        )
        
        # Step 4: Determine confidence
        image_quality = vision_analysis.get("image_quality", "good")
        confidence = self.determine_confidence(vision_analysis, image_quality)
        
        # Step 5: Generate recommendations
        recommendations = self.generate_recommendations(
            vision_analysis,
            sequestration
        )
        
        # Step 6: Next steps
        next_steps = self.generate_next_steps()
        
        # Compile complete result
        return {
            "carbon_estimate": {
                "annual_sequestration_tons": sequestration["annual_co2_tons"],
                "estimated_land_area_hectares": estimated_area,
                "area_estimation_method": area_explanation,
                "potential_annual_credits": revenue_data["annual_credits"],
                "potential_revenue_inr": revenue_data["revenue_projections_inr"],
                "confidence_level": confidence.value,
                "calculation_details": sequestration,
                "market_context": {
                    "credit_price_range_inr": revenue_data["credit_price_range_inr"],
                    "exchange_rate": revenue_data["exchange_rate_reference"],
                    "note": "Prices vary by program, verification level, and market conditions"
                }
            },
            "recommendations": recommendations,
            "next_steps": next_steps,
            "disclaimers": [
                "⚠️ This is a preliminary estimate based on single image analysis",
                "⚠️ Actual carbon credit eligibility requires professional land survey and soil testing",
                "⚠️ Revenue estimates are approximate and depend on market conditions",
                "⚠️ Most carbon programs require 20-30 year land commitments",
                "⚠️ Verification and monitoring costs typically range from ₹4-17 lakhs",
                "⚠️ Contact certified carbon credit programs for official assessment"
            ]
        }
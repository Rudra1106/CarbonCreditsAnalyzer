from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# Enums for controlled values
class VegetationType(str, Enum):
    FOREST = "forest"
    CROPLAND = "cropland"
    GRASSLAND = "grassland"
    MIXED = "mixed"
    BARREN = "barren"
    UNKNOWN = "unknown"

class VegetationDensity(str, Enum):
    SPARSE = "sparse"      # 0-30%
    MODERATE = "moderate"  # 30-60%
    DENSE = "dense"        # 60-100%
    NONE = "none"

class LandCondition(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    DEGRADED = "degraded"
    POOR = "poor"

class ConfidenceLevel(str, Enum):
    HIGH = "high"      # Clear image, typical land
    MEDIUM = "medium"  # Partial view or mixed features
    LOW = "low"        # Poor quality or unusual features

# Vision Analysis Response
class VisionAnalysis(BaseModel):
    vegetation_type: VegetationType
    vegetation_density: VegetationDensity
    density_percentage: float = Field(..., ge=0, le=100, description="Vegetation coverage 0-100%")
    estimated_tree_count: Optional[int] = Field(None, description="Visible tree count if applicable")
    land_condition: LandCondition
    visible_features: List[str] = Field(default_factory=list, description="Key features identified")
    image_quality: str = Field(..., description="Quality assessment of uploaded image")
    confidence: ConfidenceLevel

# Carbon Calculation Result
class CarbonEstimate(BaseModel):
    annual_sequestration_tons: float = Field(..., description="Estimated CO2 tons/year")
    estimated_land_area_hectares: float = Field(..., description="Estimated visible area")
    potential_annual_credits: float = Field(..., description="Estimated carbon credits per year")
    potential_annual_revenue_usd: dict = Field(..., description="Revenue range min/max")
    confidence_level: ConfidenceLevel
    calculation_method: str = Field(..., description="How this was calculated")

# Final Analysis Response
class AnalysisResponse(BaseModel):
    vision_analysis: VisionAnalysis
    carbon_estimate: CarbonEstimate
    recommendations: List[str]
    next_steps: List[str]
    disclaimers: List[str] = Field(
        default=[
            "This is a preliminary assessment based on image analysis only",
            "Actual carbon credit eligibility requires professional land survey",
            "Revenue estimates are approximate and depend on market conditions",
            "Contact certified carbon credit programs for official assessment"
        ]
    )

# Upload Response (immediate)
class UploadResponse(BaseModel):
    message: str
    image_id: str
    status: str
    estimated_processing_time: str = "10-15 seconds"
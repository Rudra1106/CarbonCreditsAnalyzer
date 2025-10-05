'use server';

import type { AnalysisResult } from '@/lib/types';

// This function maps the raw API response to the frontend's AnalysisResult type.
function mapApiToAnalysisResult(data: any): AnalysisResult {
  
  const carbonEstimate = data.carbon_analysis?.carbon_estimate || {};
  const visionAnalysis = data.vision_analysis || {};
  const locationData = data.location_data;
  const carbonAnalysis = data.carbon_analysis || {};
  const calculationDetails = carbonEstimate.calculation_details || {};
  const reports = data.reports || {};
  
  return {
    summary: {
      vegetation: {
        type: visionAnalysis.vegetation_type || 'N/A',
        description: visionAnalysis.reasoning || 'No description available.',
      },
      landArea: `${carbonEstimate.estimated_land_area_hectares || 'N/A'} hectares`,
      annualCO2: `${carbonEstimate.annual_sequestration_tons || 'N/A'} tons/year`,
      confidence: (carbonAnalysis.confidence_level?.toUpperCase() || visionAnalysis.confidence?.toUpperCase() || 'MEDIUM') as 'HIGH' | 'MEDIUM' | 'LOW',
    },
    revenue: {
      estimate: carbonEstimate.potential_revenue_inr?.['1_year']?.mid || 0,
      conservative: carbonEstimate.potential_revenue_inr?.['1_year']?.min || 0,
      optimistic: carbonEstimate.potential_revenue_inr?.['1_year']?.max || 0,
      projections: {
        '1': {
          conservative: carbonEstimate.potential_revenue_inr?.['1_year']?.min || 0,
          mid: carbonEstimate.potential_revenue_inr?.['1_year']?.mid || 0,
          optimistic: carbonEstimate.potential_revenue_inr?.['1_year']?.max || 0,
        },
        '5': {
          conservative: carbonEstimate.potential_revenue_inr?.['5_year']?.min || 0,
          mid: carbonEstimate.potential_revenue_inr?.['5_year']?.mid || 0,
          optimistic: carbonEstimate.potential_revenue_inr?.['5_year']?.max || 0,
        },
        '10': {
          conservative: carbonEstimate.potential_revenue_inr?.['10_year']?.min || 0,
          mid: carbonEstimate.potential_revenue_inr?.['10_year']?.mid || 0,
          optimistic: carbonEstimate.potential_revenue_inr?.['10_year']?.max || 0,
        },
      },
    },
    location: locationData ? {
      city: locationData.location?.city || 'N/A',
      state: locationData.location?.state || 'N/A',
      climateZone: locationData.location?.climate_zone || 'N/A',
      weather: {
        temp: locationData.weather_data?.temperature || 0,
        humidity: locationData.weather_data?.humidity || 0,
        condition: locationData.weather_data?.weather || 'N/A',
      },
      multiplier: `${locationData.climate_multiplier || 'N/A'}x`,
      notes: locationData.adjustments || [],
      analysis: locationData.explanation || 'No analysis available.',
    } : undefined,
    detailedAnalysis: {
      vision: {
        vegetationType: visionAnalysis.vegetation_type || 'N/A',
        density: `${visionAnalysis.vegetation_density || 'N/A'} (${visionAnalysis.density_percentage || 0}%)`,
        condition: visionAnalysis.land_condition || 'N/A',
        visibleFeatures: visionAnalysis.visible_features || [],
        imageQuality: visionAnalysis.image_quality || 'N/A',
        treeCount: visionAnalysis.estimated_tree_count?.toString() || 'N/A',
      },
      carbonCalculations: {
        baseRate: `${calculationDetails.base_rate || 'N/A'} tons/ha`,
        multipliers: `Density: ${calculationDetails.density_multiplier || 'N/A'}x, Condition: ${calculationDetails.condition_multiplier || 'N/A'}x, Climate: ${calculationDetails.climate_multiplier || 'N/A'}x`,
        effectiveRate: `${calculationDetails.effective_rate_per_hectare || 'N/A'} tons/ha`,
        breakdown: `(${calculationDetails.base_rate} * ${calculationDetails.density_multiplier} * ${calculationDetails.condition_multiplier} * ${calculationDetails.climate_multiplier}) * ${carbonEstimate.estimated_land_area_hectares} ha`,
      },
      methodology: {
        areaEstimation: carbonEstimate.area_estimation_method || 'N/A',
        climateAdjustments: calculationDetails.location_adjustment || 'N/A',
        confidenceScoring: `Based on image quality (${visionAnalysis.image_quality}) and visibility of land features.`,
      },
    },
    report: {
      professionalReport: reports.full_report_markdown || '# Report Not Available',
      executiveSummary: reports.executive_summary || 'No executive summary available.',
      textSummary: reports.text_summary || 'No text summary available.',
    },
    recommendations: carbonAnalysis.recommendations || [],
    nextSteps: (carbonAnalysis.next_steps || []).map((step: string) => ({ text: step.substring(step.indexOf('.') + 2), completed: false })),
    disclaimers: carbonAnalysis.disclaimers || [],
  };
}


const API_BASE_URL = "https://carboncreditsanalyzer-production.up.railway.app/";

if (!API_BASE_URL) {
  // In a real app, you'd want to handle this more gracefully.
  // For this project, we'll throw an error during the build if it's not set.
  throw new Error("Missing API_BASE_URL environment variable. Please set it in your .env file.");
}

async function getErrorMessage(response: Response): Promise<string> {
    const contentType = response.headers.get('content-type');
    let errorDetail;

    if (contentType && contentType.includes('application/json')) {
        try {
            const errorData = await response.json();
            errorDetail = errorData.detail || JSON.stringify(errorData);
        } catch (e) {
            errorDetail = `An unexpected JSON error occurred (Status: ${response.status}).`;
        }
    } else {
        try {
            errorDetail = await response.text();
        } catch (e) {
            errorDetail = `An unexpected error occurred (Status: ${response.status}).`;
        }
    }
    return errorDetail || 'An unknown error occurred.';
}

export async function performAnalysis(formData: FormData): Promise<AnalysisResult> {
  const file = formData.get('file');
  if (!file) {
    throw new Error('No file provided for analysis.');
  }

  formData.append('include_report', 'true');

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
        const errorMessage = await getErrorMessage(response);
        throw new Error(errorMessage);
    }

    const result = await response.json();
    return mapApiToAnalysisResult(result);

  } catch (error) {
    console.error('Error in performAnalysis:', error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('The analysis service is currently unavailable. Please ensure your local backend is running and try again.');
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('An unknown error occurred while communicating with the analysis service.');
  }
}

export async function getChatResponse(
  message: string,
  analysisData: AnalysisResult | null
): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_analysis: analysisData,
      }),
    });

    if (!response.ok) {
        const errorMessage = await getErrorMessage(response);
        throw new Error(errorMessage);
    }

    const result = await response.json();
    return result.response || "I'm sorry, I couldn't get a proper response.";

  } catch (error) {
    console.error("Error getting chat response:", error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return 'The chat service is currently unavailable. Please ensure your local backend is running and try again.';
    }
    if (error instanceof Error) {
        return `I'm sorry, an error occurred: ${error.message}`;
    }
    return "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.";
  }
}

export interface AnalysisResult {
  summary: {
    vegetation: {
      type: string;
      description: string;
    };
    landArea: string;
    annualCO2: string;
    confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  };
  revenue: {
    estimate: number;
    conservative: number;
    optimistic: number;
    projections: Record<'1' | '5' | '10', Record<'conservative' | 'mid' | 'optimistic', number>>;
  };
  location?: {
    city: string;
    state: string;
    climateZone: string;
    weather: {
        temp: number;
        humidity: number;
        condition: string;
    };
    multiplier: string;
    notes: string[];
    analysis: string;
  };
  detailedAnalysis: {
    vision: {
      vegetationType: string;
      density: string;
      condition: string;
      visibleFeatures: string[];
      imageQuality: string;
      treeCount?: string;
    };
    carbonCalculations: {
      baseRate: string;
      multipliers: string;
      effectiveRate: string;
      breakdown: string;
    };
    methodology: {
      areaEstimation: string;
      climateAdjustments: string;
      confidenceScoring: string;
    };
  };
  report: {
    professionalReport: string;
    executiveSummary: string;
    textSummary: string;
  };
  recommendations: string[];
  nextSteps: { text: string; completed: boolean }[];
  disclaimers: string[];
}

export interface AnalysisProgressStep {
  name: string;
  status: 'pending' | 'in-progress' | 'complete' | 'error';
}

export type ChatMessage = {
  role: 'user' | 'bot';
  content: string;
  timestamp: string;
  isTyping?: boolean;
};

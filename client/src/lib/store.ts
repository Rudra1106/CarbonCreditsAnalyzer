"use client";

import { create } from 'zustand';
import type { AnalysisResult, AnalysisProgressStep } from '@/lib/types';

interface AppState {
  analysisResult: AnalysisResult | null;
  setAnalysisResult: (result: AnalysisResult | null) => void;
  isAnalyzing: boolean;
  analysisProgress: AnalysisProgressStep[];
  setAnalyzing: (isAnalyzing: boolean) => void;
  setAnalysisProgress: (progress: AnalysisProgressStep[]) => void;
  clearAnalysis: () => void;
}

const initialProgress: AnalysisProgressStep[] = [
  { name: 'Processing image', status: 'pending' },
  { name: 'Fetching location data', status: 'pending' },
  { name: 'Running AI analysis', status: 'pending' },
  { name: 'Calculating carbon potential', status: 'pending' },
  { name: 'Generating report', status: 'pending' },
];

export const useAppStore = create<AppState>((set) => ({
  analysisResult: null,
  setAnalysisResult: (result) => set({ analysisResult: result }),
  isAnalyzing: false,
  analysisProgress: initialProgress,
  setAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
  setAnalysisProgress: (progress) => set({ analysisProgress: progress }),
  clearAnalysis: () => set({ analysisResult: null, isAnalyzing: false, analysisProgress: initialProgress }),
}));

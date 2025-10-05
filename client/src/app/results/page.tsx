"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { MainLayout } from '@/components/layout/main-layout';
import { SummaryCards } from '@/components/results/summary-cards';
import { RevenueProjection } from '@/components/results/revenue-projection';
import { LocationAnalysis } from '@/components/results/location-analysis';
import { DetailedAnalysis } from '@/components/results/detailed-analysis';
import { ReportSection } from '@/components/results/report-section';
import { Recommendations } from '@/components/results/recommendations';
import { NextSteps } from '@/components/results/next-steps';
import { Disclaimer } from '@/components/results/disclaimer';
import { ActionsBar } from '@/components/results/actions-bar';
import { ExecutiveSummary } from '@/components/results/executive-summary';
import { Loader2 } from 'lucide-react';

export default function ResultsPage() {
  const router = useRouter();
  const { analysisResult, clearAnalysis } = useAppStore();

  useEffect(() => {
    if (!analysisResult) {
      router.replace('/analyze');
    }
  }, [analysisResult, router]);

  const handleAnalyzeAnother = () => {
    clearAnalysis();
    router.push('/analyze');
  };

  const handleChat = () => {
    router.push('/chat');
  };

  if (!analysisResult) {
    return (
      <MainLayout>
        <div className="flex h-screen items-center justify-center">
          <div className="flex items-center gap-2 text-lg">
            <Loader2 className="h-6 w-6 animate-spin" />
            Loading analysis results...
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="container mx-auto max-w-7xl py-12 px-4 sm:px-6 lg:px-8 space-y-8">
        <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl font-headline">
          Your Farmland Analysis Results
        </h1>
        
        <SummaryCards summary={analysisResult.summary} />

        <ExecutiveSummary 
          executiveSummary={analysisResult.report.executiveSummary} 
          textSummary={analysisResult.report.textSummary}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <RevenueProjection revenue={analysisResult.revenue} />
            <DetailedAnalysis analysis={analysisResult.detailedAnalysis} />
          </div>
          <div className="space-y-8">
            {analysisResult.location && <LocationAnalysis location={analysisResult.location} />}
            <ReportSection report={analysisResult.report.professionalReport} />
            <Recommendations recommendations={analysisResult.recommendations} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <NextSteps steps={analysisResult.nextSteps} />
            <Disclaimer disclaimers={analysisResult.disclaimers} />
        </div>

      </div>
      <ActionsBar
        onAnalyzeAnother={handleAnalyzeAnother}
        onChat={handleChat}
        report={analysisResult.report.professionalReport}
      />
    </MainLayout>
  );
}

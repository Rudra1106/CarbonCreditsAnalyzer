"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Eye, Calculator, BookOpen } from 'lucide-react';
import type { AnalysisResult } from "@/lib/types";

interface DetailedAnalysisProps {
  analysis: AnalysisResult['detailedAnalysis'];
}

function AnalysisDetail({ label, value }: { label: string; value?: string }) {
    if (!value) return null;
    return (
        <div>
            <p className="text-sm font-semibold">{label}</p>
            <p className="text-muted-foreground">{value}</p>
        </div>
    );
}

export function DetailedAnalysis({ analysis }: DetailedAnalysisProps) {
  const { vision, carbonCalculations, methodology } = analysis;

  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="text-2xl font-headline">Detailed Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="vision" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="vision"><Eye className="mr-2 h-4 w-4" />Vision Analysis</TabsTrigger>
            <TabsTrigger value="calculations"><Calculator className="mr-2 h-4 w-4" />Calculations</TabsTrigger>
            <TabsTrigger value="methodology"><BookOpen className="mr-2 h-4 w-4" />Methodology</TabsTrigger>
          </TabsList>
          
          <TabsContent value="vision" className="mt-6 space-y-4">
            <AnalysisDetail label="Vegetation Type" value={vision.vegetationType} />
            <AnalysisDetail label="Density" value={vision.density} />
            <AnalysisDetail label="Condition" value={vision.condition} />
            <AnalysisDetail label="Visible Features" value={vision.visibleFeatures.join(', ')} />
            <AnalysisDetail label="Image Quality" value={vision.imageQuality} />
            <AnalysisDetail label="Estimated Tree Count" value={vision.treeCount} />
          </TabsContent>

          <TabsContent value="calculations" className="mt-6 space-y-4">
            <AnalysisDetail label="Base Sequestration Rate" value={carbonCalculations.baseRate} />
            <AnalysisDetail label="Applied Multipliers" value={carbonCalculations.multipliers} />
            <AnalysisDetail label="Effective Rate" value={carbonCalculations.effectiveRate} />
            <AnalysisDetail label="Breakdown" value={carbonCalculations.breakdown} />
          </TabsContent>

          <TabsContent value="methodology" className="mt-6 space-y-4">
            <AnalysisDetail label="Area Estimation" value={methodology.areaEstimation} />
            <AnalysisDetail label="Climate Adjustments" value={methodology.climateAdjustments} />
            <AnalysisDetail label="Confidence Scoring" value={methodology.confidenceScoring} />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

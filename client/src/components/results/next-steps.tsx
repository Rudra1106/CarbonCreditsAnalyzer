"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { ListChecks } from 'lucide-react';
import type { AnalysisResult } from "@/lib/types";

interface NextStepsProps {
  steps: AnalysisResult['nextSteps'];
}

export function NextSteps({ steps }: NextStepsProps) {
  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl font-headline">
          <ListChecks className="h-6 w-6 text-accent" />
          Your Next Steps
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {steps.map((step, index) => (
          <div key={index} className="flex items-center space-x-3">
            <Checkbox id={`step-${index}`} checked={step.completed} />
            <Label htmlFor={`step-${index}`} className="text-base text-muted-foreground">
              {step.text}
            </Label>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

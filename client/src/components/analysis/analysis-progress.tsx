"use client";

import { useAppStore } from "@/lib/store";
import { CheckCircle2, Loader2, CircleDashed } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export function AnalysisProgress() {
  const { analysisProgress } = useAppStore();

  const getStatusIcon = (status: "pending" | "in-progress" | "complete" | "error") => {
    switch (status) {
      case "complete":
        return <CheckCircle2 className="h-6 w-6 text-green-500" />;
      case "in-progress":
        return <Loader2 className="h-6 w-6 animate-spin text-primary" />;
      case "pending":
        return <CircleDashed className="h-6 w-6 text-muted-foreground" />;
      case "error":
        return <CheckCircle2 className="h-6 w-6 text-destructive" />;
      default:
        return null;
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto animate-fade-in">
      <CardHeader className="text-center">
        <CardTitle className="text-3xl font-bold font-headline">Analyzing Your Land...</CardTitle>
        <CardDescription>Estimated time: 20-30 seconds. Please don't close this page.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 pt-4">
          {analysisProgress.map((step, index) => (
            <div key={index} className="flex items-center gap-4 text-lg">
              <div>{getStatusIcon(step.status)}</div>
              <span className={step.status === 'pending' ? 'text-muted-foreground' : ''}>{step.name}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

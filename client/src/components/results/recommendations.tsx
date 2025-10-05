"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb } from 'lucide-react';

interface RecommendationsProps {
  recommendations: string[];
}

export function Recommendations({ recommendations }: RecommendationsProps) {
  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl font-headline">
          <Lightbulb className="h-6 w-6 text-accent" />
          Expert Recommendations
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-3">
          {recommendations.map((rec, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="mt-1 flex h-2 w-2 translate-y-1 rounded-full bg-primary" />
              <span className="text-muted-foreground">{rec}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

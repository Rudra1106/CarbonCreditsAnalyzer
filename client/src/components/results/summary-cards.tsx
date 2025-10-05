"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TreePine, LandPlot, Cloud, Sparkles } from "lucide-react";
import type { AnalysisResult } from "@/lib/types";

interface SummaryCardsProps {
  summary: AnalysisResult['summary'];
}

export function SummaryCards({ summary }: SummaryCardsProps) {
  const { vegetation, landArea, annualCO2, confidence } = summary;

  const confidenceVariant = {
    HIGH: 'default',
    MEDIUM: 'secondary',
    LOW: 'destructive',
  } as const;

  const cards = [
    {
      icon: <TreePine className="h-8 w-8 text-primary" />,
      title: "Vegetation",
      value: vegetation.type,
      description: vegetation.description,
    },
    {
      icon: <LandPlot className="h-8 w-8 text-primary" />,
      title: "Land Area",
      value: landArea,
      description: "Estimated area",
    },
    {
      icon: <Cloud className="h-8 w-8 text-primary" />,
      title: "Annual CO2",
      value: annualCO2,
      description: "Sequestration estimate",
    },
    {
      icon: <Sparkles className="h-8 w-8 text-primary" />,
      title: "Confidence",
      value: (
        <Badge variant={confidenceVariant[confidence] || 'secondary'} className="text-base">
          {confidence}
        </Badge>
      ),
      description: "Analysis confidence",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => (
        <Card key={index} className="bg-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
            {card.icon}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{card.value}</div>
            <p className="text-xs text-muted-foreground">{card.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

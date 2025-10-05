"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { IndianRupee } from "lucide-react";
import type { AnalysisResult } from "@/lib/types";

interface RevenueProjectionProps {
  revenue: AnalysisResult['revenue'];
}

export function RevenueProjection({ revenue }: RevenueProjectionProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(value);
  };
  
  const formatLargeCurrency = (value: number) => {
    if (value >= 10000000) {
      return `₹${(value / 10000000).toFixed(2)} Cr`;
    }
    if (value >= 100000) {
      return `₹${(value / 100000).toFixed(2)} L`;
    }
    return formatCurrency(value);
  }

  const projectionData = [
    { timeframe: '1 Year', ...revenue.projections['1'] },
    { timeframe: '5 Years', ...revenue.projections['5'] },
    { timeframe: '10 Years', ...revenue.projections['10'] },
  ];

  return (
    <Card className="bg-white shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-2xl font-headline">
          <IndianRupee className="h-8 w-8 text-accent" />
          Estimated Annual Revenue
        </CardTitle>
        <CardDescription>Based on current carbon market estimates.</CardDescription>
      </CardHeader>
      <CardContent className="text-center">
        <p className="text-5xl font-bold text-primary">{formatCurrency(revenue.estimate)}</p>
        <p className="text-muted-foreground">(Mid-range estimate)</p>
        <div className="mt-6 flex justify-around text-sm">
          <div>
            <p className="text-muted-foreground">Conservative</p>
            <p className="font-semibold">{formatCurrency(revenue.conservative)}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Optimistic</p>
            <p className="font-semibold">{formatCurrency(revenue.optimistic)}</p>
          </div>
        </div>
      </CardContent>
      <CardFooter className="p-0">
        <Accordion type="single" collapsible className="w-full">
          <AccordionItem value="item-1" className="border-t">
            <AccordionTrigger className="px-6 py-3 text-base">
              View 5-year & 10-year projections
            </AccordionTrigger>
            <AccordionContent className="px-6 pb-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Time Frame</TableHead>
                    <TableHead className="text-right">Conservative</TableHead>
                    <TableHead className="text-right font-bold">Mid-Range</TableHead>
                    <TableHead className="text-right">Optimistic</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {projectionData.map((proj) => (
                    <TableRow key={proj.timeframe}>
                      <TableCell className="font-medium">{proj.timeframe}</TableCell>
                      <TableCell className="text-right">{formatLargeCurrency(proj.conservative)}</TableCell>
                      <TableCell className="text-right font-bold">{formatLargeCurrency(proj.mid)}</TableCell>
                      <TableCell className="text-right">{formatLargeCurrency(proj.optimistic)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardFooter>
    </Card>
  );
}

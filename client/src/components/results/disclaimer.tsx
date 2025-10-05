"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { AlertTriangle } from 'lucide-react';

interface DisclaimerProps {
  disclaimers: string[];
}

export function Disclaimer({ disclaimers }: DisclaimerProps) {
  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl font-headline">
          <AlertTriangle className="h-6 w-6 text-destructive" />
          Important Disclaimers
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible defaultValue="item-0">
          {disclaimers.map((disclaimer, index) => (
            <AccordionItem value={`item-${index}`} key={index}>
              <AccordionTrigger className="text-left">{disclaimer.split('.')[0]}.</AccordionTrigger>
              <AccordionContent className="text-muted-foreground">
                {disclaimer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  );
}

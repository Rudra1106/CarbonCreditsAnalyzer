"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ExecutiveSummaryProps {
  executiveSummary: string;
  textSummary: string;
}

export function ExecutiveSummary({ executiveSummary, textSummary }: ExecutiveSummaryProps) {
  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-2xl font-headline">
          <FileText className="h-6 w-6 text-accent" />
          Executive Summary
        </CardTitle>
        <CardDescription>A high-level overview of your farmland's potential.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="prose prose-sm max-w-none text-muted-foreground">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{executiveSummary}</ReactMarkdown>
        </div>
        <div className="p-4 rounded-lg bg-muted/50 border">
             <pre className="text-sm whitespace-pre-wrap font-sans text-muted-foreground">
                {textSummary}
             </pre>
        </div>
      </CardContent>
    </Card>
  );
}

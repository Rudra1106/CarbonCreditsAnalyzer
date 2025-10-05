"use client";

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Download } from 'lucide-react';
import { ReportViewer } from './report-viewer';
import { useToast } from '@/hooks/use-toast';

interface ReportSectionProps {
  report: string;
}

export function ReportSection({ report }: ReportSectionProps) {
  const [isViewerOpen, setViewerOpen] = useState(false);
  const { toast } = useToast();

  const handleDownload = () => {
    if (!report) {
      toast({
        variant: "destructive",
        title: "Download Failed",
        description: "Report content is not available to download.",
      });
      return;
    }
    toast({
      title: "Downloading Report",
      description: "Your report is being prepared for download as a Markdown file.",
    });
    const blob = new Blob([report], { type: 'text/markdown;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'AgriCarbon_Insights_Report.md';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <>
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl font-headline">
            <FileText className="h-6 w-6 text-accent" />
            Professional Report
          </CardTitle>
          <CardDescription>
            Your comprehensive analysis is ready to share with certification programs.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex gap-2">
          <Button onClick={() => setViewerOpen(true)} className="flex-1">
            <FileText className="mr-2 h-4 w-4" /> View Full Report
          </Button>
          <Button onClick={handleDownload} variant="outline" size="icon" aria-label="Download Report">
              <Download className="h-4 w-4" />
          </Button>
        </CardContent>
      </Card>
      <ReportViewer isOpen={isViewerOpen} onOpenChange={setViewerOpen} reportContent={report} />
    </>
  );
}

"use client";

import { Button } from "@/components/ui/button";
import { ArrowLeft, MessageSquare, Download } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface ActionsBarProps {
  onAnalyzeAnother: () => void;
  onChat: () => void;
  report: string;
}

export function ActionsBar({ onAnalyzeAnother, onChat, report }: ActionsBarProps) {
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
    <div className="sticky bottom-0 z-40 w-full bg-background/80 p-4 backdrop-blur-sm border-t">
      <div className="container mx-auto flex items-center justify-center gap-2 sm:gap-4">
        <Button variant="outline" onClick={onAnalyzeAnother}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Analyze Another
        </Button>
        <Button onClick={onChat}>
          <MessageSquare className="mr-2 h-4 w-4" />
          Chat with Expert
        </Button>
        <Button variant="secondary" onClick={handleDownload}>
          <Download className="mr-2 h-4 w-4" />
          Download Report
        </Button>
      </div>
    </div>
  );
}

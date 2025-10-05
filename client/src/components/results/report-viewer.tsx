"use client";

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Copy, Printer } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

interface ReportViewerProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  reportContent: string;
}

export function ReportViewer({ isOpen, onOpenChange, reportContent }: ReportViewerProps) {
    const { toast } = useToast();

    const handleCopy = () => {
        navigator.clipboard.writeText(reportContent);
        toast({ title: "Report copied to clipboard!" });
    };

    const handlePrint = () => {
        const printWindow = window.open('', '_blank');
        if (printWindow) {
            printWindow.document.write('<html><head><title>AgriCarbon Insights Report</title>');
            printWindow.document.write('<style>body { font-family: sans-serif; } table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid #ddd; padding: 8px; text-align: left; } th { background-color: #f2f2f2; }</style>');
            printWindow.document.write('</head><body>');
            
            const printableContent = document.getElementById('printable-report-content');
            if(printableContent) {
                printWindow.document.write(printableContent.innerHTML);
            }

            printWindow.document.write('</body></html>');
            printWindow.document.close();
            printWindow.focus();
            printWindow.print();
        }
    };

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Professional Report</DialogTitle>
          <DialogDescription>
            A comprehensive overview of your farmland's carbon credit potential.
          </DialogDescription>
        </DialogHeader>
        <ScrollArea className="flex-1 -mx-6 px-6">
            <div id="printable-report-content" className="prose dark:prose-invert max-w-none">
                <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                >
                    {reportContent}
                </ReactMarkdown>
            </div>
        </ScrollArea>
        <DialogFooter className="mt-4">
            <Button variant="outline" onClick={handleCopy}>
                <Copy className="mr-2 h-4 w-4" /> Copy
            </Button>
            <Button onClick={handlePrint}>
                <Printer className="mr-2 h-4 w-4" /> Print
            </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

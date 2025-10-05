
"use client";

import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ArrowUp, Paperclip, Search, Lightbulb, MoreHorizontal } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface ChatInputV2Props {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

export function ChatInputV2({ onSendMessage, disabled }: ChatInputV2Props) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSendMessage(message);
    setMessage('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <TooltipProvider>
      <form 
        onSubmit={handleSubmit} 
        className="relative w-full p-2 rounded-2xl bg-white border shadow-lg"
        onClick={() => textareaRef.current?.focus()}
      >
        <Textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
          className="w-full text-base resize-none border-none focus-visible:ring-0 shadow-none p-4 pr-16"
          rows={1}
          disabled={disabled}
        />

        <div className="absolute bottom-4 right-4 flex items-center">
            <Button 
                type="submit" 
                size="icon" 
                disabled={disabled || !message.trim()} 
                aria-label="Send message"
                className="bg-foreground text-background rounded-lg h-9 w-9 hover:bg-foreground/80"
            >
                <ArrowUp className="h-5 w-5" />
            </Button>
        </div>

        <div className="flex items-center gap-1 p-2 border-t">
          <Tooltip>
            <TooltipTrigger asChild>
                <Button type="button" variant="ghost" size="icon" className="h-8 w-8 rounded-full" disabled={disabled}>
                    <Paperclip className="h-4 w-4" />
                </Button>
            </TooltipTrigger>
            <TooltipContent><p>Attach file</p></TooltipContent>
          </Tooltip>

          <Tooltip>
            <TooltipTrigger asChild>
                <Button type="button" variant="ghost" className="rounded-full h-8 px-3" disabled={disabled}>
                    <Search className="h-4 w-4 mr-2" />
                    Deep Search
                </Button>
            </TooltipTrigger>
            <TooltipContent><p>Enable deep search</p></TooltipContent>
          </Tooltip>
           
          <Tooltip>
            <TooltipTrigger asChild>
                <Button type="button" variant="ghost" className="rounded-full h-8 px-3" disabled={disabled}>
                    <Lightbulb className="h-4 w-4 mr-2" />
                    Reason
                </Button>
            </TooltipTrigger>
            <TooltipContent><p>Explain reasoning</p></TooltipContent>
          </Tooltip>

          <Tooltip>
            <TooltipTrigger asChild>
                <Button type="button" variant="ghost" size="icon" className="h-8 w-8 rounded-full" disabled={disabled}>
                    <MoreHorizontal className="h-4 w-4" />
                </Button>
            </TooltipTrigger>
            <TooltipContent><p>More options</p></TooltipContent>
          </Tooltip>
        </div>
      </form>
    </TooltipProvider>
  );
}

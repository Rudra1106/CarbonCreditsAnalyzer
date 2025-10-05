"use client";

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ChatMessages } from '@/components/chat/chat-messages';
import { ChatInput } from '@/components/chat/chat-input';
import { getChatResponse } from '@/lib/actions';
import { useAppStore } from '@/lib/store';
import type { ChatMessage } from '@/lib/types';
import { X } from 'lucide-react';

interface ChatPanelProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
}

export function ChatPanel({ isOpen, onOpenChange }: ChatPanelProps) {
  const { analysisResult } = useAppStore();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messages.length > 0 && scrollAreaRef.current) {
        const viewport = scrollAreaRef.current.querySelector('div');
        if (viewport) {
            viewport.scrollTo({
                top: viewport.scrollHeight,
                behavior: 'smooth',
            });
        }
    }
  }, [messages, isBotTyping]);
  
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsBotTyping(true);

    try {
      const botResponse = await getChatResponse(message, analysisResult);
      const botMessage: ChatMessage = {
        role: 'bot',
        content: botResponse,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
        console.error("Failed to get chat response:", error);
        const errorMessage: ChatMessage = {
            role: 'bot',
            content: error instanceof Error ? error.message : 'Sorry, something went wrong.',
            timestamp: new Date().toLocaleTimeString(),
        };
        setMessages((prev) => [...prev, errorMessage]);
    } finally {
        setIsBotTyping(false);
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={onOpenChange}>
      <SheetContent className="w-full sm:w-[540px] flex flex-col p-0">
        <SheetHeader className="p-6">
          <SheetTitle>Chat with Expert</SheetTitle>
        </SheetHeader>
        <ScrollArea className="flex-1" ref={scrollAreaRef}>
            <div className="px-6">
                <ChatMessages messages={messages} isBotTyping={isBotTyping} />
            </div>
        </ScrollArea>
        <SheetFooter className="p-6 pt-2 bg-background border-t">
          <div className="w-full space-y-2">
            <ChatInput onSendMessage={handleSendMessage} disabled={isBotTyping} />
            <p className="text-center text-xs text-muted-foreground">
              AI can make mistakes. Please double-check responses.
            </p>
          </div>
        </SheetFooter>
        <Button 
            variant="ghost" 
            size="icon"
            onClick={() => onOpenChange(false)}
            className="absolute top-4 right-4"
        >
            <X className="h-5 w-5" />
        </Button>
      </SheetContent>
    </Sheet>
  );
}

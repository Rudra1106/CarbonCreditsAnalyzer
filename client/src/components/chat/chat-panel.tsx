"use client";

import { useState, useEffect, useRef } from 'react';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Bot, Trash2 } from 'lucide-react';
import { ChatMessages } from './chat-messages';
import { ChatInput } from './chat-input';
import { SuggestedQuestions } from './suggested-questions';
import { getChatResponse, getChatSuggestions } from '@/lib/actions';
import { useAppStore } from '@/lib/store';
import type { ChatMessage } from '@/lib/types';

interface ChatPanelProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ChatPanel({ isOpen, onOpenChange }: ChatPanelProps) {
  const { analysisResult } = useAppStore();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      if (messages.length === 0) {
        setMessages([
          {
            role: 'bot',
            content: `Hi! I'm your carbon credit expert. I can help you understand your analysis results. How can I assist you?`,
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
      }
      fetchSuggestions();
    }
  }, [isOpen, messages.length]);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTo({
        top: scrollAreaRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isBotTyping]);

  const fetchSuggestions = async () => {
    const newSuggestions = await getChatSuggestions(analysisResult);
    setSuggestions(newSuggestions);
  };

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsBotTyping(true);

    const chatHistory = [...messages, userMessage].map(({ role, content }) => ({ role, content }));

    try {
      const botResponse = await getChatResponse(message, chatHistory, analysisResult);
      const botMessage: ChatMessage = {
        role: 'bot',
        content: botResponse,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: 'bot',
        content: 'Sorry, something went wrong. Please try again.',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsBotTyping(false);
      fetchSuggestions();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'bot',
        content: 'Hi again! How can I help you understand your results?',
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  };

  return (
    <Sheet open={isOpen} onOpenChange={onOpenChange}>
      <SheetContent className="w-full sm:max-w-md flex flex-col p-0">
        <SheetHeader className="p-6 pb-2">
          <SheetTitle className="flex items-center gap-2">
            <Bot className="h-6 w-6 text-primary" />
            Carbon Credit Expert
          </SheetTitle>
          <SheetDescription>Ask me anything about your analysis.</SheetDescription>
        </SheetHeader>
        <div className="relative flex-1">
          <ScrollArea className="absolute inset-0 h-full w-full px-6">
            <ChatMessages messages={messages} isBotTyping={isBotTyping} />
          </ScrollArea>
        </div>
        <SheetFooter className="flex-col p-4 border-t bg-background">
          <SuggestedQuestions
            suggestions={suggestions}
            onSuggestionClick={handleSendMessage}
            disabled={isBotTyping}
          />
          <div className="flex w-full items-center gap-2">
            <ChatInput onSendMessage={handleSendMessage} disabled={isBotTyping} />
            <Button variant="ghost" size="icon" onClick={clearChat} disabled={isBotTyping} aria-label="Clear chat">
              <Trash2 className="h-5 w-5" />
            </Button>
          </div>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}

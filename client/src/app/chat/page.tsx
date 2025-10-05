
"use client";

import { useState, useEffect, useRef } from 'react';
import { MainLayout } from '@/components/layout/main-layout';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Bot, User, ArrowUp, Paperclip, Search, Lightbulb, MoreHorizontal } from 'lucide-react';
import { ChatMessages } from '@/components/chat/chat-messages';
import { ChatInputV2 } from '@/components/chat/chat-input-v2';
import { SuggestedQuestions } from '@/components/chat/suggested-questions';
import { getChatResponse, getChatSuggestions } from '@/lib/actions';
import { useAppStore } from '@/lib/store';
import type { ChatMessage } from '@/lib/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export default function ChatPage() {
  const { analysisResult } = useAppStore();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
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

    // const chatHistory = [...messages, userMessage].map(({ role, content }) => ({ role, content }));

    try {
      const botResponse = await getChatResponse(message, analysisResult);
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
    }
  };


  return (
    <MainLayout>
        <div className="flex flex-col h-screen-minus-header-footer">
          <ScrollArea className="flex-1" ref={scrollAreaRef}>
            {messages.length > 0 ? (
                <div className="container mx-auto max-w-4xl py-12 px-4 sm:px-6 lg:px-8">
                  <ChatMessages messages={messages} isBotTyping={isBotTyping} />
                </div>
            ) : (
                <div className="flex justify-center items-center h-full">
                    <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl font-headline">
                        What can I help with?
                    </h1>
                </div>
            )}
          </ScrollArea>
          
          <div className="container mx-auto max-w-3xl pb-8 px-4 sm:px-6 lg:px-8">
            <ChatInputV2 onSendMessage={handleSendMessage} disabled={isBotTyping} />
            <p className="text-center text-xs text-muted-foreground mt-2">
              AI can make mistakes. Please double-check responses.
            </p>
          </div>
        </div>
    </MainLayout>
  );
}

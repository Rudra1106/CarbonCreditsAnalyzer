"use client";

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from '@/lib/utils';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Bot, User } from 'lucide-react';
import type { ChatMessage } from '@/lib/types';

interface ChatMessagesProps {
  messages: ChatMessage[];
  isBotTyping: boolean;
}

export function ChatMessages({ messages, isBotTyping }: ChatMessagesProps) {
  return (
    <div className="space-y-8 py-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={cn('flex items-start gap-4', {
            'justify-end': message.role === 'user',
          })}
        >
          {message.role === 'bot' && (
            <Avatar className="h-8 w-8 bg-primary text-primary-foreground">
              <AvatarFallback className="bg-transparent">
                <Bot className="h-5 w-5" />
              </AvatarFallback>
            </Avatar>
          )}
          <div
            className={cn('max-w-[80%] rounded-lg px-4 py-3 text-base', {
              'bg-muted': message.role === 'bot',
              'bg-primary text-primary-foreground': message.role === 'user',
            })}
          >
            <div className="prose dark:prose-invert max-w-none prose-p:my-0">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  a: ({ node, ...props }) => (
                    <a 
                      {...props} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="text-primary underline" 
                    />
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
          {message.role === 'user' && (
            <Avatar className="h-8 w-8">
              <AvatarFallback>
                <User className="h-5 w-5" />
              </AvatarFallback>
            </Avatar>
          )}
        </div>
      ))}
      {isBotTyping && (
        <div className="flex items-start gap-3">
          <Avatar className="h-8 w-8 bg-primary text-primary-foreground">
            <AvatarFallback className="bg-transparent">
              <Bot className="h-5 w-5" />
            </AvatarFallback>
          </Avatar>
          <div className="max-w-[80%] rounded-lg px-4 py-3 text-base bg-muted flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.3s]" />
            <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.15s]" />
            <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" />
          </div>
        </div>
      )}
    </div>
  );
}
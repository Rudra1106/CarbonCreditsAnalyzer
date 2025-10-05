"use client";

import { Button } from '@/components/ui/button';
import { Lightbulb } from 'lucide-react';

interface SuggestedQuestionsProps {
  suggestions: string[];
  onSuggestionClick: (suggestion: string) => void;
  disabled: boolean;
}

export function SuggestedQuestions({ suggestions, onSuggestionClick, disabled }: SuggestedQuestionsProps) {
  if (suggestions.length === 0) return null;

  return (
    <div className="w-full space-y-2 mb-2">
        <p className="text-sm font-medium flex items-center gap-2"><Lightbulb className="h-4 w-4 text-accent" /> Suggested Questions:</p>
        <div className="flex flex-wrap gap-2">
        {suggestions.map((q, i) => (
            <Button
            key={i}
            variant="outline"
            size="sm"
            onClick={() => onSuggestionClick(q)}
            disabled={disabled}
            className="text-xs h-auto py-1 px-2"
            >
            {q}
            </Button>
        ))}
        </div>
    </div>
  );
}

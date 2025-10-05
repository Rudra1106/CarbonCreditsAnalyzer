"use client";

import { Info } from "lucide-react";
import { INDIAN_STATES } from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface LocationSelectorProps {
  onLocationChange: (location: { city: string; state: string }) => void;
}

export function LocationSelector({ onLocationChange }: LocationSelectorProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <h3 className="text-xl font-semibold">Select Location (Optional)</h3>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger>
              <Info className="h-5 w-5 text-muted-foreground" />
            </TooltipTrigger>
            <TooltipContent>
              <p>Location improves accuracy by 15-20%</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="city">City</Label>
          <Input
            id="city"
            placeholder="e.g., Surat"
            onChange={(e) => onLocationChange({ city: e.target.value, state: "" })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="state">State</Label>
          <Select onValueChange={(value) => onLocationChange({ city: "", state: value })}>
            <SelectTrigger id="state">
              <SelectValue placeholder="e.g., Gujarat" />
            </SelectTrigger>
            <SelectContent>
              {INDIAN_STATES.map((state) => (
                <SelectItem key={state} value={state}>
                  {state}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}

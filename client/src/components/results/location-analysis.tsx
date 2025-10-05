"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MapPin, Thermometer, Droplets, CheckCircle2, Wind } from 'lucide-react';
import type { AnalysisResult } from "@/lib/types";

interface LocationAnalysisProps {
  location: NonNullable<AnalysisResult['location']>;
}

export function LocationAnalysis({ location }: LocationAnalysisProps) {
  return (
    <Card className="bg-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl font-headline">
          <MapPin className="h-6 w-6 text-accent" />
          Location Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="font-bold text-lg">{location.city}, {location.state}</p>
          <p className="text-sm text-muted-foreground">Climate Zone: {location.climateZone}</p>
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
           <p className="flex items-center gap-2"><Thermometer className="h-4 w-4 text-muted-foreground"/> Temp: {location.weather.temp.toFixed(1)}°C</p>
           <p className="flex items-center gap-2"><Droplets className="h-4 w-4 text-muted-foreground"/> Humidity: {location.weather.humidity}%</p>
           <p className="flex items-center gap-2 col-span-2"><Wind className="h-4 w-4 text-muted-foreground"/> Weather: {location.weather.condition}</p>
           <p className="flex items-center gap-2 col-span-2"><CheckCircle2 className="h-4 w-4 text-green-500"/> Climate Multiplier: {location.multiplier}</p>
        </div>

        <div className="space-y-1 text-sm">
            <h4 className="font-semibold mb-1">Favorable Conditions:</h4>
            {location.notes.map((note, index) => (
                <p key={index} className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-green-500"/> {note}</p>
            ))}
        </div>

        <div>
            <h4 className="font-semibold mb-1">Refined Analysis:</h4>
            <p className="text-sm text-muted-foreground italic">"{location.analysis}"</p>
        </div>
      </CardContent>
    </Card>
  );
}

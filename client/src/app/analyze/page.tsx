"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";
import { MainLayout } from "@/components/layout/main-layout";
import { ImageUploader } from "@/components/analysis/image-uploader";
import { LocationSelector } from "@/components/analysis/location-selector";
import { AnalysisProgress } from "@/components/analysis/analysis-progress";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { performAnalysis } from "@/lib/actions";
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from "lucide-react";

export default function AnalyzePage() {
  const router = useRouter();
  const { toast } = useToast();
  const [isPending, startTransition] = useTransition();
  const { setAnalysisResult, setAnalyzing, isAnalyzing, setAnalysisProgress, clearAnalysis } = useAppStore();

  const [imageFile, setImageFile] = useState<File | null>(null);
  const [location, setLocation] = useState<{ city: string; state: string }>({ city: "", state: "" });

  const handleAnalysis = async () => {
    if (!imageFile) {
      toast({
        title: "Image Required",
        description: "Please upload an image of your farmland to begin.",
        variant: "destructive",
      });
      return;
    }

    setAnalyzing(true);
    
    const progressInterval = setInterval(() => {
      setAnalysisProgress(
        useAppStore.getState().analysisProgress.map(p => {
          if (p.status === 'pending') {
            return { ...p, status: 'in-progress' };
          }
          if (p.status === 'in-progress') {
            return { ...p, status: 'complete' };
          }
          return p;
        })
      );
    }, 500);

    const formData = new FormData();
    formData.append("file", imageFile);
    if (location.city) formData.append("city", location.city);
    if (location.state) formData.append("state", location.state);

    startTransition(async () => {
      try {
        const result = await performAnalysis(formData);
        setAnalysisResult(result);
        router.push("/results");
      } catch (error) {
        console.error("Analysis failed:", error);
        toast({
          title: "Analysis Failed",
          description: error instanceof Error ? error.message : "An unknown error occurred. Please try again.",
          variant: "destructive",
        });
        clearAnalysis();
      } finally {
        clearInterval(progressInterval);
        setAnalyzing(false);
      }
    });
  };

  return (
    <MainLayout>
      <div className="container mx-auto max-w-4xl py-12 px-4 sm:px-6 lg:px-8">
        {isAnalyzing ? (
          <AnalysisProgress />
        ) : (
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl font-headline">
                Analyze Your Land
              </h1>
              <p className="mt-4 text-lg text-muted-foreground">
                Upload a photo to get started. Add a location for a more accurate result.
              </p>
            </div>

            <Card className="bg-white">
              <CardContent className="p-8 space-y-8">
                <ImageUploader onFileChange={setImageFile} />

                {imageFile && (
                  <div className="animate-in fade-in-50 duration-500">
                    <LocationSelector onLocationChange={setLocation} />
                  </div>
                )}
              </CardContent>
            </Card>

            <div className="flex justify-end">
              <Button
                size="lg"
                onClick={handleAnalysis}
                disabled={!imageFile || isPending || isAnalyzing}
                className="w-full md:w-auto"
              >
                {isPending || isAnalyzing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  "Analyze My Land"
                )}
              </Button>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}

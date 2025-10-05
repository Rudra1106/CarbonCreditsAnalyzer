"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";
import { UploadCloud, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

interface ImageUploaderProps {
  onFileChange: (file: File | null) => void;
}

export function ImageUploader({ onFileChange }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [fileSize, setFileSize] = useState<string>("");
  const { toast } = useToast();

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    if (fileRejections.length > 0) {
      fileRejections.forEach(({ errors }: any) => {
        errors.forEach((error: any) => {
          toast({
            title: "Upload Error",
            description: error.message,
            variant: "destructive",
          });
        });
      });
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setPreview(URL.createObjectURL(file));
      setFileName(file.name);
      setFileSize((file.size / (1024 * 1024)).toFixed(2) + " MB");
      onFileChange(file);
    }
  }, [onFileChange, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': [],
      'image/png': [],
      'image/webp': [],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false,
  });

  const handleRemove = () => {
    setPreview(null);
    setFileName("");
    setFileSize("");
    onFileChange(null);
    if (preview) {
      URL.revokeObjectURL(preview);
    }
  };

  if (preview) {
    return (
      <div className="relative w-full max-w-md mx-auto p-4 border rounded-lg shadow-sm bg-gray-50">
        <Image src={preview} alt="Farmland preview" width={400} height={300} className="w-full h-auto rounded-md object-cover" />
        <div className="mt-2 text-sm text-muted-foreground">
          ✓ {fileName} ({fileSize})
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleRemove}
          className="absolute top-2 right-2 bg-background/50 hover:bg-background"
        >
          <X className="h-4 w-4" />
          <span className="sr-only">Remove image</span>
        </Button>
      </div>
    );
  }

  return (
    <div
      {...getRootProps()}
      className={`flex flex-col items-center justify-center w-full p-12 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${
        isDragActive ? "border-primary bg-primary/10" : "border-gray-300 hover:border-primary/50"
      }`}
    >
      <input {...getInputProps()} />
      <UploadCloud className="h-16 w-16 text-gray-400 mb-4" />
      <p className="text-lg font-semibold">
        {isDragActive ? "Drop the image here..." : "Upload Farmland Image"}
      </p>
      <p className="text-muted-foreground">Drag & Drop or Click to Upload</p>
      <p className="text-xs text-muted-foreground mt-2">Supports: JPG, PNG, WebP (max 10MB)</p>
    </div>
  );
}

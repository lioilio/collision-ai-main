import { useState, useCallback } from "react";
import { Upload, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface UploadZoneProps {
  onImageSelect: (file: File) => void;
  selectedImage: File | null;
  onClear: () => void;
}

export const UploadZone = ({ onImageSelect, selectedImage, onClear }: UploadZoneProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      onImageSelect(file);
    }
  }, [onImageSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  }, [onImageSelect]);

  return (
    <div className="w-full">
      {!selectedImage ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300",
            isDragging
              ? "border-primary bg-medical-light scale-[1.02]"
              : "border-border hover:border-primary/50 hover:bg-medical-light/50"
          )}
        >
          <input
            type="file"
            accept="image/*"
            onChange={handleFileInput}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <Upload className="w-8 h-8 text-primary" />
              </div>
              <div>
                <p className="text-lg font-semibold text-foreground mb-1">
                  Upload Gambar Slide Darah
                </p>
                <p className="text-sm text-muted-foreground">
                  Drag & drop atau klik untuk memilih file
                </p>
                <p className="text-xs text-muted-foreground mt-2">
                  Format: JPG, PNG (Max 10MB)
                </p>
              </div>
            </div>
          </label>
        </div>
      ) : (
        <div className="relative rounded-xl overflow-hidden border-2 border-primary bg-card shadow-card">
          <img
            src={URL.createObjectURL(selectedImage)}
            alt="Uploaded preview"
            className="w-full h-auto max-h-96 object-contain"
          />
          <Button
            onClick={onClear}
            size="icon"
            variant="destructive"
            className="absolute top-4 right-4 rounded-full shadow-lg"
          >
            <X className="w-4 h-4" />
          </Button>
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
            <p className="text-white text-sm font-medium truncate">
              {selectedImage.name}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

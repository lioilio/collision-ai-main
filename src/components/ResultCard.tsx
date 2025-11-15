import { CheckCircle2, AlertCircle, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ResultCardProps {
  result: string | null;
  confidence?: number;
  isLoading: boolean;
}

export const ResultCard = ({ result, confidence, isLoading }: ResultCardProps) => {
  if (isLoading) {
    return (
      <Card className="border-primary/20 shadow-medical">
        <CardContent className="pt-6">
          <div className="flex flex-col items-center justify-center py-12 gap-4">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center animate-pulse">
              <Activity className="w-8 h-8 text-primary animate-spin" />
            </div>
            <div className="text-center">
              <p className="text-lg font-semibold text-foreground mb-2">
                Menganalisis Gambar...
              </p>
              <p className="text-sm text-muted-foreground">
                Sistem sedang memproses gambar Anda
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return (
      <Card className="border-dashed border-2 border-border">
        <CardContent className="pt-6">
          <div className="flex flex-col items-center justify-center py-12 gap-4 text-center">
            <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
              <Activity className="w-8 h-8 text-muted-foreground" />
            </div>
            <div>
              <p className="text-lg font-semibold text-foreground mb-2">
                Menunggu Analisis
              </p>
              <p className="text-sm text-muted-foreground">
                Upload gambar dan klik "Deteksi Sekarang" untuk melihat hasil
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getResultIcon = () => {
    if (result.toLowerCase().includes("normal")) {
      return <CheckCircle2 className="w-8 h-8 text-success" />;
    }
    return <AlertCircle className="w-8 h-8 text-warning" />;
  };

  const getResultColor = () => {
    if (result.toLowerCase().includes("normal")) {
      return "bg-success/10 border-success/20";
    }
    return "bg-warning/10 border-warning/20";
  };

  return (
    <Card className={`border-2 shadow-medical ${getResultColor()}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {getResultIcon()}
          <span>Hasil Deteksi</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-card border border-border">
            <p className="text-sm text-muted-foreground mb-2">Klasifikasi:</p>
            <p className="text-xl font-bold text-foreground">{result}</p>
          </div>
          
          {confidence !== undefined && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Tingkat Keyakinan:</span>
                <Badge variant="secondary">{confidence}%</Badge>
              </div>
              <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-500"
                  style={{ width: `${confidence}%` }}
                />
              </div>
            </div>
          )}

          <div className="pt-4 border-t border-border">
            <p className="text-xs text-muted-foreground">
              ⚠️ Disclaimer: Hasil ini adalah prediksi model AI dan harus dikonfirmasi oleh tenaga medis profesional.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

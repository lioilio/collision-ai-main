import { useState } from "react";
import { Microscope, Activity, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UploadZone } from "@/components/UploadZone";
import { ResultCard } from "@/components/ResultCard";
import { ChatBot } from "@/components/ChatBot";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleDetect = async () => {
    if (!selectedImage) {
      toast({
        title: "Tidak ada gambar",
        description: "Silakan upload gambar terlebih dahulu",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setResult(null);

    try {
      // Import API function
      const { predictImage } = await import("@/lib/api");
      
      // Call Flask API
      const response = await predictImage(selectedImage);

      setResult(response.result);
      setConfidence(response.confidence);

      toast({
        title: "Analisis Selesai",
        description: "Hasil deteksi telah tersedia",
      });
    } catch (error) {
      console.error("Prediction error:", error);
      toast({
        title: "Terjadi Kesalahan",
        description: error instanceof Error ? error.message : "Gagal melakukan deteksi. Pastikan Flask API sudah berjalan.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setResult(null);
    setConfidence(undefined);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-medical-light/30 to-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/80 backdrop-blur-sm sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-medical">
              <Microscope className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">LeukemiaDetect</h1>
              <p className="text-xs text-muted-foreground">AI-Powered Detection System</p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-12 text-center">
        <div className="max-w-3xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium">
            <Shield className="w-4 h-4" />
            Teknologi AI Terpercaya
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
            Deteksi Leukemia dengan
            <span className="block bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Artificial Intelligence
            </span>
          </h2>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Upload gambar slide darah mikroskopis untuk mendapatkan analisis cepat dan akurat menggunakan teknologi machine learning terkini.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="container mx-auto px-4 pb-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Upload Section */}
            <div className="space-y-6">
              <div className="space-y-2">
                <h3 className="text-2xl font-bold text-foreground flex items-center gap-2">
                  <Activity className="w-6 h-6 text-primary" />
                  Upload Gambar
                </h3>
                <p className="text-sm text-muted-foreground">
                  Pilih gambar slide darah yang ingin Anda analisis
                </p>
              </div>

              <UploadZone
                onImageSelect={setSelectedImage}
                selectedImage={selectedImage}
                onClear={handleClear}
              />

              <Button
                onClick={handleDetect}
                disabled={!selectedImage || isLoading}
                className="w-full h-14 text-lg font-semibold shadow-medical hover:shadow-lg transition-all duration-300"
                size="lg"
              >
                {isLoading ? (
                  <>
                    <Activity className="w-5 h-5 mr-2 animate-spin" />
                    Menganalisis...
                  </>
                ) : (
                  <>
                    <Microscope className="w-5 h-5 mr-2" />
                    Deteksi Sekarang
                  </>
                )}
              </Button>
            </div>

            {/* Result Section */}
            <div className="space-y-6">
              <div className="space-y-2">
                <h3 className="text-2xl font-bold text-foreground flex items-center gap-2">
                  <Activity className="w-6 h-6 text-secondary" />
                  Hasil Analisis
                </h3>
                <p className="text-sm text-muted-foreground">
                  Klasifikasi dan tingkat keyakinan model AI
                </p>
              </div>

              <ResultCard result={result} confidence={confidence} isLoading={isLoading} />
            </div>
          </div>
        </div>
      </section>

      {/* Info Cards */}
      <section className="container mx-auto px-4 pb-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-card border border-border shadow-card hover:shadow-medical transition-all duration-300">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Microscope className="w-6 h-6 text-primary" />
              </div>
              <h4 className="text-lg font-semibold text-foreground mb-2">Akurat</h4>
              <p className="text-sm text-muted-foreground">
                Model AI terlatih dengan ribuan sampel untuk hasil yang presisi
              </p>
            </div>

            <div className="p-6 rounded-xl bg-card border border-border shadow-card hover:shadow-medical transition-all duration-300">
              <div className="w-12 h-12 rounded-lg bg-secondary/10 flex items-center justify-center mb-4">
                <Activity className="w-6 h-6 text-secondary" />
              </div>
              <h4 className="text-lg font-semibold text-foreground mb-2">Cepat</h4>
              <p className="text-sm text-muted-foreground">
                Dapatkan hasil analisis dalam hitungan detik
              </p>
            </div>

            <div className="p-6 rounded-xl bg-card border border-border shadow-card hover:shadow-medical transition-all duration-300">
              <div className="w-12 h-12 rounded-lg bg-success/10 flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-success" />
              </div>
              <h4 className="text-lg font-semibold text-foreground mb-2">Aman</h4>
              <p className="text-sm text-muted-foreground">
                Data Anda diproses dengan sistem keamanan terjamin
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8">
          <p className="text-center text-sm text-muted-foreground">
            © 2025 LeukemiaDetect. Sistem deteksi ini adalah alat bantu dan bukan pengganti diagnosis medis profesional.
          </p>
        </div>
      </footer>

      {/* Chatbot - hanya muncul jika ada hasil analisis */}
      {result && (
        <ChatBot analysisResult={result} confidence={confidence} />
      )}
    </div>
  );
};

export default Index;

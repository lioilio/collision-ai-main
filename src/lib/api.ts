// Konfigurasi API endpoint
// PENTING: Ubah URL ini sesuai dengan lokasi Flask API Anda

// Untuk development lokal
export const API_BASE_URL = "http://localhost:5000";

// Untuk production, uncomment dan ganti dengan URL Flask API Anda:
// export const API_BASE_URL = "https://your-flask-api.com";

export interface PredictionResponse {
  result: string;
  confidence: number;
  all_probabilities?: {
    [key: string]: number;
  };
}

export interface ApiError {
  error: string;
  message: string;
}

/**
 * Kirim gambar ke Flask API untuk prediksi
 */
export const predictImage = async (imageFile: File): Promise<PredictionResponse> => {
  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      body: formData,
      // Tidak perlu set Content-Type, browser akan set otomatis untuk FormData
    });

    if (!response.ok) {
      const errorData: ApiError = await response.json();
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data: PredictionResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      // Network error atau error dari server
      if (error.message.includes("Failed to fetch")) {
        throw new Error(
          "Tidak dapat terhubung ke server. Pastikan Flask API sudah berjalan di " + API_BASE_URL
        );
      }
      throw error;
    }
    throw new Error("Terjadi kesalahan yang tidak diketahui");
  }
};

/**
 * Check API health
 */
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: "GET",
    });
    return response.ok;
  } catch (error) {
    return false;
  }
};

/**
 * Get model information
 */
export const getModelInfo = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/model-info`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    throw new Error("Gagal mendapatkan informasi model");
  }
};

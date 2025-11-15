# Leukemia Detection Backend - Flask API

Backend Flask untuk sistem deteksi leukemia menggunakan model TensorFlow Lite.

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- Model TFLite (`leukemia_model.tflite`)

## 🚀 Setup dan Instalasi

### 1. Buat Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Aktifkan Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Letakkan Model TFLite

Letakkan file model Anda di folder `model/`:

```
backend/
├── model/
│   └── leukemia_model.tflite  <-- Letakkan model Anda di sini
├── app.py
└── requirements.txt
```

### 5. Jalankan Server

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

## 🔧 Konfigurasi Model

### Sesuaikan Preprocessing

Di file `app.py`, sesuaikan fungsi `preprocess_image()` dengan cara model Anda dilatih:

```python
# INPUT_SIZE - Sesuaikan dengan input shape model
INPUT_SIZE = (224, 224)  # Ubah jika model Anda menggunakan ukuran lain

# CLASS_LABELS - Sesuaikan urutan class dengan model
CLASS_LABELS = [
    "Leukemia Akut Limfoblastik (ALL)",
    "Leukemia Akut Mieloblastik (AML)", 
    "Sel Normal (Normal Cells)"
]

# Normalisasi - Pilih sesuai training model
# Option 1: Normalisasi 0-1 (paling umum)
img_array = img_array / 255.0

# Option 2: Normalisasi -1 sampai 1
# img_array = (img_array / 127.5) - 1.0

# Option 3: ImageNet normalization
# mean = np.array([0.485, 0.456, 0.406])
# std = np.array([0.229, 0.224, 0.225])
# img_array = (img_array / 255.0 - mean) / std
```

## 📡 API Endpoints

### 1. Health Check
```
GET /
Response: { "status": "online", "model_loaded": true }
```

### 2. Predict
```
POST /predict
Content-Type: multipart/form-data
Body: image (file)

Response:
{
  "result": "Leukemia Akut Limfoblastik (ALL)",
  "confidence": 92.5,
  "all_probabilities": {
    "ALL": 92.5,
    "AML": 5.2,
    "Normal": 2.3
  }
}
```

### 3. Model Info
```
GET /model-info
Response: { "input_shape": [1, 224, 224, 3], "classes": [...] }
```

## 🧪 Testing API

### Menggunakan cURL:

```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@path/to/your/image.jpg"
```

### Menggunakan Python:

```python
import requests

url = "http://localhost:5000/predict"
files = {"image": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## ⚠️ Troubleshooting

### Model tidak ditemukan
```
Error: Model not loaded
```
**Solusi:** Pastikan file `model/leukemia_model.tflite` ada dan path-nya benar.

### Error input shape
```
Error: Cannot set tensor: Dimension mismatch
```
**Solusi:** Sesuaikan `INPUT_SIZE` di `app.py` dengan input shape model Anda.

### CORS Error dari frontend
```
Error: CORS policy blocked
```
**Solusi:** Pastikan `flask-cors` sudah terinstall dan `CORS(app)` ada di `app.py`.

## 📦 Struktur Folder

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation (file ini)
├── model/
│   └── leukemia_model.tflite  # Model TFLite Anda
├── static/
│   └── uploads/          # Folder untuk uploads (opsional)
└── venv/                 # Virtual environment
```

## 🔒 Production Notes

Untuk production deployment:

1. **Ganti `debug=True` menjadi `debug=False`**
2. **Gunakan production WSGI server** (Gunicorn/uWSGI)
3. **Setup HTTPS** untuk keamanan
4. **Batasi CORS** hanya ke domain frontend Anda
5. **Add rate limiting** untuk mencegah abuse

Contoh dengan Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

© 2025 LeukemiaDetect

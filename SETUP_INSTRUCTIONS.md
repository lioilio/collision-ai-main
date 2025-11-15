# 🔬 Setup Instructions - Leukemia Detection

Panduan lengkap untuk menjalankan aplikasi deteksi leukemia dengan Flask backend dan React frontend.

## 📁 Struktur Project

```
leukemia-detection/
├── backend/                    # Flask API
│   ├── app.py                 # Main Flask app
│   ├── requirements.txt       # Python dependencies
│   ├── README.md             # Backend documentation
│   └── model/
│       └── leukemia_model.tflite  # Model TFLite Anda
│
└── [Lovable React Project]/   # Frontend (project Lovable ini)
    ├── src/
    │   ├── pages/Index.tsx    # Main page
    │   ├── components/        # UI components
    │   └── lib/api.ts         # API client
    └── ...
```

## 🚀 Cara Setup dan Menjalankan

### STEP 1: Setup Backend Flask

1. **Copy folder `backend/` ke local computer Anda**

2. **Buka terminal di folder backend:**
   ```bash
   cd backend
   ```

3. **Buat virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Aktifkan virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **PENTING: Letakkan model TFLite Anda**
   
   Copy file `leukemia_model.tflite` Anda ke folder `backend/model/`:
   ```
   backend/
   └── model/
       └── leukemia_model.tflite  <-- Letakkan di sini
   ```

7. **SESUAIKAN konfigurasi model di `app.py`:**
   
   Buka `backend/app.py` dan edit bagian berikut sesuai model Anda:
   
   ```python
   # Baris 25-29: Sesuaikan class labels
   CLASS_LABELS = [
       "Leukemia Akut Limfoblastik (ALL)",
       "Leukemia Akut Mieloblastik (AML)",
       "Sel Normal (Normal Cells)"
   ]
   
   # Baris 32: Sesuaikan input size
   INPUT_SIZE = (224, 224)  # Ubah sesuai model Anda
   
   # Baris 52-56: Pilih normalisasi yang sesuai
   # Option 1: 0-1 (paling umum)
   img_array = img_array / 255.0
   
   # Option 2: -1 sampai 1
   # img_array = (img_array / 127.5) - 1.0
   
   # Option 3: ImageNet
   # mean = np.array([0.485, 0.456, 0.406])
   # std = np.array([0.229, 0.224, 0.225])
   # img_array = (img_array / 255.0 - mean) / std
   ```

8. **Jalankan Flask server:**
   ```bash
   python app.py
   ```
   
   ✅ Server akan berjalan di `http://localhost:5000`
   
   Output yang benar:
   ```
   ==================================================
   🔬 Leukemia Detection API
   ==================================================
   📁 Model path: model/leukemia_model.tflite
   ✓ Model loaded successfully
   ✓ Server running on http://localhost:5000
   ✓ CORS enabled for React frontend
   ==================================================
   ```

### STEP 2: Jalankan Frontend React (Lovable)

Frontend sudah otomatis berjalan di Lovable preview!

Jika ingin test di local:

1. **Pastikan Flask API sudah running** (dari Step 1)

2. **Frontend akan otomatis connect ke** `http://localhost:5000`
   
   Konfigurasi ada di `src/lib/api.ts`:
   ```typescript
   export const API_BASE_URL = "http://localhost:5000";
   ```

3. **Test aplikasi:**
   - Upload gambar slide darah
   - Klik "Deteksi Sekarang"
   - Lihat hasil analisis

## 🧪 Testing API

### Test dengan cURL:

```bash
curl http://localhost:5000/
# Response: {"status":"online","model_loaded":true}

curl -X POST http://localhost:5000/predict \
  -F "image=@/path/to/test-image.jpg"
```

### Test dengan Python:

```python
import requests

# Health check
response = requests.get("http://localhost:5000/")
print(response.json())

# Predict
files = {"image": open("test-image.jpg", "rb")}
response = requests.post("http://localhost:5000/predict", files=files)
print(response.json())
```

## ⚙️ Konfigurasi untuk Production

### Untuk Deploy Flask API ke Server:

1. **Edit `src/lib/api.ts`:**
   ```typescript
   // Uncomment dan ganti dengan URL production
   export const API_BASE_URL = "https://your-flask-api.com";
   ```

2. **Deploy Flask API** (pilih salah satu):
   - **Railway**: https://railway.app/
   - **Heroku**: https://heroku.com/
   - **DigitalOcean App Platform**: https://www.digitalocean.com/products/app-platform
   - **AWS EC2 / Google Cloud Run**

3. **Update CORS di Flask** untuk security:
   ```python
   # Di app.py, ganti:
   CORS(app)
   
   # Dengan:
   CORS(app, origins=["https://your-frontend-domain.com"])
   ```

## 🔧 Troubleshooting

### ❌ Error: "Tidak dapat terhubung ke server"

**Penyebab:** Flask API tidak running atau wrong URL

**Solusi:**
1. Pastikan Flask API running di `http://localhost:5000`
2. Check terminal Flask ada error atau tidak
3. Test dengan `curl http://localhost:5000/`

### ❌ Error: "Model not loaded"

**Penyebab:** File model tidak ditemukan

**Solusi:**
1. Pastikan file `leukemia_model.tflite` ada di `backend/model/`
2. Check path di `app.py` line 12: `MODEL_PATH = "model/leukemia_model.tflite"`

### ❌ Error: "Cannot set tensor: Dimension mismatch"

**Penyebab:** Input size tidak sesuai dengan model

**Solusi:**
1. Check input shape model Anda
2. Update `INPUT_SIZE` di `app.py` line 32
3. Lihat di terminal Flask output: `Input shape: [1, 224, 224, 3]`

### ❌ Error: CORS blocked

**Penyebab:** CORS tidak enabled di Flask

**Solusi:**
1. Pastikan `flask-cors` terinstall: `pip install flask-cors`
2. Pastikan ada `CORS(app)` di `app.py`
3. Restart Flask server

### ❌ Hasil prediksi tidak akurat

**Penyebab:** Preprocessing tidak sesuai dengan training model

**Solusi:**
1. Review bagaimana model Anda dilatih
2. Sesuaikan normalisasi di fungsi `preprocess_image()`
3. Pastikan `CLASS_LABELS` urutannya sesuai dengan model

## 📚 Resources

- Flask Documentation: https://flask.palletsprojects.com/
- TensorFlow Lite: https://www.tensorflow.org/lite
- React + Flask Tutorial: https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project

## 💡 Tips

1. **Development:** Jalankan Flask di port 5000, React otomatis connect
2. **Production:** Deploy Flask terpisah, update `API_BASE_URL`
3. **Testing:** Gunakan Postman atau cURL untuk test API
4. **Debugging:** Check console browser (F12) dan terminal Flask untuk errors
5. **Performance:** Untuk produksi, gunakan Gunicorn sebagai WSGI server

## 📞 Need Help?

Jika ada masalah:
1. Check terminal Flask untuk error messages
2. Check browser console (F12) untuk frontend errors
3. Pastikan semua dependencies terinstall
4. Review README.md di folder backend

---

**IMPORTANT:** Model `.tflite` TIDAK termasuk dalam project ini. Anda harus menggunakan model Anda sendiri!

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS untuk frontend React

# ========================================
# KONFIGURASI GEMINI API
# ========================================
# PASTE GEMINI API KEY ANDA DI SINI
GEMINI_API_KEY = "AIzaSyCmcz23klweFQZJTokJXbdMJXR7MyqT8-o"

# Konfigurasi Gemini
if GEMINI_API_KEY and GEMINI_API_KEY != "PASTE_YOUR_GEMINI_API_KEY_HERE":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✓ Gemini AI configured successfully")
    except Exception as e:
        print(f"✗ Error configuring Gemini: {e}")
        model = None
else:
    print("⚠ Gemini API Key not configured. Chatbot will not work.")
    model = None

# ========================================
# KONFIGURASI MODEL LEUKEMIA
# ========================================
# Path ke model .tflite
MODEL_PATH = "model/model4.tflite"

# Load model TFLite
try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    interpreter = None

# Dapatkan input dan output details
if interpreter:
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(f"Input shape: {input_details[0]['shape']}")
    print(f"Output shape: {output_details[0]['shape']}")

# Konfigurasi class labels
CLASS_LABELS = [
    "EarlyPreB",
    "PreB",
    "ProB",
    "benign"
]

# Deskripsi untuk setiap class (untuk chatbot)
CLASS_DESCRIPTIONS = {
    "EarlyPreB": "Early Pre-B Cell Leukemia - Stadium awal dari leukemia limfoblastik akut sel B",
    "PreB": "Pre-B Cell Leukemia - Stadium Pre-B dari leukemia limfoblastik akut sel B",
    "ProB": "Pro-B Cell Leukemia - Stadium Pro-B dari leukemia limfoblastik akut sel B",
    "benign": "Benign/Normal - Sel darah yang normal dan sehat"
}

# Input size berdasarkan model
INPUT_SIZE = (224, 224)


def preprocess_image(image_file):
    """
    Preprocess gambar sesuai dengan requirement model.
    Model menggunakan float32 input, normalisasi 0–1, dan ukuran 224x224.
    """
    img = Image.open(io.BytesIO(image_file.read()))

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = img.resize(INPUT_SIZE)
    img_array = np.array(img, dtype=np.float32) / 255.0  # Normalisasi 0–1
    img_array = np.expand_dims(img_array, axis=0)  # Tambah batch dimensi

    return img_array


# ========================================
# ENDPOINTS
# ========================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'message': 'Leukemia Detection API is running',
        'model_loaded': interpreter is not None,
        'chatbot_enabled': model is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if interpreter is None:
            return jsonify({'error': 'Model not loaded'}), 500

        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        img_array = preprocess_image(file)

        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        predictions = output_data[0]

        predicted_idx = np.argmax(predictions)
        predicted_class = CLASS_LABELS[predicted_idx]
        confidence = float(predictions[predicted_idx] * 100)

        all_probabilities = {
            CLASS_LABELS[i]: float(predictions[i] * 100)
            for i in range(len(CLASS_LABELS))
        }

        print(f"Prediction: {predicted_class} ({confidence:.2f}%)")

        return jsonify({
            'result': predicted_class,
            'confidence': round(confidence, 2),
            'all_probabilities': all_probabilities
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint chatbot dengan Gemini API untuk konsultasi hasil analisis
    """
    try:
        if model is None:
            return jsonify({
                'error': 'Chatbot not configured',
                'message': 'Gemini API key belum dikonfigurasi. Silakan tambahkan GEMINI_API_KEY di app.py'
            }), 500

        data = request.get_json()
        user_message = data.get('message', '')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Ambil context hasil analisis
        result = context.get('result', 'tidak diketahui')
        confidence = context.get('confidence', 0)
        
        # Dapatkan deskripsi lengkap dari class
        result_description = CLASS_DESCRIPTIONS.get(result, result)
        
        # Buat system prompt dengan context hasil analisis
        system_prompt = f"""Anda adalah asisten medis AI yang ahli dalam menjelaskan hasil analisis leukemia dari gambar sel darah.

HASIL ANALISIS SAAT INI:
- Diagnosis: {result}
- Deskripsi: {result_description}
- Tingkat Confidence: {confidence:.1f}%

KLASIFIKASI YANG TERSEDIA:
{chr(10).join([f"- {label}: {CLASS_DESCRIPTIONS[label]}" for label in CLASS_LABELS])}

TUGAS ANDA:
1. Jelaskan hasil diagnosis dengan bahasa Indonesia yang mudah dipahami oleh pasien/keluarga
2. Berikan informasi edukatif tentang jenis leukemia atau kondisi sel yang terdeteksi
3. Jelaskan apa arti dari stadium EarlyPreB, PreB, ProB jika ditanyakan
4. Sarankan langkah-langkah yang harus dilakukan (konsultasi hematologi, tes lanjutan, dll)
5. SANGAT PENTING: Selalu ingatkan bahwa ini adalah screening awal dan diagnosis final harus oleh dokter spesialis
6. Jawab dengan empati, profesional, dan tidak menakut-nakuti
7. Jika confidence rendah (<70%), jelaskan bahwa hasil perlu konfirmasi lebih lanjut
8. Berikan informasi faktual berdasarkan pengetahuan medis tentang ALL (Acute Lymphoblastic Leukemia)

CATATAN:
- Jangan memberikan diagnosis final atau pengobatan spesifik
- Fokus pada edukasi dan arahan ke profesional medis
- Gunakan bahasa yang hangat dan supportif"""

        # Gabungkan system prompt dengan user message
        full_prompt = f"{system_prompt}\n\nPertanyaan user: {user_message}\n\nJawaban (dalam Bahasa Indonesia, maksimal 200 kata):"
        
        # Generate response dari Gemini
        response = model.generate_content(full_prompt)
        
        print(f"Chat - User: {user_message[:50]}... | AI Response: {response.text[:50]}...")
        
        return jsonify({
            'response': response.text,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({
            'error': 'Chat error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500


@app.route('/model-info', methods=['GET'])
def model_info():
    if interpreter is None:
        return jsonify({'error': 'Model not loaded'}), 500

    return jsonify({
        'input_shape': input_details[0]['shape'].tolist(),
        'output_shape': output_details[0]['shape'].tolist(),
        'input_dtype': str(input_details[0]['dtype']),
        'output_dtype': str(output_details[0]['dtype']),
        'classes': CLASS_LABELS,
        'class_descriptions': CLASS_DESCRIPTIONS,
        'input_size': INPUT_SIZE
    })


if __name__ == '__main__':
    os.makedirs('model', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)

    print("\n" + "=" * 60)
    print("🔬 Leukemia Detection API with AI Chatbot")
    print("=" * 60)
    print(f"📁 Model path: {MODEL_PATH}")
    print(f"🤖 Chatbot: {'✓ Enabled' if model else '✗ Disabled (API key not set)'}")
    print(f"✓ Server running on http://localhost:5000")
    print(f"✓ CORS enabled for React frontend")
    print("\n📌 Available Endpoints:")
    print("  GET  / - Health check")
    print("  POST /predict - Image classification")
    print("  POST /chat - AI chatbot consultation")
    print("  GET  /model-info - Model information")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)

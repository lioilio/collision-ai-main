from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)  # Enable CORS untuk frontend React

# Path ke model .tflite
MODEL_PATH = "model/leukemia_model.tflite"

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

# Konfigurasi class labels - SESUAIKAN DENGAN MODEL ANDA
CLASS_LABELS = [
    "Leukemia Akut Limfoblastik (ALL)",
    "Leukemia Akut Mieloblastik (AML)",
    "Sel Normal (Normal Cells)"
]

# Konfigurasi preprocessing - SESUAIKAN DENGAN MODEL ANDA
INPUT_SIZE = (224, 224)  # Sesuaikan dengan input shape model Anda


def preprocess_image(image_file):
    """
    Preprocess gambar sesuai dengan requirement model.
    PENTING: Sesuaikan preprocessing ini dengan cara model Anda dilatih!
    """
    # Baca gambar
    img = Image.open(io.BytesIO(image_file.read()))
    
    # Convert ke RGB jika perlu
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize ke ukuran yang sesuai
    img = img.resize(INPUT_SIZE)
    
    # Convert ke numpy array
    img_array = np.array(img, dtype=np.float32)
    
    # Normalisasi - SESUAIKAN INI!
    # Jika model Anda menggunakan normalisasi 0-1:
    img_array = img_array / 255.0
    
    # Jika model Anda menggunakan normalisasi -1 sampai 1:
    # img_array = (img_array / 127.5) - 1.0
    
    # Jika model Anda menggunakan ImageNet normalization:
    # mean = np.array([0.485, 0.456, 0.406])
    # std = np.array([0.229, 0.224, 0.225])
    # img_array = (img_array / 255.0 - mean) / std
    
    # Expand dimensions untuk batch
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Leukemia Detection API is running',
        'model_loaded': interpreter is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint untuk prediksi gambar leukemia.
    
    Expected request:
    - Method: POST
    - Content-Type: multipart/form-data
    - Field: image (file)
    
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
    """
    try:
        # Validasi model
        if interpreter is None:
            return jsonify({
                'error': 'Model not loaded',
                'message': 'TFLite model belum berhasil dimuat'
            }), 500
        
        # Validasi request
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image provided',
                'message': 'Tidak ada gambar yang dikirim'
            }), 400
        
        file = request.files['image']
        
        # Validasi file
        if file.filename == '':
            return jsonify({
                'error': 'Empty filename',
                'message': 'Nama file kosong'
            }), 400
        
        # Preprocess gambar
        img_array = preprocess_image(file)
        
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], img_array)
        
        # Run inference
        interpreter.invoke()
        
        # Get output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # Get predictions
        predictions = output_data[0]  # Remove batch dimension
        
        # Softmax jika belum (beberapa model sudah include softmax)
        # Uncomment jika model Anda belum menggunakan softmax:
        # exp_predictions = np.exp(predictions - np.max(predictions))
        # predictions = exp_predictions / exp_predictions.sum()
        
        # Get predicted class
        predicted_idx = np.argmax(predictions)
        predicted_class = CLASS_LABELS[predicted_idx]
        confidence = float(predictions[predicted_idx] * 100)
        
        # Get all probabilities
        all_probabilities = {
            CLASS_LABELS[i]: float(predictions[i] * 100) 
            for i in range(len(CLASS_LABELS))
        }
        
        # Log prediction
        print(f"Prediction: {predicted_class} ({confidence:.2f}%)")
        
        return jsonify({
            'result': predicted_class,
            'confidence': round(confidence, 2),
            'all_probabilities': all_probabilities
        })
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    if interpreter is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'input_shape': input_details[0]['shape'].tolist(),
        'output_shape': output_details[0]['shape'].tolist(),
        'input_dtype': str(input_details[0]['dtype']),
        'output_dtype': str(output_details[0]['dtype']),
        'classes': CLASS_LABELS,
        'input_size': INPUT_SIZE
    })


if __name__ == '__main__':
    # Pastikan folder model dan uploads ada
    os.makedirs('model', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
    # Run Flask app
    print("\n" + "="*50)
    print("🔬 Leukemia Detection API")
    print("="*50)
    print(f"📁 Model path: {MODEL_PATH}")
    print(f"✓ Server running on http://localhost:5000")
    print(f"✓ CORS enabled for React frontend")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

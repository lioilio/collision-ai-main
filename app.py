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

# Konfigurasi class labels (ISI SESUAI MODEL ANDA)
CLASS_LABELS = [
    "EarlyPreB",
    "PreB",
    "ProB",
    "benign"
]
# Input size berdasarkan model
INPUT_SIZE = (224, 224)


def preprocess_image(image_file):
    """
    Preprocess gambar sesuai dengan requirement model.
    Model kamu menggunakan float32 input, normalisasi 0–1, dan ukuran 224x224.
    """
    img = Image.open(io.BytesIO(image_file.read()))

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = img.resize(INPUT_SIZE)
    img_array = np.array(img, dtype=np.float32) / 255.0  # Normalisasi 0–1
    img_array = np.expand_dims(img_array, axis=0)  # Tambah batch dimensi

    return img_array


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'message': 'Leukemia Detection API is running',
        'model_loaded': interpreter is not None
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
        'input_size': INPUT_SIZE
    })


if __name__ == '__main__':
    os.makedirs('model', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)

    print("\n" + "=" * 50)
    print("🔬 Leukemia Detection API")
    print("=" * 50)
    print(f"📁 Model path: {MODEL_PATH}")
    print(f"✓ Server running on http://localhost:5000")
    print(f"✓ CORS enabled for React frontend")
    print("=" * 50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
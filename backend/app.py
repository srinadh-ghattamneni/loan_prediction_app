from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import joblib
import os

# Set Flask app with correct paths
app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")
CORS(app)

# Load the trained model and scaler
model = joblib.load("loan_default_model.pkl")
scaler = joblib.load("scaler.pkl")

# Serve index.html from frontend folder
@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

# Serve static files (CSS, JS)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("../frontend/static", filename)

# Loan prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json.get("features")
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Convert input into numpy array and scale it
        data = np.array(data).reshape(1, -1)
        data_scaled = scaler.transform(data)

        # Predict loan approval
        prediction = model.predict(data_scaled)

        return jsonify({"loan_approved": bool(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

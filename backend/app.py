from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib
import os

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")
CORS(app)

# Load trained model and scaler
model = joblib.load("loan_default_model.pkl")
scaler = joblib.load("scaler.pkl")

# Feature names (MUST match training data order)
feature_names = [
    "person_age", "person_gender", "person_education", "person_income",
    "person_emp_exp", "person_home_ownership", "loan_amnt", "loan_intent",
    "loan_int_rate", "loan_percent_income", "cb_person_cred_hist_length",
    "credit_score", "previous_loan_defaults_on_file"
]

# Categorical encoding mappings
gender_map = {"male": 0, "female": 1}
education_map = {"High School": 0, "Bachelor": 1, "Master": 2}
home_ownership_map = {"RENT": 0, "OWN": 1, "MORTGAGE": 2}
loan_intent_map = {"PERSONAL": 0, "EDUCATION": 1, "MEDICAL": 2}
default_map = {"No": 0, "Yes": 1}

def preprocess_input(data):
    """Convert categorical values, ensure feature order, and create a DataFrame."""
    try:
        # Convert input to dictionary with correct feature order
        input_dict = dict(zip(feature_names, data))

        # Convert categorical features to numerical values
        input_dict["person_gender"] = gender_map.get(str(input_dict["person_gender"]).lower(), 0)
        input_dict["person_education"] = education_map.get(str(input_dict["person_education"]), 0)
        input_dict["person_home_ownership"] = home_ownership_map.get(str(input_dict["person_home_ownership"]), 0)
        input_dict["loan_intent"] = loan_intent_map.get(str(input_dict["loan_intent"]), 0)
        input_dict["previous_loan_defaults_on_file"] = default_map.get(str(input_dict["previous_loan_defaults_on_file"]), 0)

        # Convert to DataFrame with correct feature names
        input_df = pd.DataFrame([input_dict], columns=feature_names)

        return input_df
    except Exception as e:
        raise ValueError(f"Preprocessing error: {str(e)}")

# Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

# Serve static files
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("../frontend/static", filename)

# Loan prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.json.get("features")
        if not data or len(data) != len(feature_names):
            return jsonify({"error": "Invalid input data"}), 400

        # Preprocess input
        input_df = preprocess_input(data)

        # Scale input data **(Fix Warning: Pass DataFrame)**
        data_scaled_df = pd.DataFrame(scaler.transform(input_df), columns=feature_names)

        # Predict loan approval **(Fix Warning: Pass DataFrame)**
        prediction = model.predict(data_scaled_df)

        return jsonify({"loan_approved": bool(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

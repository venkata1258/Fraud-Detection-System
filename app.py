from flask import Flask, request, jsonify
import mysql.connector
import pickle
import re
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

# Download stopwords before usage
nltk.download('stopwords')

# Load NLP Model & Vectorizer (Handle File Errors)
try:
    model = pickle.load(open("fraud_sms_model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    vectorizer = None

# MySQL Database Connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="186707",
            database="fraud_detection"
        )
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# Preprocess function for text messages
def clean_text(text):
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english'))
    return text

# ✅ Homepage Route (Fixes 405 Error)
@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"message": "Welcome to the Fraud Detection System!"})

# 🛑 API 1: Detect Fraud in SMS/Email (NLP Model)
@app.route('/detect_fraud', methods=['POST'])
def detect_fraud():
    if not model or not vectorizer:
        return jsonify({"error": "Model is not available"}), 500

    data = request.json or request.form  # Support both JSON & form-data
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    message_cleaned = clean_text(message)
    message_vectorized = vectorizer.transform([message_cleaned]).toarray()
    
    prediction = model.predict(message_vectorized)
    result = "Fraud" if prediction[0] == 1 else "Safe"
    
    return jsonify({"message": message, "result": result})

# 📢 API 2: Report Fraud Cases (Store in MySQL)
@app.route('/report_fraud', methods=['POST'])
def report_fraud():
    data = request.json or request.form  # Support both JSON & form-data
    phone = data.get("phone")
    email = data.get("email")
    message = data.get("message")
    fraud_type = data.get("fraud_type")

    if not (phone and email and message and fraud_type):
        return jsonify({"error": "All fields are required"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor()
        sql = "INSERT INTO fraud_reports (phone, email, message, fraud_type) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (phone, email, message, fraud_type))
        db.commit()
        return jsonify({"message": "Fraud report submitted successfully!"})
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        db.close()

# 📜 API 3: Fetch All Fraud Reports (For Admin)
@app.route('/get_reports', methods=['GET'])
def get_reports():
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)  # Return results as JSON objects
        cursor.execute("SELECT * FROM fraud_reports")
        reports = cursor.fetchall()
        return jsonify(reports)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

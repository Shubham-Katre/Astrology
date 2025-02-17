from flask import Flask, request, jsonify
from service import calculate_dashboard
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="https://horoscopex-1.onrender.com")

@app.route("/planets", methods=['POST'])
def user():
    payload = request.get_json()
    print(payload)
    if not payload:
        return jsonify({"error": "Invalid or missing payload"}), 400
    scores = calculate_dashboard(payload)
    return jsonify(scores)

from db import get_db_connection

@app.route("/user/db", methods=['POST'])
def planet():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid or missing payload"}), 400
    
    # Assuming payload contains 'name' and 'email' fields for a new user
    name = payload.get("Shubham")
    email = payload.get("email")

    if name and email:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "User added successfully"}), 201
        else:
            return jsonify({"error": "Database connection failed"}), 500
    else:
        return jsonify({"error": "Missing name or email"}), 400


if __name__ == "__main__":
    app.run()

from flask import Flask, request, jsonify
from service import calculate_dashboard
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

@app.route("/planets", methods=['POST'])
def user():
    payload = request.get_json()
    print(payload)
    if not payload:
        return jsonify({"error": "Invalid or missing payload"}), 400
    scores = calculate_dashboard(payload)
    return jsonify(scores)

if __name__ == "__main__":
    app.run()

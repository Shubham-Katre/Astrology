from flask import Flask, request, jsonify
from service import calculate_dashboard

app = Flask(__name__)

@app.route("/planets", methods=['POST'])
def user():
    print("run>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid or missing payload"}), 400
    scores = calculate_dashboard(payload)
    return jsonify(scores)

if __name__ == "__main__":
    app.run()

from flask import Flask, jsonify, request
import time
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/time')
def get_time():
    return jsonify(time=time.time())

@app.route("/api/demo")
def question():
    return {"Hello": "World"}

@app.route("/api/submit", methods=["POST"])
def submit_data():
    data = request.get_json()
    print("Received from React:", data)
    
    response = {"status": "success", "received": data}
    # need to return pdf of solutions
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3001)
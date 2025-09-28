from flask import Flask, jsonify, request
import time
from flask_cors import CORS
import json


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
    print("Received from React:", data["message"])
    data_dict = json.loads("'{" + {data["message"]} + "}'")
    
    # response = {"status": "success", "received": data}
    # need to return pdf of solutions

    '''
    {year}{div}{topic}{location}(S) or (A)?? seems they like to switch it up
    or
    {year}{div}{location}{month}(S)
    '''

    if data_dict["loc"] == "sw" or data_dict["loc"] == "reg":
        # structure is {year}{div}{location}{month}(S)
        query = f"{data_dict["year"]}{data_dict["div"]}{data_dict["loc"]}{data_dict["month"]}(S)"
    else:
        # structure is {year}{div}{topic}{location}(S) or (A)
        query = f"{data_dict["year"]}{data_dict["div"]}{data_dict["topic"]}{data_dict["loc"]}(S)"

    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True, port=3001)
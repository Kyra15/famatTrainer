from flask import Flask, jsonify, request
import time
from flask_cors import CORS
import dropbox
import pandas as pd
import json

DROPBOX_ACCESS_TOKEN = ''

with open("api/dropbox_token.json", "r") as f:
    DROPBOX_ACCESS_TOKEN = json.load(f)

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

    # i have never seen this syntax in my life
    data_dict = {
        pair.split(': ')[0]: pair.split(': ')[1] 
        for pair in data["message"].split(', ')
    }

    '''
    {year}{div}{topic}{location}(S) or (A)?? seems they like to switch it up
    or
    {year}{div}{location}{month}(S)
    '''

    # if data_dict["loc"] == "sw" or data_dict["loc"] == "reg":
    #     # structure is {year}{div}{location}{month}(S)
    #     query = f"{data_dict["year"]}{data_dict["div"]}{data_dict["loc"]}{data_dict["month"]}(S)".upper()
    # else:
    #     # structure is {year}{div}{topic}{location}(S) or (A)
    #     query = f"{data_dict["year"]}{data_dict["div"]}{data_dict["topic"]}{data_dict["loc"]}(S)".upper()
    
    queryDB(data_dict)

    return jsonify(data_dict)


def queryDB(data):
    # if data["loc"] == "sw" or data["loc"] == "reg":
    #     query = f'/famat//{data["div"]}/{{data["month"]}}-{{data["loc"]}}'

    if data["loc"] == "sw" or data["loc"] == "reg":
        # structure is {year}{div}{location}{month}(S)
        query = f"{data["year"]}{data["div"]}{data["loc"]}{data["month"]}(S)".upper()
    else:
        # structure is {year}{div}{topic}{location}(S) or (A)
        query = f"{data["year"]}{data["div"]}{data["topic"]}{data["loc"]}(S)".upper()
    db_key = connect_to_dropbox()
    # data = dropbox_list_files(db_key, )
    data = dropbox_list_files(db_key, query)
    print(data)

def connect_to_dropbox():
  
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print('Connected to Dropbox successfully')
    
    except Exception as e:
        print(str(e))
    
    return dbx

def dropbox_list_files(dbx, path):

    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            metadata = {
                'name': file.name,
                'path_display': file.path_display,
                'type': 'folder' if isinstance(file, dropbox.files.FolderMetadata) else 'file',
            }

            files_list.append(metadata)

        df = pd.DataFrame.from_records(files_list)
        return df
    except Exception as e:
        print('Error getting list of folders from Dropbox: ' + str(e))



if __name__ == '__main__':
    app.run(debug=True, port=3001)
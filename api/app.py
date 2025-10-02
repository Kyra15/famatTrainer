from flask import Flask, jsonify, request
import time
from flask_cors import CORS
import dropbox
import pandas as pd
import json
from dropbox import DropboxOAuth2FlowNoRedirect
import os
from dotenv import load_dotenv
import requests


load_dotenv()

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://famat-lookup.onrender.com"}})

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
    
    results = queryDB(data_dict)

    return jsonify(results)


def queryDB(data):

    # need to map the data to the right codes
    code_dict = {
                    "geo": "g",
                    "alg2": "a2",
                    "precalc": "pc",
                    "stats": "st",
                    "calc": "m",
                    "reg": "r",
                    "theta": "t",
                    "alpha": "a",
                    "mu": "m"
                }
    
    # map the divisions
    mapped_data = {
        key: code_dict.get(value, value)
        for key, value in data.items()
    }

    print(mapped_data)

    if mapped_data["custom"] != "{{all}}":
        query = mapped_data["custom"].strip().upper()
    elif mapped_data["loc"] == "sw" or mapped_data["loc"] == "r":
        # structure is {year}{div}{location}{month}(S)
        query = f"{mapped_data["year"]}{mapped_data["div"]}{mapped_data["loc"]}{mapped_data["month"]}".upper()
    else:
        # structure is {year}{div}{topic}{location}(S) or (A)
        query = f"{mapped_data["year"]}{mapped_data["div"]}{mapped_data["topic"]}{mapped_data["loc"]}".upper()

    db_key = connect_to_dropbox()
    
    results = find_files(db_key, "/famat", query)
    docs = {}
    for f in results:
        print(f"Found:", f.path_display)
        if "(T)" not in f.name:
            # metadata, res = db_key.files_download(f.path_display)
            # file_bytes = res.content
            # docs[f.name] = base64.b64encode(file_bytes).decode("utf-8")
            docs[f.name] = db_key.files_get_temporary_link(f.path_display).link
    
    # now, send get a temp link
    # then send back to react

    return docs


def connect_to_dropbox():
  
    try:
        dbx = dropbox.Dropbox(app_key=APP_KEY, oauth2_refresh_token=REFRESH_TOKEN)
        print('Connected to Dropbox successfully')
    
    except Exception as e:
        print(f"Error getting db key: {str(e)}")
    
    return dbx

# this doesnt work i have no clue why maybe due to special characters or sharing issues
# def dropbox_search(dbx, query):

#     print("Query:", query)

#     search_options = dropbox.files.SearchOptions(
#         path="/famat/theta/geo/jan-reg",
#         max_results=10,
#         file_extensions=[".pdf"],
#         filename_only=True
#     )

#     try:
#         results = dbx.files_search_v2(query, options=search_options)
#         for match in results.matches:
#             metadata = match.metadata.get_metadata()
#             if isinstance(metadata, dropbox.files.FileMetadata):
#                 print(f"Found file: {metadata.name} (Path: {metadata.path_display})")
#         print("Ran loop")
#     except Exception as e:
#         print('Error searching Dropbox: ' + str(e))


def find_files(dbx, folder, query):
    result = dbx.files_list_folder(folder, recursive=True)
    matches = []

    while True:
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if query.lower() in entry.name.lower():
                    matches.append(entry)
        if result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
        else:
            break
    return matches


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
    app.run(debug=True ,host='0.0.0.0', port=3001)
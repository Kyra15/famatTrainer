import dropbox
import pandas as pd
import json

DROPBOX_ACCESS_TOKEN = ''

with open("api/dropbox_token.json", "r") as f:
    DROPBOX_ACCESS_TOKEN = json.load(f)

def connect_to_dropbox():
  
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print('Connected to Dropbox successfully')
    
    except Exception as e:
        print(str(e))
    
    return dbx

dbx = connect_to_dropbox()

def dropbox_list_files(path):
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
    """

    dbx = connect_to_dropbox()

    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            # if isinstance(file, dropbox.files.FolderMetadata):
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
      

data = dropbox_list_files('/theta')

print(data)

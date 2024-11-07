import os

def get_api_key ():
    with open ("api key") as f:
        return f.readline().strip()
    
def check_if_file_exists_and_create (filePath):
    if not os.path.exists(filePath):
        with open(filePath, 'w') as f:
            pass
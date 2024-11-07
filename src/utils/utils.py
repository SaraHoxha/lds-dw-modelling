import os

def get_api_key ():
    with open ("api key") as f:
        return f.readline().strip()
    
def check_if_file_exists_and_create (filePath):
    if not os.path.exists(filePath):
        with open(filePath, 'w') as f:
            pass
        

def fill_missing_values (dataset, column_defaults):
    for row_key, row in dataset.items():
        for column, default_value in column_defaults.items():
            if  row[column] is None:
                row[column] = default_value
    return dataset

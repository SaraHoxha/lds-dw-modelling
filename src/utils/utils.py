import os
from datetime import datetime

DAY_COLUMN = 'DAY'
MONTH_COLUMN = 'MONTH'
YEAR_COLUMN = 'YEAR'
TIME_COLUMN = 'TIME'

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


def split_date(dataset, date_column):
    for row in dataset.values():
        if row.get(date_column):
            dt = datetime.strptime(row[date_column], "%m/%d/%Y %I:%M:%S %p")
            row[YEAR_COLUMN] = dt.year
            row[MONTH_COLUMN] = dt.month
            row[DAY_COLUMN] = dt.day
            row[TIME_COLUMN] = dt.strftime("%I:%M:%S %p")
            
    return dataset
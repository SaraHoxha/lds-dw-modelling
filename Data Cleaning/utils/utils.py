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
        

# Fill missing values for columns that provide a default 'Unknown' value
def fill_missing_values (dataset, column_defaults):
    for row in dataset.values():
        for column, default_value in column_defaults.items():
            if column in row:
                if row[column] == '':
                    row[column] = default_value
            else:
                print(f"Column {column} not found in row")       
    return dataset


#Split date column into 'DAY', 'MONTH', 'YEAR', 'TIME' columns
def split_date(dataset, date_column):
    for row in dataset.values():
        if row.get(date_column):
            try:
                # year is YYYY and 12-hour format
                dt = datetime.strptime(row[date_column], "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                try:
                    #year is YYYY 24-hour format
                    dt = datetime.strptime(row[date_column], "%m/%d/%y %H:%M")
                except ValueError as e:
                    print(f'Date is: {row.get(date_column)}')
                    print(f'Error: {e}')
                    
            row[YEAR_COLUMN] = dt.year
            row[MONTH_COLUMN] = dt.month
            row[DAY_COLUMN] = dt.day
            row[TIME_COLUMN] = dt.strftime("%I:%M:%S %p")
            
    return dataset
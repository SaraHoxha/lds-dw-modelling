import os
import csv
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
    print ("Filling missing values with default value", column_defaults)
    for row in dataset.values():
        try:
            for column, default_value in column_defaults.items():
                if column in row:
                    if row[column] == '':
                        row[column] = default_value      
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset


#Split date column into 'DAY', 'MONTH', 'YEAR', 'TIME' columns
def split_date(dataset, date_column):
    print ("Splitting date column", date_column, "into 'DAY', 'MONTH', 'YEAR', 'TIME'")

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

def select_columns(data, columns):
    print ("Filtering the dataset by columns", columns)
    """
    Filters a list of dictionaries to include only the specified keys.

    :param data: List of dictionaries (e.g., rows from a CSV file).
    :param columns: List of keys to retain in the dictionaries.
    :return: A new list of dictionaries containing only the specified keys.
    """
    return [
        {key: row[key] for key in columns if key in row}
        for row in data
    ]

def concatenate_values(input_dict, idColumn):
    """
    Takes a dictionary as input and returns a string 
    with all the values concatenated.

    Args:
    input_dict (dict): The input dictionary.

    Returns:
    str: A concatenated string of all dictionary values.
    """
    if not isinstance(input_dict, dict):
        raise ValueError("Input must be a dictionary.")

    concatenated_string = ""
    for key in list(input_dict.keys()):
        if key != idColumn:
            concatenated_string += " " + str(input_dict[key])

    return concatenated_string.strip()

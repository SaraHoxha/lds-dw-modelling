from datetime import datetime
from typing import Dict, Any, Union
import os

DAY_COLUMN = 'DAY'
MONTH_COLUMN = 'MONTH'
YEAR_COLUMN = 'YEAR'
TIME_COLUMN = 'TIME'

def get_api_key() -> str:
    """
    Reads and returns the API key from a file named 'api key'.

    :return: The API key as a string.
    """
    with open("api key") as f:
        return f.readline().strip()

def check_if_file_exists_and_create(filePath: str) -> None:
    """
    Checks if a file exists at the specified path. If it does not, creates an empty file.

    :param filePath: Path to the file to check and possibly create.
    :return: None
    """
    if not os.path.exists(filePath):
        with open(filePath, 'w') as f:
            pass

def convert_value(value: str) -> Union[int, float, str]:
    """
    Converts a string value to an int, float, or keeps it as a string if conversion is not possible.

    :param value: The value to convert (as a string).
    :return: The converted value (int, float, or the original string).
    """
    try:
        if '.' in value:
            float_value = float(value)
            if float_value.is_integer():
                return int(float_value)  # Convert to int if the value is a whole number
            return float_value
        else:
            return int(value)  # Convert to int if there's no decimal point
    except ValueError:
        return value  # Return the original value if conversion fails

def fill_missing_values(dataset: Dict[str, Dict[str, Any]], column_defaults: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Fills missing (empty) values in the dataset with default values for specified columns.

    :param dataset: A dictionary representing the dataset, where each row is a dictionary of column names and values.
    :param column_defaults: A dictionary of default values for columns where missing values should be filled.
    :return: The dataset with missing values filled.
    """
    print("Filling missing values with default value", column_defaults)
    for row in dataset.values():
        try:
            for column, default_value in column_defaults.items():
                if column in row and row[column] == '':
                    row[column] = default_value  # Fill missing value with default
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

def split_date(dataset: Dict[str, Dict[str, Any]], date_column: str, affix="") -> Dict[str, Dict[str, Any]]:
    """
    Splits a date string in the specified date column into separate 'DAY', 'MONTH', 'YEAR', and 'TIME' columns.

    :param dataset: A dictionary representing the dataset, where each row is a dictionary of column names and values.
    :param date_column: The name of the column containing date strings to split.
    :return: The dataset with the date column split into multiple components.
    """
    print ("Splitting date column", date_column, "into 'DAY" + affix + "', 'MONTH" + affix + "', 'YEAR" + affix + "', 'TIME" + affix + "'")

    for row in dataset.values():
        if row.get(date_column):
            try:
                # Try parsing the date using 12-hour format
                dt = datetime.strptime(row[date_column], "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                try:
                    # Fallback to 24-hour format
                    dt = datetime.strptime(row[date_column], "%m/%d/%y %H:%M")
                except ValueError as e:
                    print(f'Date is: {row.get(date_column)}')
                    print(f'Error: {e}')

            # Assign extracted date parts to respective columns
            row[YEAR_COLUMN + affix] = dt.year
            row[MONTH_COLUMN + affix] = dt.month
            row[DAY_COLUMN + affix] = dt.day
            row[TIME_COLUMN + affix] = dt.strftime("%I:%M:%S %p")
            
    return dataset

def concatenate_values(input_dict: Dict[str, Any], idColumn: str) -> str:
    """
    Concatenates all values in a dictionary into a single string, excluding the value of the specified ID column.

    :param input_dict: The dictionary to concatenate.
    :param idColumn: The column to exclude from the concatenation.
    :return: A concatenated string of all dictionary values, excluding the ID column.
    :raises ValueError: If the input is not a dictionary.
    """
    if not isinstance(input_dict, dict):
        raise ValueError("Input must be a dictionary.")

    concatenated_string = ""
    for key in list(input_dict.keys()):
        if key != idColumn:
            concatenated_string += " " + str(input_dict[key])

    return concatenated_string.strip()

def getDBPassword():
    with open ("dbPassword") as f:
        return f.readline().strip()
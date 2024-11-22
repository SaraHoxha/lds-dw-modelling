import csv
from os.path import basename
from typing import List, Dict, Any, Union
from utils.utils import concatenate_values, convert_value

def read_csv(
    file_path: str, 
    primary_key: str = None, 
    idColumn: List[str] = None,
    no_duplicates = True
) -> Union[Dict[str, Dict[str, Union[int, float, str]]], List[Dict[str, Union[int, float, str]]]]:
    """
    Reads a CSV file and returns data in various formats based on provided parameters.
    
    Args:
        file_path (str): The path to the CSV file to be read.
        primary_key (str, optional): The column name to be used as the dictionary key. Defaults to None.
        idColumn (List[str], optional): List of column names to concatenate for creating unique keys. Defaults to None.
        
    Returns:
        Union[Dict[str, Dict[str, Union[int, float, str]]], List[Dict[str, Union[int, float, str]]]]:
        A dictionary or a list of dictionaries based on the provided parameters.
        
    Raises:
        Exception: If the file is not found, there's a problem reading the file, or an unexpected error occurs.
    """
    print("Reading CSV:", basename(file_path))
    result = {}

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if primary_key:
                # Option 1: Use a primary key
                result = {
                    row[primary_key]: {k: convert_value(v) for k, v in row.items()}
                    for row in reader
                }
            elif idColumn:
                # Option 2: Use concatenated values from specified columns as keys
                result = {}
                for row in reader:

                    key = concatenate_values(row, idColumn)
                    if no_duplicates and key in result:
                        print('ROW')
                        print(row)
                        raise ValueError(f"Duplicate key found: {key}")
                    result[key] = {k: convert_value(v) for k, v in row.items()}
            else:
                # Option 3: Just return a list of dictionaries (all rows)
                result = [
                    {k: convert_value(v) for k, v in row.items()}
                    for row in reader
                ]
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")

    return result


def to_csv(
    data: Union[Dict[str, Dict[str, Any]], List[Dict[str, Any]]], 
    file_name: str, 
    use_writer: bool = False
) -> None:
    """
    Writes data to a CSV file, supporting both dictionary and list of dictionaries formats.
    
    Args:
        data (Union[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]): The data to write to the file.
            - If a dictionary is provided, the keys represent rows and the values are row data.
            - If a list is provided, each element is a row represented as a dictionary.
        file_name (str): The name (or path) of the file where the CSV data will be saved.
        use_writer (bool, optional): Whether to use `csv.writer` for writing. Defaults to False.
        
    Raises:
        Exception: If the input data is empty or an error occurs while writing the file.
    """
    print(f"Saving data to: {file_name}")
    
    # Determine headers and handle empty data
    if isinstance(data, dict):
        if not data:
            raise Exception("The dictionary is empty. No file will be created.")
        headers = list(next(iter(data.values())).keys())
        rows = data.values()
    elif isinstance(data, list):
        if not data:
            raise Exception("The list of dictionaries is empty. No file will be created.")
        headers = list(data[0].keys())
        rows = data
    else:
        raise TypeError("Input data must be a dictionary or a list of dictionaries.")
    
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            if use_writer:
                # Use csv.writer
                writer = csv.writer(csvfile)
                writer.writerow(headers)  # Write headers
                writer.writerows([row.values() for row in rows])  # Write rows
            else:
                # Use csv.DictWriter
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()  # Write headers
                writer.writerows(rows)  # Write rows
                
        print(f"Data successfully saved to {file_name}")
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")

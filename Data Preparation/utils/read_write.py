import csv
from os.path import basename
from typing import List, Dict, Any, Union
from utils.utils import concatenate_values, convert_value

def read_csv(file_path: str, primary_key: str) -> Dict[str, Dict[str, Union[int, float, str]]]:
    """
    Reads a CSV file and converts its contents into a dictionary keyed by the specified primary key.
    
    Args:
        file_path (str): The path to the CSV file to be read.
        primary_key (str): The column name to be used as the dictionary key.
        
    Returns:
        Dict[str, Dict[str, Union[int, float, str]]]: A dictionary representation of the CSV file.
        
    Raises:
        Exception: If the file is not found, there's a problem reading the file, or an unexpected error occurs.
    """
    print("Reading CSV:", basename(file_path))
    result: Dict[str, Dict[str, Union[int, float, str]]] = {}

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            result = {
                row[primary_key]: {k: convert_value(v) for k, v in row.items()}
                for row in reader
            }
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")


    return result

def read_csv_v2(file_path: str) -> List[Dict[str, Union[int, float, str]]]:
    """
    Reads a CSV file and converts its contents into a list of dictionaries.
    
    Args:
        file_path (str): The path to the CSV file to be read.
        
    Returns:
        List[Dict[str, Union[int, float, str]]]: A list of dictionaries representing the CSV rows.
        
    Raises:
        Exception: If the file is not found, there's a problem reading the file, or an unexpected error occurs.
    """
    print("Reading CSV:", basename(file_path))
    result: List[Dict[str, Union[int, float, str]]] = []


    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            result = [
                {k: convert_value(v) for k, v in row.items()}
                for row in reader
            ]
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")


    return result

def read_csv_v3(file_path: str, idColumn: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Reads a CSV file and creates a dictionary where keys are concatenated values from specified columns.
    
    Args:
        file_path (str): The path to the CSV file to be read.
        idColumn (List[str]): List of column names to concatenate for creating unique keys.
        
    Returns:
        Dict[str, Dict[str, str]]: A dictionary with concatenated keys and row data as values.
        
    Raises:
        Exception: If the file is not found, there's a problem reading the file, or an unexpected error occurs.
    """
    print("Reading CSV:", basename(file_path))
    result: Dict[str, Dict[str, str]] = {}

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Generate a unique key by concatenating specified column values
                key = concatenate_values(row, idColumn)
                if key in result:
                    raise ValueError(f"Duplicate key found: {key}")
                result[key] = {k: convert_value(v) for k, v in row.items()}
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")


    return result

def to_csv(df: Dict[str, Dict[str, Any]], file_path: str) -> None:
    """
    Writes a dictionary of data to a CSV file.
    
    Args:
        df (Dict[str, Dict[str, Any]]): The dictionary containing the data to write.
        file_path (str): The path where the CSV file will be saved.
    """
    print("Saving data to:", file_path)
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(next(iter(df.values())).keys()))
        writer.writeheader()
        for row in df.values():
            writer.writerow(row)

def to_csv_v2(dict_list: List[Dict[str, Any]], file_name: str) -> None:
    """
    Writes a list of dictionaries to a CSV file.
    
    Args:
        dict_list (List[Dict[str, Any]]): The list of dictionaries to write.
        file_name (str): The name of the file where the CSV data will be saved.
        
    Raises:
        Exception: If the input list is empty or an error occurs while writing the file.
    """
    if not dict_list:
        raise Exception("The dictionary list is empty. No file will be created.")

    headers = dict_list[0].keys()  # Extract headers from the first dictionary
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for dictionary in dict_list:
                writer.writerow(dictionary)
        print(f"Data successfully saved to {file_name}")
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")

def to_csv_v3(dict_list: List[Dict[str, Any]], file_name: str) -> None:
    """
    Writes a list of dictionaries to a CSV file using the `csv.writer`.

    Args:
        dict_list (List[Dict[str, Any]]): A list of dictionaries containing the data to write to the CSV file.
        file_name (str): The name (or path) of the file where the CSV data will be saved.

    Raises:
        Exception: If an error occurs while writing to the file.
    """
    if not dict_list:
        raise Exception("The dictionary list is empty. No file will be created.")
    
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(dict_list)
                
        print(f"Data successfully saved to {file_name}")
        
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")
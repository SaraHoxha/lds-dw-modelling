import csv
from os.path import basename

def read_csv(file_path, primary_key):
    """
    outputs a dictionary with the following structure
    {
        primary key val_n:
            {col1:val1, col2:val2, ... col_m:val_m}
    }
    """
    print ("Reading csv", basename(file_path))
    result = {}  # Initialize an empty dictionary to store the CSV data

    def convert_value(value):
        """Convert value to int or float if possible, otherwise return as is."""
        try:
            if '.' in value:  # Check for float
                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                return float_value
            else:  # Check for int
                return int(value)
        except ValueError:
            return value  # Return the original value if conversion fails

    try:
        # Open the specified CSV file in read mode
        with open(file_path, mode='r', newline='') as csvfile:
            # Create a CSV dictionary reader to read rows as dictionaries
            reader = csv.DictReader(csvfile)

            # Populate the result dictionary with data from the CSV
            result = {
                # Use the value of the primary key as the dictionary key
                row[primary_key]: {k: convert_value(v) for k, v in row.items()} 
                for row in reader  # Iterate over each row in the CSV
            }

    except FileNotFoundError:
        # Handle the case where the specified file does not exist
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        # Handle errors related to CSV reading
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"An unexpected error occurred: {e}")

    return result  # Return the populated dictionary containing CSV data

def read_csv_v2(file_path):
    """
    outputs a list with the following structure
    [
        {col1:val1, col2:val2, ... col_m:val_m}
    ]
    """

    print ("Reading csv", basename(file_path))
    result = []  # Initialize an empty list to store the CSV data

    def convert_value(value):
        """Convert value to int or float if possible, otherwise return as is."""
        try:
            if '.' in value:  # Check for float
                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                return float_value
            else:  # Check for int
                return int(value)
        except ValueError:
            return value  # Return the original value if conversion fails

    try:
        # Open the specified CSV file in read mode
        with open(file_path, mode='r', newline='') as csvfile:
            # Create a CSV dictionary reader to read rows as dictionaries
            reader = csv.DictReader(csvfile)

            # Populate the result dictionary with data from the CSV
            result = [
                {k: convert_value(v) for k, v in row.items()} 
                for row in reader  # Iterate over each row in the CSV
            ]

    except FileNotFoundError:
        # Handle the case where the specified file does not exist
        raise Exception(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        # Handle errors related to CSV reading
        raise Exception(f"Error: There was a problem reading the CSV file: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"An unexpected error occurred: {e}")

    return result  # Return the populated dictionary containing CSV data

def to_csv (df, file_path):
    print ("Saving data at filepath:", file_path)
    with open(file_path, mode='w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=df[next(iter(df))].keys())
        
        # Write the header row
        writer.writeheader()
        
        # Write each row of data
        for key, row in df.items():
            writer.writerow(row)

import csv

def to_csv_v2(dict_list, file_name):
    """
    Saves a list of dictionaries to a CSV file.

    Parameters:
    - dict_list: List[Dict], the list of dictionaries to save.
    - file_name: str, the name of the output CSV file.
    """
    if not dict_list:
        raise Exception("The dictionary list is empty. No file will be created.")
    
    # Extract the keys from the first dictionary as headers
    headers = dict_list[0].keys()
    
    try:
        # Open the file for writing
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            
            # Write the headers first
            writer.writeheader()
            
            # Write the rows
            for dictionary in dict_list:
                writer.writerow(dictionary)
        
        print(f"Data has been successfully saved to {file_name}")
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")

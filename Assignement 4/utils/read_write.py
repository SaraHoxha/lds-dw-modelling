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
        print(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        # Handle errors related to CSV reading
        print(f"Error: There was a problem reading the CSV file: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

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
        print(f"Error: The file {file_path} was not found.")
    except csv.Error as e:
        # Handle errors related to CSV reading
        print(f"Error: There was a problem reading the CSV file: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

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

def to_csv_v2 (df, file_path):
    print ("Saving data at filepath:", file_path)
    with open(file_path, mode='w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=df[0].keys())

        # Write the header (column names)
        writer.writeheader()

        # Write each row
        for row in df:
            writer.writerow(row)
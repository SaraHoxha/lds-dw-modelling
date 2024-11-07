import csv

def read_csv(file_path, primary_key='RD_NO'):
    result = {}  # Initialize an empty dictionary to store the CSV data

    def convert_value(value):
        """Convert value to int or float if possible, otherwise return as is."""
        try:
            if '.' in value:  # Check for float
                return float(value)
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
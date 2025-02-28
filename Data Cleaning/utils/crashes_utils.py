# Imports
import re
from datetime import datetime
import json
import time
import sys
import os
from opencage.geocoder import OpenCageGeocode

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.utils import get_api_key, check_if_file_exists_and_create
sys.path = original_sys_path

# adding geospatial missing data
def query_api(queries, resultDict):
    """
    Query the OpenCage Geocoding API to get latitude and longitude for given addresses.
    
    Args:
        queries (set): Set of address strings to geocode
        resultDict (dict): Existing dictionary of cached geocoding results
        
    Returns:
        dict: Updated dictionary containing geocoding results with query strings as keys and lat/lng coordinates as values
    
    Raises:
        Exception: If geocoding fails for any query
    """
    # Initialize the geocoder with the API key
    geocoder = OpenCageGeocode(get_api_key())

    # Iterate over each query in the provided list
    for query in queries:
        # Check if the query has already been processed
        if query not in resultDict:
            try:
                # Attempt to geocode the query
                results = geocoder.geocode(query)
                # If results are found, extract latitude and longitude
                if results:
                    resultDict[query]= {
                        "lat": results[0]['geometry']['lat'],
                        "lng": results[0]['geometry']['lng'],
                    }
                else:
                    # Log if no results were found for the query
                    print(f"No results found for query: {query}")
            except Exception as e:
                # Log any errors that occur during the geocoding process
                raise Exception(f"Error geocoding query '{query}': {e}")
            # Sleep for 1 second to avoid hitting the API rate limit
            time.sleep(1)
    
    # Return the updated result dictionary with geocoded data
    return resultDict

def create_file_with_missing_location_values(crashes_df, results_file="data/missing lat lng python.json"):
    """
    Create or update a JSON file containing geocoded location data for crashes with missing coordinates.
    
    Args:
        crashes_df (dict): Dictionary containing crash data
        results_file (str): Path to JSON file for storing geocoding results
        
    """
    print(f"Starting the process to create file with missing location values from '{results_file}'...")
    # Ensure the results file exists or create it if it doesn't
    check_if_file_exists_and_create(results_file)
    
    try:
        # Attempt to open and read the existing results file
        with open(results_file) as f:
            resultDict = json.load(f)  # Load the JSON data into a dictionary
    except FileNotFoundError:
        # If the file does not exist, initialize an empty dictionary
        resultDict = {}
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors (e.g., if the file is corrupted)
        print(f"Error decoding JSON from file '{results_file}': {e}")
        resultDict = {}  # Reset to an empty dictionary
    except Exception as e:
        # Handle any other unexpected exceptions that may occur
        print(f"Unexpected error while reading '{results_file}': {e}")
        resultDict = {}  # Reset to an empty dictionary

    # Create a set of queries based on the STREET_NAME and STREET_NO from the crashes DataFrame
    queries = {f"{row['STREET_NAME']} {row['STREET_NO']}, Chicago, Illinois" 
               for row in crashes_df.values() 
               if row["LATITUDE"] == '' and row["LONGITUDE"] == ''}
    
    try:
        # Call the query_api function to get geocoded data for the queries
        resultDict = query_api(queries, resultDict)
    except Exception as e:
        # Handle errors that may occur during the API query
        print(f"Error during API query: {e}")

    try:
        # Attempt to write the updated result dictionary back to the results file
        with open(results_file, 'w') as f:
            json.dump(resultDict, f, indent=4)  # Save the dictionary as JSON
    except Exception as e:
        # Handle errors that may occur while writing to the file
        print(f"Error writing to file '{results_file}': {e}")

def fill_missing_location_values(crashes_df, results_file="data/missing lat lng python.json"):
    """
    Fill missing latitude, longitude, and location values in crashes dataset using cached geocoding results.
    
    Args:
        crashes_df (dict): Dictionary containing crash data
        results_file (str): Path to JSON file containing geocoding results
        
    Returns:
        dict: Updated crashes dictionary with filled location values
    """
    print(f"Filling missing location values using data from '{results_file}'...")
    with open (results_file) as f:
        resultDict = json.load(f)

    for indexKey, row in crashes_df.items():
        if isinstance(row['LATITUDE'], str): #missing values, present values are float
            if row["STREET_NAME"] != '':
                query_key_value = f"{row['STREET_NAME']} {row['STREET_NO']}, Chicago, Illinois"
                location = "POINT (" + str(resultDict[query_key_value]["lng"]) + " " + str(resultDict[query_key_value]["lat"]) + ")"
                crashes_df[indexKey]["LATITUDE"] = resultDict[query_key_value]["lat"]
                crashes_df[indexKey]["LONGITUDE"] = resultDict[query_key_value]["lng"]
                crashes_df[indexKey]["LOCATION"] = location
    
    return crashes_df

def fill_missing_BEAT_OF_OCCURRENCE(dict_df):
    """
    Fill missing beat of occurrence values based on location matches in the dataset.
    
    Args:
        dict_df (dict): Dictionary containing crash data
        
    Returns:
        dict: Updated dictionary with filled beat of occurrence values
        
    Raises:
        ValueError: If row data is missing required fields
        KeyError: If required keys are missing from row data
    """
    print(f"Filling missing beat of occurrence values...")
    
    # Initialize sets and dictionaries to track missing beats and location-to-beat mappings.
    missing_beat_indexes = set()
    location_to_beat_dict = {}

    try:
        # First pass: Identify rows with missing 'BEAT_OF_OCCURRENCE' and build location-to-beat mapping
        for index_key, row in dict_df.items():
            # Check if row is valid and contains required keys
            if not isinstance(row, dict) or 'BEAT_OF_OCCURRENCE' not in row or 'LOCATION' not in row:
                raise ValueError(f"Row at index {index_key} is missing required fields.")
            
            beat_of_occurrence = row['BEAT_OF_OCCURRENCE']
            location = row['LOCATION']

            # Track rows where 'BEAT_OF_OCCURRENCE' is missing but 'LOCATION' is present
            if beat_of_occurrence == '' and location != '':
                missing_beat_indexes.add((index_key, location))

            # Build location-to-beat mapping for rows with both values present
            if beat_of_occurrence != '' and location != '':
                location_to_beat_dict[location] = beat_of_occurrence

        # Second pass: Fill missing 'BEAT_OF_OCCURRENCE' based on location-to-beat mapping
        for index_key, location in missing_beat_indexes:
            # Fill 'BEAT_OF_OCCURRENCE' if a mapping for the location exists
            if location in location_to_beat_dict:
                dict_df[index_key]['BEAT_OF_OCCURRENCE'] = location_to_beat_dict[location]

    except KeyError as e:
        print(f"KeyError encountered: {e}. Ensure all rows have 'BEAT_OF_OCCURRENCE' and 'LOCATION' keys.")
    except ValueError as e:
        print(f"ValueError encountered: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return dict_df

# adding delta between car crash and police report
def add_delta_car_crash_date_police_report_date(crashes_df):
    """
    Calculate and add time difference between crash date and police report date.
    
    Args:
        crashes_df (dict): Dictionary containing crash data
        
    Returns:
        dict: Updated dictionary with new 'DELTA_TIME_CRASH_DATE_POLICE_REPORT_DATE' field
        
    Note:
        Time delta is formatted as "X days, Y hours, Z minutes, W seconds"
    """
    print("Calculating the time delta between crash dates and police report dates...")
    # Define the date format for parsing
    date_format = "%m/%d/%Y %I:%M:%S %p"
    
    # Iterate over each item in the crashes DataFrame
    for _, row in crashes_df.items():
        try: 
            # Parse the crash date from the DataFrame
            crash_date = datetime.strptime(row['CRASH_DATE'], date_format)
            # Parse the date when police were notified
            date_police_notified = datetime.strptime(row['DATE_POLICE_NOTIFIED'], date_format)

            # Calculate the time difference between the two dates
            delta = date_police_notified - crash_date

            # Store the delta time in a formatted string in the DataFrame
            row['DELTA_TIME_CRASH_DATE_POLICE_REPORT_DATE'] = f"{delta.days} days, {delta.seconds // 3600} hours, {(delta.seconds // 60) % 60} minutes, {delta.seconds % 60} seconds" 
        except KeyError as e:
            # Handle cases where expected keys might be missing
            print(f'KeyError for key {row.get("RD_NO", "unknown")}: {e}')  
        except ValueError as e:
            # Handle cases where the date format is invalid
            print(f'ValueError for key {row.get("RD_NO", "unknown")}: {e}')  
        except Exception as e:
            # Handle any other unexpected exceptions
            print(f'Unexpected error for key {row.get("RD_NO", "unknown")}: {e}')  
    
    # Return the modified DataFrame with the added delta time
    return crashes_df

# fixing wrong licens plates
def fix_license_plates(dict_df):
    """
    Standardize license plate formats and fix inconsistencies.
    
    Args:
        dict_df (dict): Dictionary containing crash data
        
    Returns:
        dict: New dictionary with standardized license plate keys
        
    Note:
        Valid license plate format is two uppercase letters followed by six digits
    """
    print("Checking and fixing license plates...")
    # Define a regex pattern for valid license plates
    license_plates_pattern = r'^[A-Z]{2}\d{6}$'
    
    # Initialize a new dictionary to store modified entries
    modified_dict = {}

    # Iterate over each key-value pair in the input dictionary
    for indexKey, row in dict_df.items():
        try:  # Start of exception handling
            # Check if the key does not match the license plate pattern
            if not re.match(license_plates_pattern, indexKey):
                # Convert the 'RD_NO' value to uppercase
                row['RD_NO'] = row['RD_NO'].upper()  
                # Add the modified entry to the new dictionary with the key in uppercase
                modified_dict[indexKey.upper()] = row 
            else:
                # If the key matches the pattern, add it unchanged to the new dictionary
                modified_dict[indexKey] = row 
        except KeyError as e:
            # Handle cases where expected keys might be missing
            print(f'KeyError for key {indexKey}: {e}')  
        except Exception as e:
            # Handle any other unexpected exceptions
            print(f'Unexpected error for key {indexKey}: {e}')  

    # Return the modified dictionary with updated license plates
    return modified_dict

# conversion of the float64 columns to int when there is no need for it to be a float
def convert_float_columns_to_int_columns(dict_df, columns_to_convert = [
    'NUM_UNITS',
    'INJURIES_TOTAL',
    'INJURIES_FATAL',
    'INJURIES_INCAPACITATING',
    'INJURIES_NON_INCAPACITATING',
    'INJURIES_REPORTED_NOT_EVIDENT',
    'INJURIES_NO_INDICATION',
    'INJURIES_UNKNOWN'
]):
    """
    Convert specified float columns to integer type where appropriate.
    
    Args:
        dict_df (dict): Dictionary containing crash data
        columns_to_convert (list): List of column names to convert from float to int
        
    Returns:
        dict: Updated dictionary with converted numeric types
        
    Note:
        Handles conversion of both float and string values to integers
    """
    print("Converting float columns to integer columns where applicable...")
    # Iterate over each key-value pair in the input dictionary
    for indexKey, row in dict_df.items():
        # Iterate over each column specified for conversion
        for col in columns_to_convert:
            # Get the value for the current column
            value = row.get(col)

            # Check if the value is a float
            if isinstance(value, float):
                # Convert float to int and update the dictionary
                dict_df[indexKey][col] = int(value)
            elif isinstance(value, int):
                continue
            # Check if the value is a string
            elif isinstance(value, str):
                try:
                    # Attempt to convert the string to a float, then to an int
                    dict_df[indexKey][col] = int(float(value))
                except (ValueError, TypeError) as e:
                    # Print an error message if conversion fails
                    print(f'Error converting column {col} for key {indexKey}: {e}')
            else:
                # Print a message for unexpected data types
                print(f'Unexpected type for column {col} in key {indexKey}: {type(value)}')

    # Return the modified dictionary with converted columns
    return dict_df

def fill_missing_values_with_placeholder_string(data_dict, placeholder_string = 'unknown', columns = [
    'STREET_DIRECTION', 'STREET_NAME', 'BEAT_OF_OCCURRENCE',
    'LATITUDE', 'LONGITUDE', 'LOCATION']):
    """
    Fill empty string values with a placeholder string for specified columns.
    
    Args:
        data_dict (dict): Dictionary containing crash data
        placeholder_string (str): String to use for filling missing values
        columns (list): List of column names to check for missing values
        
    Returns:
        dict: Updated dictionary with filled missing values
    """
    try:
        # Iterate over each row's data in the dictionary
        for row_id, row_data in data_dict.items():
            # Validate that each row is a dictionary
            if not isinstance(row_data, dict):
                raise ValueError(f"Expected row data to be a dictionary, but got {type(row_data)} for row {row_id}")

            # Iterate through specified columns and fill missing values with 'unknown'
            for col in columns:
                if col in row_data and row_data[col] == '':
                    row_data[col] = placeholder_string
                    
    except Exception as e:
        # Catch and log any unexpected exceptions for debugging purposes
        raise Exception(f"An error occurred while filling missing values: {e}")
        
    return data_dict

"""
Data integrity checking module for crash data warehouse tables.
This module provides functionality to validate CSV files against predefined schemas,
checking for data types, primary keys, and non-nullable constraints.
"""

import csv
from typing import Dict, List, Tuple, Union, Any

# Define file paths
FILE_PATHS = {
    "CrashLocation": "Data Preparation/dw_tables_csv/CrashLocation.csv",
    "CrashCondition": "Data Preparation/dw_tables_csv/CrashCondition.csv",
    "Injury": "Data Preparation/dw_tables_csv/Injury.csv",
    "DateTime": "Data Preparation/dw_tables_csv/DateTime.csv",
    "Crash": "Data Preparation/dw_tables_csv/Crash.csv",
    "Person": "Data Preparation/dw_tables_csv/Person.csv",
    "Vehicle": "Data Preparation/dw_tables_csv/Vehicle.csv",
    "DamageReimbursement": "Data Preparation/dw_tables_csv/DamageReimbursement.csv",
}

# Define schema, primary keys, and non-nullable columns for each table
SCHEMAS = {
    "CrashLocation": {
        "schema": {
            "Crash_Location_ID": int,
            "Street_No": int,
            "Street_Direction": str,
            "Beat_Of_Occurrence": int,
            "Latitude": float,
            "Longitude": float,
            "Location": str,
        },
        "primary_key": "Crash_Location_ID",
        "non_nullable": ["Crash_Location_ID"],
    },
    "CrashCondition": {
        "schema": {
            "Crash_Condition_ID": int,
            "Posted_Speed_Limit": int,
            "Traffic_Control_Device": str,
            "Traffic_Control_Device_Condition": str,
            "Weather_Condition": str,
            "Lighting_Condition": str,
            "Trafficway_Type": str,
            "Roadway_Surface_Condition": str,
            "Road_Defect": str,
            "Alignment": str,
        },
        "primary_key": "Crash_Condition_ID",
        "non_nullable": ["Crash_Condition_ID"],
    },
    "Injury": {
        "schema": {
            "Injury_ID": int,
            "Injuries_Total": int,
            "Injuries_Fatal": int,
            "Injuries_Incapacitating": int,
            "Injuries_Non_Incapacitating": int,
            "Injuries_No_Indication": int,
            "Injuries_Reported_Not_Evident": int,
            "Injuries_Unknown": int,
        },
        "primary_key": "Injury_ID",
        "non_nullable": ["Injury_ID"],
    },
    "DateTime": {
        "schema": {
            "DateTime_ID": int,
            "Day": int,
            "Month": int,
            "Year": int,
            "Time": str,  
        },
        "primary_key": "DateTime_ID",
        "non_nullable": ["DateTime_ID"],
    },
    "Crash": {
        "schema": {
            "Crash_ID": int,
            "Crash_Date_ID": int,
            "Police_Notified_Date_ID": int,
            "Crash_Location_ID": int,
            "Crash_Condition_ID": int,
            "Injury_ID": int,
            "Primary_Contributory_Cause": str,
            "Secondary_Contributory_Cause": str,
            "Number_of_Units": int,
            "Most_Severe_Injury": str,
            "Difference_Between_Crash_Date_And_Police_Notified": str,
        },
        "primary_key": "Crash_ID",
        "non_nullable": [
            "Crash_ID"
        ],
    },
    "Vehicle": {
        "schema": {
            "Vehicle_ID": int,
            "Date_ID": int,
            "Unit_NO": int,
            "Unit_Type": str,
            "Make": str,
            "Model": str,
            "License_Plate_State": str,
            "Year": str,
            "Defect": str,
            "Type": str,
            "Use": str,
            "Travel_Direction": str,
            "Maneuver": str,
            "Occupant_Count": int,
            "First_Contact_Point": str,
        },
        "primary_key": "Vehicle_ID",
        "non_nullable": [
            "Vehicle_ID"
        ],
    },
    "DamageReimbursement": {
        "schema": {
            "Crash_ID": int,
            "Person_ID": int,
            "Vehicle_ID": int,
            "Cost": float,
            "Category": str,
        },
        "primary_key": ["Crash_ID", "Person_ID", "Vehicle_ID"],  
        "non_nullable": ["Crash_ID", "Person_ID", "Vehicle_ID"], 
    },
    "Person": {
        "schema": {
            "Person_ID": int,
            "Type": str,
            "Sex": str,
            "Age": int,
            "Safety_Equipment": str,
            "Airbag_Deployment_Status": str,
            "Driver_Action": str,
            "Driver_Vision": str,
            "Physical_Condition": str,
            "Injury_Classification": str,
            "BAC_Result": str,
            "City": str,
            "State": str,
        },
        "primary_key": "Person_ID",
        "non_nullable": [
            "Person_ID"
        ],
    }
}

def read_csv(file_path: str) -> Tuple[Union[List[Dict], str], Union[List[str], None]]:
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        tuple: (rows, fieldnames) where rows is either a list of dictionaries or error message,
            and fieldnames is a list of column names or None if error occurs
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
        return rows, reader.fieldnames
    except Exception as e:
        return f"Error loading file: {e}", None

def validate_columns(fieldnames: List[str], expected_schema: Dict) -> Union[str, None]:
    """
    Check if all expected columns are present in the CSV file.

    Args:
        fieldnames (list): List of column names from the CSV
        expected_schema (dict): Dictionary containing expected column names

    Returns:
        str or None: Error message if columns are missing, None if validation passes
    """
    missing_columns = set(expected_schema.keys()) - set(fieldnames)
    if missing_columns:
        return f"Missing columns: {missing_columns}"
    return None

def validate_non_nullable(rows: List[Dict], non_nullable: List[str]) -> Union[str, None]:
    """
    Check for null values in columns that should not be nullable.

    Args:
        rows (list): List of dictionaries containing the data
        non_nullable (list): List of column names that should not contain null values

    Returns:
        str or None: Error message with count of null values, None if validation passes
    """
    errors = {}
    for row in rows:
        for column in non_nullable:
            if not row[column]:
                errors[column] = errors.get(column, 0) + 1
    if errors:
        return f"Null values in non-nullable columns: {errors}"
    return None

def validate_primary_key(rows: List[Dict], primary_key: Union[str, List[str]]) -> Union[str, None]:
    """
    Validate primary key constraints, handling both single and composite keys.

    Args:
        rows (list): List of dictionaries containing the data
        primary_key (str or list): Column name(s) that form the primary key

    Returns:
        str or None: Error message if duplicates found, None if validation passes
    """
    if isinstance(primary_key, list):
        primary_key_values = [
            tuple(row[key] for key in primary_key)
            for row in rows
        ]
    else:
        primary_key_values = [row[primary_key] for row in rows]
    
    unique_keys = set(primary_key_values)
    duplicates = len(primary_key_values) - len(unique_keys)
    
    if duplicates > 0:
        return f"Duplicate primary keys: {duplicates} duplicates found"
    return None

def validate_data_types(rows: List[Dict], schema: Dict) -> Union[str, None]:
    """
    Validate that all values match their expected data types.

    Args:
        rows (list): List of dictionaries containing the data
        schema (dict): Dictionary mapping column names to their expected types

    Returns:
        str or None: Error message with count of type mismatches, None if validation passes
    """
    errors = {}
    for row in rows:
        for column, dtype in schema.items():
            try:
                if dtype == int:
                    int(row[column]) if row[column] else None
                elif dtype == float:
                    float(row[column]) if row[column] else None
                elif dtype == str:
                    str(row[column]) if row[column] else None
            except (ValueError, TypeError):
                errors[column] = errors.get(column, 0) + 1
    if errors:
        return f"Data type errors: {errors}"
    return None

def validate_table(table_name: str, file_path: str) -> Union[List[str], str]:
    """
    Perform all validations on a single table.

    Args:
        table_name (str): Name of the table to validate
        file_path (str): Path to the CSV file

    Returns:
        list or str: List of error messages if validation fails, success message if passes
    """
    table_info = SCHEMAS[table_name]
    schema = table_info["schema"]
    primary_key = table_info["primary_key"]
    non_nullable = table_info["non_nullable"]

    rows, fieldnames = read_csv(file_path)
    if isinstance(rows, str):  # Check if loading failed
        return rows

    validations = [
        validate_columns(fieldnames, schema),
        validate_non_nullable(rows, non_nullable),
        validate_primary_key(rows, primary_key),
        validate_data_types(rows, schema),
    ]

    # Collect and return all errors
    errors = [v for v in validations if v is not None]
    return errors if errors else f"{table_name} CSV is valid."

def main():
    """
    Main function to execute validation checks on all tables.
    """
    for table_name, file_path in FILE_PATHS.items():
        print(f"Validating {table_name}...")
        errors = validate_table(table_name, file_path)
        if isinstance(errors, str) and errors.endswith("valid."):
            print(errors)
        else:
            for error in errors:
                print(error)

if __name__ == "__main__":
    main()

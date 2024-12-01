from typing import List, Dict, Any

import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.read_write import to_csv
sys.path = original_sys_path

def selectColumns(data: List[List[Dict[str, Any]]], columns: List[str]) -> List[Dict[str, Any]]:
    """
    Filters the dataset to only include the specified columns.

    :param data: A list of lists of dictionaries representing the dataset.
    :param columns: A list of column names to retain.
    :return: A flattened list of dictionaries containing only the specified columns.
    """
    print("Filtering the dataset by columns", columns)
    # Initialize the result as a list of lists of dictionaries
    result = []
    
    for dataset in data:
        # Iterate through the list of dictionaries within each dataset
        for record in dataset:
            # Filter keys present in the columns
            filtered_record = {key: value for key, value in record.items() if key in columns}
            if filtered_record:  # Add if not empty
                result.append(filtered_record)

    return result

def createTableWithNoFK(
    original_df: List[Dict[str, str]], 
    new_csv: str, 
    index_column: str, 
    new_column_names: List[str], 
    original_column_names: List[str] = None,
    no_duplicate_rows: bool = True) -> List[Dict[str, str]]:
    """
    Creates a table with a unique index column and adds data from the original dataframe.

    Args:
        original_df (List[Dict[str, str]]): A list of dictionaries representing the original data.
        new_csv (str): The file path where the generated CSV will be saved.
        index_column (str): The name of the new index column for the table.
        new_column_names (List[str]): List of new column names for the table.
        original_column_names (List[str], optional): List of column names from the original data. Defaults to None.
        no_duplicate_rows (bool, optional): Whether to remove duplicate rows. Defaults to True.

    Returns:
        List[Dict[str, str]]: List of dictionaries representing the table rows.
    """
    print("Creating table with index column:", index_column)
    try:
        result = []
        seen_rows = set()  # To store unique rows
        index_id = 1
        
        if original_column_names is None:
            original_column_names = new_column_names
        
        for row in original_df:
            try:
                # Collect data for the current row
                row_data = tuple(row.get(col, row.get(col.upper())) for col in original_column_names)
                if no_duplicate_rows:
                    if row_data not in seen_rows:
                        result.append({
                            index_column: index_id,
                            **dict(zip(new_column_names, row_data))
                        })
                        seen_rows.add(row_data)
                        index_id += 1
                        
                else:
                    result.append({
                        index_column: index_id,
                        **dict(zip(new_column_names, row_data))
                    })
                    index_id += 1
                    
            except Exception as e:
                print(f"Error processing row {row}: {e}.")
                break
        
        to_csv(result, new_csv)
        
        return result
    
    except FileNotFoundError:
        print(f"Error: The file {new_csv} could not be found.")
        return None

def createDateTimeTable(
    all_dfs: List[Dict[str,Any]], 
    path: str,
    indexCol: str,
    DATETIME_COLUMNS: List[str],
    DATETIME_OG_COLUMNS: List[str],
    POLICE_NOTIFIED_COLUMNS: List[str]) -> List[Dict[str, str]]:
    """
    Creates a date-time table from a list of DataFrames and saves it as a CSV.

    Args:
        all_dfs (List[Dict[str, Any]]): A list of dictionaries containing date-time information.
        path (str): The file path where the dateTime CSV will be saved.
        indexCol (str): The name of the new index column for the dateTime table.
        DATETIME_COLUMNS (List[str]): List of datetime column names to process.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the dateTime table.
    """
    print("Creating dateTime table...")
    try:
        # Get all dates and transform them into the required format
        allDates = selectColumns(all_dfs, DATETIME_OG_COLUMNS) #list of dictionaries
        # Create an empty list to hold transformed date entries
        transformed_entries = []
        
        for date in allDates:
            police_notified = False
            
            crash_date = {
                "Day": date.get("DAY"),
                "Month": date.get("MONTH"),
                "Year": date.get("YEAR"),
                "Time": date.get("TIME")
            }
            
            if all(col in date for col in POLICE_NOTIFIED_COLUMNS):
                police_notified = True
                police_notified_date = {
                    "Day": date.get("DAY_POLICE_NOTIFIED"),
                    "Month": date.get("MONTH_POLICE_NOTIFIED"),
                    "Year": date.get("YEAR_POLICE_NOTIFIED"),
                    "Time": date.get("TIME_POLICE_NOTIFIED")
                }
 
  
            if police_notified and crash_date != police_notified_date:
                transformed_entries.append(police_notified_date)
                
            transformed_entries.append(crash_date)

        return createTableWithNoFK(
            original_df=transformed_entries,
            new_csv=path,
            index_column=indexCol,
            new_column_names=DATETIME_COLUMNS,
        )
        
    except ValueError as ve:
        raise Exception(f"ValueError: {ve}")
    except IOError as ioe:
        raise Exception(f"IOError: {ioe}")

def findIDFromTable(row: Dict[str, Any], columns: List[str], table: Dict[str, Dict[str, Any]], tablePrimaryKey: str) -> str:
    """
    Helper function to find the ID from a given table using a combination of column values.

    Args:
        row (Dict[str, str]): The current row from the crash data.
        columns (List[str]): The list of columns to be used for creating a unique key.
        table (Dict[str, Dict[str, str]]): The table to look for the ID in.
        tablePrimaryKey (str): The primary key of the table.

    Returns:
        str: The found ID.
    """

    columns_values = [str(row.get(col, row.get(col.upper(), ""))) for col in columns]

    key = " ".join(columns_values).strip()

    row_data = table[key]
    return row_data[tablePrimaryKey]

def createCrashTable(
    path: str,
    crashes_df: List[Dict[str, Any]],
    dateTimeTable: Dict[str, Dict[str, Any]],
    crashConditionTable: Dict[str, Dict[str, Any]],
    crashInjuriesTable: Dict[str, Dict[str, Any]],
    crashLocationTable: Dict[str, Dict[str, Any]],
    date_columns_mapping: List[str],
    police_notified_columns_mapping: List[str],
    crash_condition_columns_mapping: List[str],
    crash_injury_columns_mapping: List[str],
    crash_location_columns_mapping: List[str],
    idColumnName: str) -> Dict[str, Dict[str, str]]:
    """
    Creates a crash table by linking crash data to corresponding entries in related tables
    (date-time, crash conditions, injuries, and locations).

    Args:
        path (str): The file path where the generated CSV will be saved.
        crashes_df (List[Dict[str, str]]): The crash data in a list of dictionaries format.
        dateTimeTable (Dict[str, Dict[str, str]]): The date-time table, with DateTime_ID as keys.
        crashConditionTable (Dict[str, Dict[str, str]]): The crash condition table.
        crashInjuriesTable (Dict[str, Dict[str, str]]): The crash injuries table.
        crashLocationTable (Dict[str, Dict[str, str]]): The crash location table.
        date_columns_mapping (List[str]): Mapping for date columns in the crash data.
        police_notified_columns_mapping (List[str]): Mapping for police notified date columns.
        crash_condition_columns_mapping (List[str]): Mapping for crash condition columns.
        crash_injury_columns_mapping (List[str]): Mapping for crash injury columns.
        crash_location_columns_mapping (List[str]): Mapping for crash location columns.
        idColumnName (str): The name of the ID column in the crash data.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary representing the crash table.
    """
    result = []
    date_columns_mapping = [col.upper() for col in date_columns_mapping]
    index = 1
    for row in crashes_df:
        newRow = {}
        
        newRow["Crash_Date_ID"] = findIDFromTable(row, date_columns_mapping, dateTimeTable, "DateTime_ID")
        newRow["Police_Notified_Date_ID"] = findIDFromTable(row, police_notified_columns_mapping, dateTimeTable, "DateTime_ID")
        newRow["Crash_Condition_ID"] = findIDFromTable(row, crash_condition_columns_mapping, crashConditionTable, "Crash_Condition_ID")
        newRow["Injury_ID"] = findIDFromTable(row, crash_injury_columns_mapping, crashInjuriesTable, "Injury_ID")
        newRow["Crash_Location_ID"] = findIDFromTable(row, crash_location_columns_mapping, crashLocationTable, "Crash_Location_ID")
        
        newRow["Primary_Contributory_Cause"] = row["PRIM_CONTRIBUTORY_CAUSE"]
        newRow["Secondary_Contributory_Cause"] = row["SEC_CONTRIBUTORY_CAUSE"]
        newRow["Number_of_Units"] = row["NUM_UNITS"]
        newRow["Most_Severe_Injury"] = row["MOST_SEVERE_INJURY"]
        newRow["Difference_Between_Crash_Date_And_Police_Notified"] = row["DELTA_TIME_CRASH_DATE_POLICE_REPORT_DATE"]
        newRow["RD_NO"] = row["RD_NO"]


        result.append({idColumnName: index, **newRow})
        index +=1

    to_csv(result, path)

    return result

def createVehicleTable(
    path:str,
    vehicles_df: List[Dict[str, Any]],
    dateTimeTable: Dict[str, Dict[str, Any]],
    date_columns_mapping: List[str],
    idColumnName: str):
    seen = set()
    result = []

    index = 1
    date_columns_mapping = [col.upper() for col in date_columns_mapping]
    for row in vehicles_df:
        newRow = {}
        
        newRow["Date_ID"] = findIDFromTable(row, date_columns_mapping, dateTimeTable, "DateTime_ID")
        
        newRow["Unit_NO"] = row["UNIT_NO"]
        newRow["Unit_Type"] = row["UNIT_TYPE"]
        newRow["Make"] = row["MAKE"]
        newRow["Model"] = row["MODEL"]
        newRow["License_Plate_State"] = row["LIC_PLATE_STATE"]
        newRow["Year"] = row["VEHICLE_YEAR"]
        newRow["Defect"] = row["VEHICLE_DEFECT"]
        newRow["Vehicle_Type"] = row["VEHICLE_TYPE"]
        newRow["Vehicle_Use"] = row["VEHICLE_USE"]
        newRow["Travel_Direction"] = row["TRAVEL_DIRECTION"]
        newRow["Maneuver"] = row["MANEUVER"]
        newRow["Occupant_Count"] = row["OCCUPANT_CNT"]
        newRow["First_Contact_Point"] = row["FIRST_CONTACT_POINT"]
        newRow["VEHICLE_ID"] = row["VEHICLE_ID"]

        row_tuple = tuple(newRow[key] for key in sorted(newRow.keys()))
        if tuple(row_tuple) not in seen:
            seen.add(row_tuple)
            result.append({idColumnName: index, **newRow})
            index +=1

    to_csv(result, path)

    return result

def createDamageReimbursementTable(
    path: str,
    people_df: List[Dict[str, Any]],
    vehicleTable: Dict[str, Dict[str, Any]],
    crashTable: Dict[str, Dict[str, Any]],
    personTable: Dict[str, Dict[str, Any]],
    indexingColumnName: str) -> Dict[str, Dict[str, str]]:
    
    seen = set()
    result = []
    
    # Create lookup dictionaries
    person_lookup = {person["PERSON_ID"]: person["Person_ID"] for person in personTable.values()}
    crash_lookup = {crash["RD_NO"]: crash["Crash_ID"] for crash in crashTable.values()}
    vehicle_lookup = {vehicle["VEHICLE_ID"]: vehicle["Vehicle_ID"] for vehicle in vehicleTable.values()}

    index = 1
    for row in people_df:

        newRow = {}
        RD_NO = row["RD_NO"]
        PERSON_ID = row['PERSON_ID']
        VEHICLE_ID = row['VEHICLE_ID']
        
        newRow["Person_ID"] = person_lookup.get(PERSON_ID, None)
        newRow["Crash_ID"] = crash_lookup.get(RD_NO, None)
        newRow["Vehicle_ID"] = vehicle_lookup.get(VEHICLE_ID, None)
        newRow["Cost"] = row["DAMAGE"]
        newRow["Category"] = row["DAMAGE_CATEGORY"]
        
        row_tuple = tuple(newRow[key] for key in sorted(newRow.keys()))
        if tuple(row_tuple) not in seen:
            seen.add(row_tuple)
            result.append({indexingColumnName: index, **newRow})
            index +=1

    to_csv(result, path)
    
    return result

def removeColumns(
    vehicleTable: Dict[str, Dict[str, Any]],
    crashTable: Dict[str, Dict[str, Any]],
    personTable: Dict[str, Dict[str, Any]],
    columnsToRemove: List[str],
    paths: List[str],
    ):
    try:
        tables = [vehicleTable, crashTable, personTable]
        for index, table in enumerate(tables):
            if index < len(columnsToRemove):
                field = columnsToRemove[index]
                path = paths[index]
            for record in table.values():
                try:
                    if field in record:
                        del record[field]
                except KeyError as ke:
                        print(f"Key Error: {ke}")
                        break
                except Exception as e: 
                        print(f"Error : {e}")
                        break
            to_csv(table, path)
            index+=1
    except Exception as e:
        print(f"Error : {e}")
    
    print(f'Columns {columnsToRemove} removed successfully!')
    return 

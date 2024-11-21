from utils.read_write import to_csv
from utils.utils import concatenate_values
from typing import List, Dict, Any

def create_table_no_fk(
    original_df: List[Dict[str, str]], 
    new_csv: str, 
    index_column: str, 
    new_column_names: List[str], 
    original_column_names: List[str] = None
) -> List[List[str]]:
    """
    Creates a table with a unique index column and adds data from the original dataframe.

    Args:
        original_df (List[Dict[str, str]]): A list of dictionaries representing the original data.
        new_csv (str): The file path where the generated CSV will be saved.
        index_column (str): The name of the new index column for the table.
        new_column_names (List[str]): List of new column names for the table.
        original_column_names (List[str], optional): List of column names from the original data. Defaults to None.

    Returns:
        List[List[str]]: The table in list of lists format, including the new index column.
    """
    print("Creating table with key name:", index_column)
    try:
        # Initialize the table with the header
        table = [[index_column] + new_column_names]
        
        index_id = 1
        seen_rows = set()  # To store unique rows
        
        for row in original_df:
            try:
                if original_column_names is None:
                    original_column_names = new_column_names
                
                # Collect data for the current row
                row_data = tuple(row[col.upper()] for col in original_column_names)
                
                if row_data not in seen_rows:
                    table.append([index_id] + list(row_data))
                    seen_rows.add(row_data)
                    index_id += 1
                    
            except Exception as e:
                print(f"Error processing row {row}: {e}.")
                break
        
        to_csv(table, new_csv, True)
        
        return table
    
    except FileNotFoundError:
        print(f"Error: The file {new_csv} could not be found.")
        return None

def create_date_time_table(
    all_dates: List[Dict[str, str]], 
    path: str,
    indexCol: str
) -> Dict[str, Dict[str, str]]:
    """
    Creates a date-time table from a list of date dictionaries and saves it as a CSV.

    Args:
        all_dates (List[Dict[str, str]]): A list of dictionaries containing date details.
            Each dictionary should have the keys 'DAY', 'MONTH', 'YEAR', and 'TIME'.
        path (str): The file path where the generated CSV will be saved.
        indexCol (str): The name of the new index column for the table.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary representing the date-time table.

    Raises:
        ValueError: If a required key is missing in the input dictionaries.
        IOError: If there is an error writing the output to the CSV file.
    """
    print("Creating date-time table...")
    date_time_table = {}

    # Unique identifier for each unique date-time
    date_time_id = 1

    try:
        for date in all_dates:
            # Create a unique key for the date-time
            key = concatenate_values(date, indexCol)

            # Add to the table if the key doesn't exist
            if key not in date_time_table:
                date_time_table[key] = {
                    indexCol: date_time_id,
                    "Day": date.get('DAY', date.get("DAY_POLICE_NOTIFIED")),
                    "Month": date.get("MONTH", date.get("MONTH_POLICE_NOTIFIED")),
                    "Year": date.get("YEAR", date.get("YEAR_POLICE_NOTIFIED")),
                    "Time": date.get("TIME", date.get("TIME_POLICE_NOTIFIED")),
                }
                date_time_id += 1

        # Write the resulting table to a CSV
        to_csv(date_time_table, path)
    except ValueError as ve:
        raise Exception(f"Error: {ve}")
    except IOError as ioe:
        raise Exception(f"Failed to write to CSV: {ioe}")
    
    return date_time_table

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
    idColumnName: str
) -> Dict[str, Dict[str, str]]:
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
    seen = set()
    result = []

    index = 0
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

        row_tuple = tuple(newRow[key] for key in sorted(newRow.keys()))
        if tuple(row_tuple) not in seen:
            seen.add(row_tuple)
            result.append({idColumnName: index, **newRow})
            index +=1

    to_csv(result, path)

    return result

def createVehicleTable(
    path:str,
    vehicles_df: List[Dict[str, Any]],
    dateTimeTable: Dict[str, Dict[str, Any]],
    crashTable: Dict[str, Dict[str, Any]],
    date_columns_mapping: List[str],
    crash_columns_mapping: List[str],
    idColumnName: str
):
    seen = set()
    result = []

    index = 0
    for row in vehicles_df:
        newRow = {}
        
        newRow["Date_ID"] = findIDFromTable(row, date_columns_mapping, dateTimeTable, "DateTime_ID")
        # newRow["Crash_ID"] = findIDFromTable(row, crash_columns_mapping, crashTable, "Crash_ID")
        
        newRow["Unit_NO"] = row["UNIT_NO"]
        newRow["Unit_Type"] = row["UNIT_TYPE"]
        newRow["Make"] = row["MAKE"]
        newRow["Model"] = row["MODEL"]
        newRow["License_Plate_State"] = row["LIC_PLATE_STATE"]
        newRow["Year"] = row["VEHICLE_YEAR"]
        newRow["Defect"] = row["VEHICLE_DEFECT"]
        newRow["Type"] = row["VEHICLE_TYPE"]
        newRow["Use"] = row["VEHICLE_USE"]
        newRow["Travel_Direction"] = row["TRAVEL_DIRECTION"]
        newRow["Maneuver"] = row["MANEUVER"]
        newRow["Occupant_Count"] = row["OCCUPANT_CNT"]
        newRow["First_Contact_Point"] = row["FIRST_CONTACT_POINT"]

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
    person_columns_mapping: List[str],
    idColumnName: str
) -> Dict[str, Dict[str, str]]:
    
    seen = set()
    result = []

    index = 0
    for row in people_df:
        newRow = {}
        #TBD
    return result
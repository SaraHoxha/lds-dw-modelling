from utils.read_write import read_csv_v2, read_csv_v3
from utils.utils import select_columns
from utils.tables_creation import create_date_time_table, create_table_no_fk, createCrashTable, createVehicleTable

# INJURIES
CRASH_INJURY_FILE_PATH = 'Data Preparation/dw_tables_csv/Injury.csv'
CRASH_INJURY_INDEX_COL = 'Injury_ID'
CRASH_INJURY_COLUMNS = ['Injuries_Total', 'Injuries_Fatal', 'Injuries_Incapacitating', 'Injuries_Non_Incapacitating', 'Injuries_No_Indication', 'Injuries_Reported_Not_Evident', 'Injuries_Unknown']
# LOCATION
CRASH_LOCATION_FILE_PATH = 'Data Preparation/dw_tables_csv/CrashLocation.csv'
CRASH_LOCATION_INDEX_COL = 'Crash_Location_ID'
CRASH_LOCATION_NEW_COLUMNS = ['Street', 'Street_No', 'Street_Direction', 'Beat_Of_Occurrence', 'Latitude', 'Longitude', 'Location']
CRASH_LOCATION_OG_COLUMNS = ['Street_Name', 'Street_No', 'Street_Direction', 'Beat_Of_Occurrence', 'Latitude', 'Longitude', 'Location']
# CONDITION
CRASH_CONDITION_FILE_PATH = 'Data Preparation/dw_tables_csv/CrashCondition.csv'
CRASH_CONDITION_INDEX_COL = 'Crash_Condition_ID'
CRASH_CONDITION_NEW_COLUMNS = ['Posted_Speed_Limit', 'Traffic_Control_Device', 'Traffic_Control_Device_Condition', 'Weather_Condition', 'Lighting_Condition', 'Trafficway_Type', 'Roadway_Surface_Condition', 'Road_Defect', 'Alignment']
CRASH_CONDITION_OG_COLUMNS = ['Posted_Speed_Limit', 'Traffic_Control_Device', 'Device_Condition', 'Weather_Condition', 'Lighting_Condition', 'Trafficway_Type', 'Roadway_Surface_Cond', 'Road_Defect', 'Alignment']
# DATETIME
DATETIME_FILE_PATH = "Data Preparation/dw_tables_csv/DateTime.csv"
DATETIME_INDEX_COL = "DateTime_ID"
DATES_COLUMNS = ['DAY', 'MONTH', 'YEAR', 'TIME']
# PEOPLE
PEOPLE_FILE_PATH = 'Data Preparation/dw_tables_csv/Person.csv'
PEOPLE_INDEX_COL = 'Person_ID'
ORIGINAL_DF_COLUMNS = ["PERSON_TYPE","SEX","AGE", "SAFETY_EQUIPMENT","AIRBAG_DEPLOYED", "DRIVER_ACTION", "PHYSICAL_CONDITION", "INJURY_CLASSIFICATION", "BAC_RESULT", "CITY","STATE"]
NEW_DF_COLUMNS = ["Type", "Sex", "Age", "Safety_Equipment", "Airbag_Deployment_Status", "Driver_Action", "Physical_Condition", "Injury_Classification", "BAC_Result", "City", "State"]
#CRASHES
CRASH_FILE_PATH = 'Data Preparation/dw_tables_csv/Crash.csv'
CRASH_INDEX_COL = "Crash_ID"
CRASH_NEW_COLUMNS = ["Crash_Date_ID", "Police_Notified_Date_ID", "Crash_Condition_ID", "Injury_ID", "Crash_Location_ID", "Primary_Contributory_Cause", "Secondary_Contributory_Cause", "Number_of_Units", "Most_Severe_Injury", "Difference_Between_Crash_Date_And_Police_Notified"]
#VEHICLE
VEHICLE_FILE_PATH = 'Data Preparation/dw_tables_csv/Vehicle.csv'
VEHICLE_INDEX_COL = "Vehicle_ID"


# Read csvs
VEHICLES_DF = read_csv_v2('data/Vehicles_Processed.csv')
vehicle = createVehicleTable(
    VEHICLE_FILE_PATH,
    VEHICLES_DF,
    read_csv_v3(DATETIME_FILE_PATH, DATETIME_INDEX_COL),
    read_csv_v3(CRASH_FILE_PATH, CRASH_INDEX_COL),
    DATES_COLUMNS,
    CRASH_NEW_COLUMNS,
    VEHICLE_INDEX_COL
)


CRASH_DF = read_csv_v2('data/Crashes_Processed.csv')
PEOPLE_DF = read_csv_v2('data/People_Processed.csv')


crash_injuries_tab = create_table_no_fk(
    CRASH_DF,
    CRASH_INJURY_FILE_PATH,
    CRASH_INJURY_INDEX_COL,
    CRASH_INJURY_COLUMNS
)

crash_location_tab = create_table_no_fk(
    CRASH_DF,
    CRASH_LOCATION_FILE_PATH,
    CRASH_LOCATION_INDEX_COL,
    CRASH_LOCATION_NEW_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS
)

crash_condition_tab = create_table_no_fk(
    CRASH_DF,
    CRASH_CONDITION_FILE_PATH,
    CRASH_CONDITION_INDEX_COL,
    CRASH_CONDITION_NEW_COLUMNS,
    CRASH_CONDITION_OG_COLUMNS
)

# Concatenante all the dates
allDates = select_columns (
    PEOPLE_DF, DATES_COLUMNS
    ) + select_columns (
        VEHICLES_DF, DATES_COLUMNS
    ) + select_columns (
        CRASH_DF, DATES_COLUMNS
    ) + select_columns(
        CRASH_DF, [col + "_POLICE_NOTIFIED" for col in DATES_COLUMNS]
    )
dateTime_tab = create_date_time_table(allDates, DATETIME_FILE_PATH, DATETIME_INDEX_COL)

people_tab = create_table_no_fk(
    PEOPLE_DF,
    PEOPLE_FILE_PATH,
    PEOPLE_INDEX_COL,
    NEW_DF_COLUMNS,
    ORIGINAL_DF_COLUMNS
)

crash = createCrashTable(
    CRASH_FILE_PATH,
    CRASH_DF,
    read_csv_v3(DATETIME_FILE_PATH, DATETIME_INDEX_COL),
    read_csv_v3(CRASH_CONDITION_FILE_PATH, CRASH_CONDITION_INDEX_COL),
    read_csv_v3(CRASH_INJURY_FILE_PATH, CRASH_INJURY_INDEX_COL),
    read_csv_v3(CRASH_LOCATION_FILE_PATH, CRASH_LOCATION_INDEX_COL),
    DATES_COLUMNS,
    [col + "_POLICE_NOTIFIED" for col in DATES_COLUMNS],
    CRASH_CONDITION_OG_COLUMNS,
    CRASH_INJURY_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS,
    CRASH_INDEX_COL
)

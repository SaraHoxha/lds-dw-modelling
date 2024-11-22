from utils.read_write import read_csv
from utils.tables_creation_utils import *

# INJURY
INJURY_FILE_PATH = 'Data Preparation/dw_tables_csv/Injury.csv'
INJURY_INDEX_COL = 'Injury_ID'
INJURY_COLUMNS = ['Injuries_Total', 'Injuries_Fatal', 'Injuries_Incapacitating', 'Injuries_Non_Incapacitating', 'Injuries_No_Indication', 'Injuries_Reported_Not_Evident', 'Injuries_Unknown']

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
DATETIME_NEW_COLUMNS = ['Day', 'Month', 'Year', 'Time']
DATETIME_POLICE_COLUMNS = ['DAY_POLICE_NOTIFIED', 'MONTH_POLICE_NOTIFIED', 'YEAR_POLICE_NOTIFIED', 'TIME_POLICE_NOTIFIED']
DATETIME_OG_COLUMNS = [col.upper() for col in DATETIME_NEW_COLUMNS] + DATETIME_POLICE_COLUMNS
# PERSON
PERSON_FILE_PATH = 'Data Preparation/dw_tables_csv/Person.csv'
PERSON_INDEX_COL = 'Person_ID'
PERSON_OG_COLUMNS = ["PERSON_TYPE", "SEX","AGE", "SAFETY_EQUIPMENT","AIRBAG_DEPLOYED", "DRIVER_ACTION", "PHYSICAL_CONDITION", "INJURY_CLASSIFICATION", "BAC_RESULT", "CITY","STATE", "RD_NO"]
PERSON_NEW_COLUMNS = ["Type", "Sex", "Age", "Safety_Equipment", "Airbag_Deployment_Status", "Driver_Action", "Physical_Condition", "Injury_Classification", "BAC_Result", "City", "State", "RD_NO"]

#CRASH
CRASH_FILE_PATH = 'Data Preparation/dw_tables_csv/Crash.csv'
CRASH_INDEX_COL = "Crash_ID"
CRASH_NEW_COLUMNS = ["Crash_Date_ID", "Police_Notified_Date_ID", "Crash_Condition_ID", "Injury_ID", "Crash_Location_ID", "Primary_Contributory_Cause", "Secondary_Contributory_Cause", "Number_of_Units", "Most_Severe_Injury", "Difference_Between_Crash_Date_And_Police_Notified", 'RD_NO']

#VEHICLE
VEHICLE_FILE_PATH = 'Data Preparation/dw_tables_csv/Vehicle.csv'
VEHICLE_INDEX_COL = "Vehicle_ID"
VEHICLE_OG_COLUMNS = ['CRASH_UNIT_ID', 'CRASH_DATE','UNIT_NO','UNIT_TYPE','VEHICLE_ID','MAKE','MODEL','LIC_PLATE_STATE','VEHICLE_YEAR','VEHICLE_DEFECT','VEHICLE_TYPE','VEHICLE_USE','TRAVEL_DIRECTION','MANEUVER','OCCUPANT_CNT','FIRST_CONTACT_POINT', "RD_NO"]

#DAMAGE_REIMBURSEMENT
DAMAGE_REIMBURSEMENT_FILE_PATH = 'Data Preparation/dw_tables_csv/DamageReimbursement.csv'
DAMAGE_REIMBURSEMENT_COLUMNS = ['Person_ID','Vehicle_ID','Crash_ID', 'Cost', 'Cost_Category' ]
DAMAGE_REIMBURSEMENT_INDEX_COL = "Damage_Reimbursement_ID"

# READ DFs
#VEHICLES_DF = read_csv('data/Vehicles_Processed.csv')
#CRASH_DF = read_csv('data/Crashes_Processed.csv')
PEOPLE_DF = read_csv('data/People_Processed.csv')


# CREATE TABLES
'''
crashInjuriesTable  = createTableWithNoFK(
    CRASH_DF,
    INJURY_FILE_PATH,
    INJURY_INDEX_COL,
    INJURY_COLUMNS
)

crashLocationTable = createTableWithNoFK(
    CRASH_DF,
    CRASH_LOCATION_FILE_PATH,
    CRASH_LOCATION_INDEX_COL,
    CRASH_LOCATION_NEW_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS
)

crashConditionTable = createTableWithNoFK(
    CRASH_DF,
    CRASH_CONDITION_FILE_PATH,
    CRASH_CONDITION_INDEX_COL,
    CRASH_CONDITION_NEW_COLUMNS,
    CRASH_CONDITION_OG_COLUMNS
)

peopleTable = createTableWithNoFK(
    PEOPLE_DF,
    PERSON_FILE_PATH,
    PERSON_INDEX_COL,
    PERSON_NEW_COLUMNS,
    PERSON_OG_COLUMNS,
    no_duplicate_rows=False
)

dateTimeTable = createDateTimeTable(
    [PEOPLE_DF, VEHICLES_DF, CRASH_DF],
    DATETIME_FILE_PATH,
    DATETIME_INDEX_COL,
    DATETIME_NEW_COLUMNS,
    DATETIME_OG_COLUMNS,
    DATETIME_POLICE_COLUMNS
)
crash = createCrashTable(
    CRASH_FILE_PATH,
    CRASH_DF,
    read_csv(DATETIME_FILE_PATH, idColumn=DATETIME_INDEX_COL),
    read_csv(CRASH_CONDITION_FILE_PATH,idColumn= CRASH_CONDITION_INDEX_COL),
    read_csv(INJURY_FILE_PATH, idColumn=INJURY_INDEX_COL),
    read_csv(CRASH_LOCATION_FILE_PATH, idColumn=CRASH_LOCATION_INDEX_COL),
    DATETIME_NEW_COLUMNS,
    DATETIME_POLICE_COLUMNS,
    CRASH_CONDITION_OG_COLUMNS,
    INJURY_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS,
    CRASH_INDEX_COL
)

vehicle = createVehicleTable(
    VEHICLE_FILE_PATH,
    VEHICLES_DF,
    read_csv(DATETIME_FILE_PATH, idColumn=DATETIME_INDEX_COL),
    DATETIME_NEW_COLUMNS,
    VEHICLE_INDEX_COL
)
'''

damageReimbursement = createDamageReimbursementTable(
    DAMAGE_REIMBURSEMENT_FILE_PATH,
    PEOPLE_DF,
    read_csv(VEHICLE_FILE_PATH, idColumn=VEHICLE_INDEX_COL),
    read_csv(CRASH_FILE_PATH, idColumn=CRASH_INDEX_COL, no_duplicates=False),
    read_csv(PERSON_FILE_PATH, idColumn=PERSON_INDEX_COL, no_duplicates=False),
    idColumnName=DAMAGE_REIMBURSEMENT_INDEX_COL

)
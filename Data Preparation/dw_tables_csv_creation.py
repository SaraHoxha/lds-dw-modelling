from utils.tables_creation_utils import *

import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.read_write import read_csv
sys.path = original_sys_path

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
PERSON_OG_COLUMNS = ["PERSON_TYPE", "SEX","AGE", "SAFETY_EQUIPMENT","AIRBAG_DEPLOYED", "DRIVER_ACTION", "DRIVER_VISION","PHYSICAL_CONDITION", "INJURY_CLASSIFICATION", "BAC_RESULT", "CITY","STATE", "PERSON_ID"]
PERSON_NEW_COLUMNS = ["Type", "Sex", "Age", "Safety_Equipment", "Airbag_Deployment_Status", "Driver_Action", "Driver_Vision", "Physical_Condition", "Injury_Classification", "BAC_Result", "City", "State", "PERSON_ID"]

#CRASH
CRASH_FILE_PATH = 'Data Preparation/dw_tables_csv/Crash.csv'
CRASH_INDEX_COL = "Crash_ID"
CRASH_NEW_COLUMNS = ["Crash_Date_ID", "Police_Notified_Date_ID", "Crash_Condition_ID", "Injury_ID", "Crash_Location_ID", "Primary_Contributory_Cause", "Secondary_Contributory_Cause", "Number_of_Units", "Most_Severe_Injury", "Difference_Between_Crash_Date_And_Police_Notified", 'RD_NO']

#VEHICLE
VEHICLE_FILE_PATH = 'Data Preparation/dw_tables_csv/Vehicle.csv'
VEHICLE_INDEX_COL = "Vehicle_ID"
VEHICLE_OG_COLUMNS = ['CRASH_UNIT_ID', 'CRASH_DATE','UNIT_NO','UNIT_TYPE','VEHICLE_ID','MAKE','MODEL','LIC_PLATE_STATE','VEHICLE_YEAR','VEHICLE_DEFECT','VEHICLE_TYPE','VEHICLE_USE','TRAVEL_DIRECTION','MANEUVER','OCCUPANT_CNT','FIRST_CONTACT_POINT', "VEHICLE_ID"]

#DAMAGE_REIMBURSEMENT
DAMAGE_REIMBURSEMENT_FILE_PATH = 'Data Preparation/dw_tables_csv/DamageReimbursement.csv'
DAMAGE_REIMBURSEMENT_COLUMNS = ['Person_ID','Vehicle_ID','Crash_ID', 'Cost', 'Cost_Category' ]

# READ DFs
VEHICLES_DF = read_csv('data/Vehicles_Processed.csv')
CRASH_DF = read_csv('data/Crashes_Processed.csv')
PEOPLE_DF = read_csv('data/People_Processed.csv')


# CREATE TABLES

#Injury
createTableWithNoFK(
    CRASH_DF,
    INJURY_FILE_PATH,
    INJURY_INDEX_COL,
    INJURY_COLUMNS
)

#Read Injury Table
injuryTable = read_csv(INJURY_FILE_PATH, idColumn=INJURY_INDEX_COL)

#CrashLocation
createTableWithNoFK(
    CRASH_DF,
    CRASH_LOCATION_FILE_PATH,
    CRASH_LOCATION_INDEX_COL,
    CRASH_LOCATION_NEW_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS
)

#Read CrashLocation Table
crashLocationTable = read_csv(CRASH_LOCATION_FILE_PATH, idColumn=CRASH_LOCATION_INDEX_COL)

#CrashCondition
createTableWithNoFK(
    CRASH_DF,
    CRASH_CONDITION_FILE_PATH,
    CRASH_CONDITION_INDEX_COL,
    CRASH_CONDITION_NEW_COLUMNS,
    CRASH_CONDITION_OG_COLUMNS
)

#Read CrashCondition Table
crashConditionTable = read_csv(CRASH_CONDITION_FILE_PATH, idColumn=CRASH_CONDITION_INDEX_COL)

#Person
createTableWithNoFK(
    PEOPLE_DF,
    PERSON_FILE_PATH,
    PERSON_INDEX_COL,
    PERSON_NEW_COLUMNS,
    PERSON_OG_COLUMNS,
    no_duplicate_rows=False
)

personTable = read_csv(PERSON_FILE_PATH, idColumn=PERSON_INDEX_COL, no_duplicates=False)

#DateTime
createDateTimeTable(
    [PEOPLE_DF, VEHICLES_DF, CRASH_DF],
    DATETIME_FILE_PATH,
    DATETIME_INDEX_COL,
    DATETIME_NEW_COLUMNS,
    DATETIME_OG_COLUMNS,
    DATETIME_POLICE_COLUMNS
)

#Read DateTime Table
dateTimeTable = read_csv(DATETIME_FILE_PATH, idColumn=DATETIME_INDEX_COL)

#Crash
createCrashTable(
    CRASH_FILE_PATH,
    CRASH_DF,
    dateTimeTable,
    crashConditionTable,
    injuryTable,
    crashLocationTable,
    DATETIME_NEW_COLUMNS,
    DATETIME_POLICE_COLUMNS,
    CRASH_CONDITION_OG_COLUMNS,
    INJURY_COLUMNS,
    CRASH_LOCATION_OG_COLUMNS,
    CRASH_INDEX_COL
)

#Read Crash Table
crashTable = read_csv(CRASH_FILE_PATH, idColumn=CRASH_INDEX_COL)

#Vehicle
createVehicleTable(
    VEHICLE_FILE_PATH,
    VEHICLES_DF,
    dateTimeTable,
    DATETIME_NEW_COLUMNS,
    VEHICLE_INDEX_COL
)

#Read Vehicle Table
vehicleTable = read_csv(VEHICLE_FILE_PATH, idColumn=VEHICLE_INDEX_COL)

#DamageReimbursement
createDamageReimbursementTable(
    DAMAGE_REIMBURSEMENT_FILE_PATH,
    PEOPLE_DF,
    vehicleTable,
    crashTable,
    personTable
)

#Remove helpercolumns from tables
removeColumns(vehicleTable,
    crashTable,
    personTable,
    ['VEHICLE_ID', 'RD_NO', 'PERSON_ID'],
    [VEHICLE_FILE_PATH, CRASH_FILE_PATH, PERSON_FILE_PATH])

import csv
from utils.read_write import read_csv_v2
from utils.utils import create_table_file

CRASHES_DF = read_csv_v2('data/Crashes_Processed.csv')
PEOPLE_DF = read_csv_v2('data/People_Processed.csv')
VEHICLES_DF = read_csv_v2('data/Vehicles_Processed.csv')

INJURY_FILE_PATH = 'Data Preparation/dw_tables_csv/Injury.csv'
INJURY_INDEX_COL = 'Injury_ID'
INJURY_COLUMNS = ['Injuries_Total', 'Injuries_Fatal', 'Injuries_Incapacitating', 'Injuries_Non_Incapacitating', 'Injuries_No_Indication', 'Injuries_Reported_Not_Evident', 'Injuries_Unknown']

create_table_file(CRASHES_DF, INJURY_FILE_PATH, INJURY_INDEX_COL,  INJURY_COLUMNS)

CRASH_LOCATION_FILE_PATH = 'Data Preparation/dw_tables_csv/CrashLocation.csv'
CRASH_LOCATION_INDEX_COL = 'Crash_Location_ID'
CRASH_LOCATION_NEW_COLUMNS = ['Street', 'Street_No', 'Street_Direction', 'Beat_Of_Occurrence', 'Latitude', 'Longitude', 'Location']
CRASH_LOCATION_OG_COLUMNS = ['Street_Name', 'Street_No', 'Street_Direction', 'Beat_Of_Occurrence', 'Latitude', 'Longitude', 'Location']
create_table_file(CRASHES_DF, CRASH_LOCATION_FILE_PATH, CRASH_LOCATION_INDEX_COL, CRASH_LOCATION_NEW_COLUMNS, CRASH_LOCATION_OG_COLUMNS)


CRASH_CONDITION_FILE_PATH = 'Data Preparation/dw_tables_csv/CrashCondition.csv'
CRASH_CONDITION_INDEX_COL = 'Crash_Condition_ID'
CRASH_CONDITION_NEW_COLUMNS = ['Posted_Speed_Limit', 'Traffic_Control_Device', 'Traffic_Control_Device_Condition', 'Weather_Condition', 'Lighting_Condition', 'Trafficway_Type', 'Roadway_Surface_Condition', 'Road_Defect', 'Alignment']
CRASH_CONDITION_OG_COLUMNS = ['Posted_Speed_Limit','Traffic_Control_Device', 'Device_Condition', 'Weather_Condition', 'Lighting_Condition', 'Trafficway_Type', 'Roadway_Surface_Cond', 'Road_Defect', 'Alignment']

create_table_file(CRASHES_DF, CRASH_CONDITION_FILE_PATH, CRASH_CONDITION_INDEX_COL, CRASH_CONDITION_NEW_COLUMNS, CRASH_CONDITION_OG_COLUMNS)


from utils.dateTime import createDateTimeTable
from utils.utils import select_columns

DATETIME_FILE_PATH = "Data Preparation/dw_tables_csv/dateTime.csv"

# Concatenante all the dates
allDates = select_columns (
    PEOPLE_DF, ['YEAR', 'MONTH', 'DAY', 'TIME']
    ) + select_columns (
        VEHICLES_DF, ['YEAR', 'MONTH', 'DAY', 'TIME']
    ) + select_columns (
        CRASHES_DF, ['YEAR', 'MONTH', 'DAY', 'TIME']
    )

createDateTimeTable(allDates, DATETIME_FILE_PATH)

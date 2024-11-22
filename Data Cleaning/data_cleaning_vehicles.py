from utils.vehicles_utils import license_xx_to_u, typos_fixing, set_vehicle_year

import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.read_write import read_csv, to_csv
from general.utils import fill_missing_values, split_date
sys.path = original_sys_path


# Read "Vehicles csv"
vehicles_df = read_csv ('data/Vehicles.csv', 'CRASH_UNIT_ID')

# Fill missing values for columns that provide a default 'Unknown' value
column2defaultUknown = {
    'UNIT_TYPE': 'UNKNOWN',
    'LIC_PLATE_STATE': 'UNKNOWN',
    'MAKE': 'UNKNOWN',
    'MODEL': 'UNKNOWN',
    'VEHICLE_DEFECT': 'UNKNOWN',
    'VEHICLE_TYPE': 'UNKNOWN/NA',
    'VEHICLE_USE': 'UNKNOWN/NA',
    'TRAVEL_DIRECTION': 'UNKNOWN', 
    'MANEUVER': 'UNKNOWN',
    'FIRST_CONTACT_POINT': 'UNKNOWN'
}

vehicles_df_processed = fill_missing_values(vehicles_df, column2defaultUknown)

#Changing XX state to unknown
vehicles_df_processed = license_xx_to_u(vehicles_df_processed)

#Typos for brand and fixing them
typos_make = {'NEW HOLLAND, DIV. OF SPERRY NEW HOLLAND': 'NEW HOLLAND, (DIV. OF SPERRY NEW HOLLAND)',
    'AMC (LAWN & GARDEN TRACTORS BY AMERICAN MOTORS)': 'AMC (LAWN & GARDEN TRACTORS BY AMMERICAN MOTORS)',
    'ROLLS ROYCE': 'ROLLS-ROYCE'}

vehicles_df_processed = typos_fixing(vehicles_df_processed, typos_make,"MAKE")

#Typos for model and fixing them
typos_model = {'UNKNOWN':'UNKOWN'}

vehicles_df_processed = typos_fixing(vehicles_df_processed,typos_model,"MODEL")

#Fixing years of vehicles

vehicles_df_processed = set_vehicle_year(vehicles_df_processed)

#Splitting time into 
date_column = 'CRASH_DATE'
people_df_processed =  split_date(vehicles_df_processed, date_column)

#writing to csv
to_csv(vehicles_df_processed,'data/Vehicles_Processed.csv')
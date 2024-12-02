import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.read_write import read_csv, to_csv
from general.utils import split_date
sys.path = original_sys_path

from utils.crashes_utils import create_file_with_missing_location_values, fill_missing_location_values, fill_missing_BEAT_OF_OCCURRENCE, fix_license_plates, convert_float_columns_to_int_columns, add_delta_car_crash_date_police_report_date

#Read Crashes Table
crashes_df = read_csv ('data/Crashes.csv', 'RD_NO')

create_file_with_missing_location_values(crashes_df)

#Fill missing location values
crashes_df = fill_missing_location_values(crashes_df)

#Fill missing BEAT_OF_OCCURRENCE values
crashes_df = fill_missing_BEAT_OF_OCCURRENCE (crashes_df)

#Fix license plates
crashes_df = fix_license_plates(crashes_df)

#Convert float columns to int columns
crashes_df = convert_float_columns_to_int_columns(crashes_df)

#Add delta time between crash date and police report date
crashes_df = add_delta_car_crash_date_police_report_date(crashes_df)

#Split date columns
crashes_df = split_date (crashes_df, "CRASH_DATE")
crashes_df = split_date (crashes_df, "DATE_POLICE_NOTIFIED", "_POLICE_NOTIFIED")

#crashes_df = fill_missing_values_with_placeholder_string(crashes_df, "AMENDED", ['REPORT_TYPE'])
#crashes_df = fill_missing_values_with_placeholder_string(crashes_df, 'NO INDICATION OF INJURY', ["MOST_SEVERE_INJURY"])
#crashes_df = fill_missing_values_with_placeholder_string(crashes_df)

#Save processed crashes table to CSV
to_csv(crashes_df, "data/Crashes_Processed.csv")

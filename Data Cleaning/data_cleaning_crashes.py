import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)
from general.read_write import read_csv, to_csv
from general.utils import split_date
sys.path = original_sys_path


from utils.crashes_utils import create_file_with_missing_location_values, fill_missing_location_values, fill_missing_BEAT_OF_OCCURRENCE, fix_license_plates, convert_float_columns_to_int_columns, add_delta_car_crash_date_police_report_date


crashes_df = read_csv ('data/Crashes.csv', 'RD_NO')

create_file_with_missing_location_values(crashes_df)

crashes_df = fill_missing_location_values(crashes_df)

crashes_df = fill_missing_BEAT_OF_OCCURRENCE (crashes_df)

crashes_df = fix_license_plates(crashes_df)

crashes_df = convert_float_columns_to_int_columns(crashes_df)

crashes_df = add_delta_car_crash_date_police_report_date(crashes_df)

crashes_df = split_date (crashes_df, "CRASH_DATE")
crashes_df = split_date (crashes_df, "DATE_POLICE_NOTIFIED", "_POLICE_NOTIFIED")
#crashes_df = fill_missing_values_with_placeholder_string(crashes_df, "AMENDED", ['REPORT_TYPE'])
#crashes_df = fill_missing_values_with_placeholder_string(crashes_df, 'NO INDICATION OF INJURY', ["MOST_SEVERE_INJURY"])
#crashes_df = fill_missing_values_with_placeholder_string(crashes_df)

to_csv(crashes_df, "data/Crashes_Processed.csv")


"""
after all those modifications there are still the following missing data
REPORT_TYPE           4996
STREET_DIRECTION         2
STREET_NAME              1
BEAT_OF_OCCURRENCE       1
MOST_SEVERE_INJURY       7
LATITUDE                 1
LONGITUDE                1
LOCATION                 1

regarding the one missing value from latitude, longitude, location and street name
it is only one row which misses all of those field, therfore there is no way to find 
those missing values (the only location value that is present is the 
BEAT_OF_OCCURRENCE field but i do not know a way to go from there to a location point)

for the 7 values missing in the column MOST_SEVERE_INJURY i do not know how to fill those
values since i can't seem to find any correlation with the other INJURY columns or any other
so i would propose to leave them empty

STREET_DIRECTION does not contain much informations and there are only 2 values missing

BEAT_OF_OCCURRENCE i talked to the geospatial teachers and they told me that there is a way
using shapely to trace a polygon which circumscribes all the points that have the same 
beat of occurrence
since it is very hard even with the libraries and we can only apply modifications using
plain python AND there are only 1 value missing i would propose to leave this blank 
note: there were other values missing from the beat of occurrence column but i was 
able to fill them by finding the beat of occurrence of other rows where the locations 
(LATITUDE and LONGITUDE) matched (method fill_missing_BEAT_OF_OCCURRENCE)

we can fill all the missing values with the string unknown if neededm 
(fill_missing_values method)
"""
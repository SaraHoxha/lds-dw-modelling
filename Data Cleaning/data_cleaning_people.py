# Imports
from utils.people_utils import set_age_to_none, set_city_to_unknown, set_state_to_unknown, default_sex_to_U, set_driver_cols_to_none_for_passengers, fill_state_based_on_city

import sys
import os

original_sys_path = sys.path.copy()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from general.read_write import read_csv, to_csv
from general.utils import split_date, fill_missing_values

sys.path = original_sys_path

# Read "People csv"
people_df = read_csv ('data/People.csv', 'PERSON_ID')

# Fill missing values for columns that provide a default 'Unknown' value
column2defaultUknown = {
'CITY': 'UNKNOWN',
'SAFETY_EQUIPMENT': 'USAGE UNKNOWN',
'AIRBAG_DEPLOYED': 'DEPLOYMENT UNKNOWN',
'EJECTION': 'UNKNOWN',
'DRIVER_ACTION': 'UNKNOWN',
'DRIVER_VISION': 'UNKNOWN',
'PHYSICAL_CONDITION': 'UNKNOWN' 
}

people_df_processed = fill_missing_values(people_df, column2defaultUknown)

# Make following mapping for 'SEX' values: U & NaN values -> "U"(unknown)
people_df_processed = default_sex_to_U(people_df_processed)


# Add new value 'N/A' ('NON APPLICABLE') for observations that the person_type is passenger and we have missing values on columns that regard the driver ('DRIVER_VISION' & 'DRIVER_ACTION').
people_df_processed = set_driver_cols_to_none_for_passengers(people_df_processed)

# Set a  None ('') value for 'AGE' for observations when "AGE" < 10  and "PERSON_TYPE" is "DRIVER"
people_df_processed = set_age_to_none(people_df_processed)

# Split the 'CRASH_DATE' into 'DAY', 'MONTH', 'YEAR', 'TIME' columns
date_column = 'CRASH_DATE'
people_df_processed =  split_date(people_df_processed, date_column)

#Set 'CITY' column have the value 'Unknown' when 'city' has numeric value, length < 2 or starts with UNK
people_df_processed = set_city_to_unknown(people_df_processed)

# Use "CITY" column to determine "STATE" column when the latter is empty. 
us_cities_info = read_csv ('data/us_cities_info.csv', 'CITY')
people_df_processed = fill_state_based_on_city(people_df_processed, us_cities_info)

# Make 'STATE' column have the value 'Unknown' when 'CITY' is 'UNKNOWN' or STATE == 'XX'.
people_df_processed = set_state_to_unknown(people_df_processed)

# Save the processed data into a new file
to_csv(people_df_processed,'data/People_Processed.csv')
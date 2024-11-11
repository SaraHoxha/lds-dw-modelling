from fuzzywuzzy import process

PERSON_TYPE_COL = 'PERSON_TYPE'
DRIVER_VISION_COL = 'DRIVER_VISION'
DRIVER_ACTION_COL = 'DRIVER_ACTION'
SEX_COL = 'SEX'
CITY_COL = 'CITY'
STATE_COL = 'STATE'
AGE_COL = 'AGE'
PERSON_TYPE_VALUES = {'p':'PASSENGER', 
                      'd': 'DRIVER'}
SEX_COL_VALUES =['U']
VALUE_UNKNOWN = 'UNKNOWN'


# Make following mapping for 'SEX' values: U & NaN values -> "U"(unknown)
def default_sex_to_U(dataset):
    for row in dataset.values():
        if SEX_COL in row and row[SEX_COL] == '':
            row[SEX_COL] = SEX_COL_VALUES[0]
    return dataset

# Add new value 'N/A' ('NON APPLICABLE') for observations that the person_type is passenger and we have missing values on columns that regard the driver ('DRIVER_VISION' & 'DRIVER_ACTION')
def set_driver_cols_to_none_for_passengers(dataset):
    driver_cols = [DRIVER_ACTION_COL, DRIVER_VISION_COL]
    na_value = 'N/A'
    
    for row in dataset.values():
        if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('p'):
            for col in driver_cols:
                if col in row:
                    row[col] = na_value
    
    return dataset

# Set a  None ('') value for 'AGE' for observations when "AGE" < 10  and "PERSON_TYPE" is "DRIVER" (Anomalies)
def set_age_to_none(dataset):
    for row in dataset.values():
        if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('d'):
                if  row.get(AGE_COL):
                    if int(row[AGE_COL]) < 10:
                        row[AGE_COL] = ''
    return dataset
   
# Set 'STATE' column have the value 'Unknown' when 'CITY' is 'UNKNOWN' or STATE == 'XX'. 
def set_state_to_unknown(dataset):
    for row in dataset.values():
        if row.get(STATE_COL):
            if row.get(CITY_COL) == VALUE_UNKNOWN or row.get(STATE_COL) == 'XX':
                        row[STATE_COL] = VALUE_UNKNOWN
    return dataset
    
# Set 'CITY' column have the value 'Unknown' when 'city' has numeric value, length < 2 or starts with UNK
def set_city_to_unknown(dataset):
    for row in dataset.values():
        if row.get(CITY_COL):
            if isinstance(row[CITY_COL], (int, float)) or len(row[CITY_COL]) < 2 or (row[CITY_COL].startswith("UNK")):
                row[CITY_COL] = VALUE_UNKNOWN
    return dataset

# Use "CITY" column to determine "STATE" column when the latter is empty. 
def fill_state_based_on_city(dataset, city2state_mapping):
    for row in dataset.values():
        if row.get[STATE_COL] != VALUE_UNKNOWN:
            if row.get(CITY_COL) and city2state_mapping.get(row[CITY_COL]):
                row[STATE_COL] = city2state_mapping.get(row[CITY_COL])
    return dataset
PERSON_TYPE_COL = 'PERSON_TYPE'
DRIVER_VISION_COL = 'DRIVER_VISION'
DRIVER_ACTION_COL = 'DRIVER_ACTION'
SEX_COL = 'SEX'
CITY_COL = 'CITY'
STATE_COL = 'STATE'
AGE_COL = 'AGE'
RD_NO_COL = 'RD_NO'
DAMAGE_COL = 'DAMAGE'
DAMAGE_CATEGORY_COL = 'DAMAGE_CATEGORY'
STATE_ID_COL = 'STATE_ID'
PERSON_TYPE_VALUES = {'p':'PASSENGER', 'd': 'DRIVER'}
SEX_COL_VALUES =['U']
VALUE_UNKNOWN = 'UNKNOWN'
STATE_PLACEHOLDER_VALUE = 'XX'

# Make following mapping for 'SEX' values: U & NaN values -> "U"(unknown)
def default_sex_to_U(dataset):
    print ("Mapping sex values to U & NaN values")
    for row in dataset.values():
        try:
            if SEX_COL in row and row[SEX_COL] == '':
                row[SEX_COL] = SEX_COL_VALUES[0]
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

# Add new value 'N/A' ('NON APPLICABLE') for observations that the person_type is passenger and we have missing values on columns that regard the driver ('DRIVER_VISION' & 'DRIVER_ACTION')
def set_driver_cols_to_none_for_passengers(dataset):
    print ("Setting driver column to none for passengers")
    driver_cols = [DRIVER_ACTION_COL, DRIVER_VISION_COL]
    na_value = 'N/A'
    
    for row in dataset.values():
        try:
            if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('p'):
                for col in driver_cols:
                    if col in row:
                        row[col] = na_value
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

# Set a  None ('') value for 'AGE' for observations when "AGE" < 10  and "PERSON_TYPE" is "DRIVER" (Anomalies)
def set_age_to_none(dataset):
    print ("Setting age column to none when age is less then 10 and person type is driver")
    for row in dataset.values():
        try:
            if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('d'):
                    if row.get(AGE_COL) and isinstance(row[AGE_COL],int): 
                            if int(row[AGE_COL]) < 10:
                                row[AGE_COL] = ''
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset
   
# Set 'STATE' column have the value 'Unknown' when 'CITY' is 'UNKNOWN' or STATE == 'XX'. 
def set_state_to_unknown(dataset):
    print ("Setting state to Unknown when the city value is missing or not valid")
    for row in dataset.values():
        try:
            if row.get(CITY_COL) == VALUE_UNKNOWN or row.get(STATE_COL) == STATE_PLACEHOLDER_VALUE:
                        row[STATE_COL] = VALUE_UNKNOWN
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset
    
# Set 'CITY' column have the value 'Unknown' when 'city' has numeric value, length < 2 or starts with UNK
def set_city_to_unknown(dataset):
    print ("Setting city to Unknown when the city value is missing or not valid")
    for row in dataset.values():
        try:
            if row.get(CITY_COL):
                if isinstance(row[CITY_COL], (int, float)) or len(row[CITY_COL]) < 2 or (row[CITY_COL].startswith("UNK")):
                    row[CITY_COL] = VALUE_UNKNOWN
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

# Use "CITY" column to determine "STATE" column when the latter is empty. 
def fill_state_based_on_city(dataset, city2state_mapping):
    print ("Finding state using city")
    for row in dataset.values():
        try:
            if row.get(STATE_COL) != VALUE_UNKNOWN:
                if row.get(CITY_COL) and city2state_mapping.get(row[CITY_COL]):
                    row[STATE_COL] = city2state_mapping[row[CITY_COL]][STATE_ID_COL]
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

# SET 'DAMAGE' COLUMN TO 0  & DAMAGE_CATEGORY TO '$500 OR LESS' IF MISSING VALUES
def fill_missing_damage_and_category_values(dataset):
    print ("Setting damage and damage category to 0 and '$500 OR LESS' if missing")
    for row in dataset.values():
        try:
            if DAMAGE_COL in row and row.get(DAMAGE_COL) == '':
                row[DAMAGE_COL] = 0
                row[DAMAGE_CATEGORY_COL] = '$500 OR LESS'
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset


#SET RD_NO COLUMN TO UPPERCASE
def set_rd_no_to_uppercase(dataset):
    print ("Setting rd_no column to uppercase")
    for row in dataset.values():
        if RD_NO_COL in row:
            row[RD_NO_COL] = row[RD_NO_COL].upper()
    return dataset
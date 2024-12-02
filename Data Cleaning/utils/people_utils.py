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

def default_sex_to_U(dataset):
    """
    Maps 'SEX' column values to 'U' for unknown and NaN values.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with 'SEX' values mapped to 'U'.
    """
    print ("Mapping SEX values to U & NaN values.")
    for row in dataset.values():
        try:
            if SEX_COL in row and row[SEX_COL] == '':
                row[SEX_COL] = SEX_COL_VALUES[0]
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

def set_driver_cols_to_none_for_passengers(dataset):
    """
    Sets 'DRIVER_VISION' and 'DRIVER_ACTION' columns to 'N/A' for passengers.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with driver columns set to 'N/A' for passengers.
    """
    print ("Setting driver columns to none for passengers.")
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

def set_age_to_none(dataset):
    """
    Sets 'AGE' column to None ('') for drivers with age less than 10.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with 'AGE' set to None for anomalies.
    """
    print ("Setting AGE column to none when age is less then 10 and person type is driver.")
    for row in dataset.values():
        try:
            if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('d'):
                    if row.get(AGE_COL) and isinstance(row[AGE_COL],int): 
                            if int(row[AGE_COL]) < 10:
                                row[AGE_COL] = ''
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset
   
def set_state_to_unknown(dataset):
    """
    Sets 'STATE' column to 'UNKNOWN' when 'CITY' is 'UNKNOWN' or 'STATE' is 'XX' (placeholder value).

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with 'STATE' set to 'UNKNOWN' for invalid entries.
    """
    print ("Setting STATE to UNKNOWN when the CITY value is missing or not valid.")
    for row in dataset.values():
        try:
            if row.get(CITY_COL) == VALUE_UNKNOWN or row.get(STATE_COL) == STATE_PLACEHOLDER_VALUE:
                        row[STATE_COL] = VALUE_UNKNOWN
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset
    
def set_city_to_unknown(dataset):
    """
    Sets 'CITY' column to 'UNKNOWN' for invalid city values such as numeric values, length less than 2 or starts with UNK.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with 'CITY' set to 'UNKNOWN' for invalid entries.
    """
    print ("Setting CITY to UNKNOWN  when the city value is missing or not valid.")
    for row in dataset.values():
        try:
            if row.get(CITY_COL):
                if isinstance(row[CITY_COL], (int, float)) or len(row[CITY_COL]) < 2 or (row[CITY_COL].startswith("UNK")):
                    row[CITY_COL] = VALUE_UNKNOWN
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

def fill_state_based_on_city(dataset, city2state_mapping):
    """
    Fills 'STATE' column based on 'CITY' column when 'STATE' is empty.

    Args:
        dataset (dict): The dataset containing rows of data.
        city2state_mapping (dict): A mapping from city names to state IDs.

    Returns:
        dict: The updated dataset with 'STATE' filled based on 'CITY'.
    """
    print ("Finding STATE using CITY.")
    for row in dataset.values():
        try:
            if row.get(STATE_COL) != VALUE_UNKNOWN:
                if row.get(CITY_COL) and city2state_mapping.get(row[CITY_COL]):
                    row[STATE_COL] = city2state_mapping[row[CITY_COL]][STATE_ID_COL]
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset

def fill_missing_damage_and_category_values(dataset):
    """
    Sets 'DAMAGE' to 0 and 'DAMAGE_CATEGORY' to '$500 OR LESS' if missing.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with missing damage values filled.
    """
    print ("Setting DAMAGE and DAMAGE_CATEGORY to 0 and '$500 OR LESS' if missing.")
    for row in dataset.values():
        try:
            if DAMAGE_COL in row and row.get(DAMAGE_COL) == '':
                row[DAMAGE_COL] = 0
                row[DAMAGE_CATEGORY_COL] = '$500 OR LESS'
        except Exception as e:
            print(f"Error processing row: {row} | Error: {e}")
    return dataset


def set_rd_no_to_uppercase(dataset):
    """
    Sets 'RD_NO' column to uppercase.

    Args:
        dataset (dict): The dataset containing rows of data.

    Returns:
        dict: The updated dataset with 'RD_NO' set to uppercase.
    """
    print ("Setting RD_NO column to uppercase.")
    for row in dataset.values():
        if RD_NO_COL in row:
            row[RD_NO_COL] = row[RD_NO_COL].upper()
    return dataset
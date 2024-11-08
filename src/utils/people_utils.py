from opencage.geocoder import OpenCageGeocode
import time

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
API_KEY = '56f1c293199a4eb5a935b2ec8e4b3cd5'


def default_to_U_for_sex_column(dataset):
    for row in dataset.values():
        if SEX_COL in row and row[SEX_COL] == '':
            row[SEX_COL] = SEX_COL_VALUES[0]
    return dataset

def add_value_na_to_driver_cols_for_passengers(dataset):
    driver_cols = [DRIVER_ACTION_COL, DRIVER_VISION_COL]
    na_value = 'N/A'
    
    for row in dataset.values():
        if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('p'):
            for col in driver_cols:
                if col in row:
                    row[col] = na_value
    
    return dataset

def set_age_to_none_for_anomalies(dataset):
    for row in dataset.values():
        if row.get(PERSON_TYPE_COL) == PERSON_TYPE_VALUES.get('d'):
                if  AGE_COL in row and row[AGE_COL] < 10:
                    row[AGE_COL] = ''
    return dataset
    

def fill_state_column_based_on_city(dataset):
    city_values  = {row[CITY_COL] for row in dataset.values() if CITY_COL in row}
    city_2_state= create_city_2_state_dict(city_values)
    
    for row in dataset.values():
        if row.get(CITY_COL):
            row[STATE_COL] = city_2_state.get(row[CITY_COL])
    
    return dataset
    
def create_city_2_state_dict(city_values):
    geocoder = OpenCageGeocode(API_KEY)
    city_2_state = {}
    
    for city in city_values:
        try:
            result = geocoder.query(city)
            if result:
                state_code = result[0]['components'].get('state_code')
                if state_code:
                    city_2_state[city] = state_code
                else:
                    city_2_state[city] = ''  # No state code found
            else:
                city_2_state[city] = ''  # No result for this city
        except Exception as e:
            print(f"Error geocoding city {city}: {e}")
            city_2_state[city] = None        
    time.sleep(1) 
    
    return city_2_state
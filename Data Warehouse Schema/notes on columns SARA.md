## PEOPLE (modelled by PERSON table)
 'PERSON_ID', primary key for the table person
 'PERSON_TYPE', yes 
 'RD_NO', no not gonna be used 
 'VEHICLE_ID', foreign key that refers VEHICLE table
 'CRASH_DATE', foreign key that refers DATE table
 'DRIVER_ACTION',
 'DRIVER_VISION',
 'PHYSICAL_CONDITION',
 'BAC_RESULT',
 'SEX',  
 'AGE', 
 'INJURY_CLASSIFICATION',
 'SAFETY_EQUIPMENT',
 'AIRBAG_DEPLOYED',
 'EJECTION',
 <!--- The following two columns are removed as they're part of the Damage Reimbursement table -->
 'DAMAGE_CATEGORY', 
 'DAMAGE', 
  <!--- The following two columns will be part of the Location table and refered by FK Location_ID -->
 'CITY', 
 'STATE', 

### New columns
'Location_ID' -> foreign key that refers LOCATION table

## VEHICLES (modelled by VEHICLE table)
 'CRASH_UNIT_ID', foreign key that refers CRASH table
 'RD_NO', not gonna be used 
 'CRASH_DATE', foreign key that refers DATE table
 'FIRST_CONTACT_POINT'
 'UNIT_NO', 
 'UNIT_TYPE',
 'VEHICLE_ID',  (PK)
 'MAKE',  
 'MODEL', 
 'LIC_PLATE_STATE',
 'VEHICLE_YEAR', 
 'VEHICLE_DEFECT',
 'VEHICLE_TYPE',
 'VEHICLE_USE',
 'TRAVEL_DIRECTION', 
 'MANEUVER',
 'OCCUPANT_CNT',


### CRASHES (modelled by CRASH table)
 'RD_NO', no not gonna be used 
 'CRASH_DATE', foreign key that refers DATE table
 'FIRST_CRASH_TYPE',
 'REPORT_TYPE',
 'CRASH_TYPE',
 'DATE_POLICE_NOTIFIED', foreign key that refers DATE table
 'PRIM_CONTRIBUTORY_CAUSE',
 'SEC_CONTRIBUTORY_CAUSE',
 'NUM_UNITS',
 'MOST_SEVERE_INJURY',
 <!--- The following three columns will be part of the Injury table and refered by FK Injury_ID -->
 'INJURIES_TOTAL',
 'INJURIES_FATAL',
 'INJURIES_INCAPACITATING',
 'INJURIES_NON_INCAPACITATING',
 'INJURIES_REPORTED_NOT_EVIDENT',
 'INJURIES_NO_INDICATION',
 'INJURIES_UNKNOWN',
 <!--- The following three columns will be part of the DateTime table and refered by FK Date_ID -->
 'CRASH_HOUR',
 'CRASH_DAY_OF_WEEK',
 'CRASH_MONTH',
 <!--- The following three columns will be part of the Location table and refered by FK Location_ID -->
 'LATITUDE', 
 'LONGITUDE',
 'LOCATION', 
 'BEAT_OF_OCCURRENCE',
 'STREET_NO', 
 'STREET_DIRECTION',
 'STREET_NAME'
  <!--- All the following columns will be part of the Conditions table and refered by FK Condition_ID -->
 'POSTED_SPEED_LIMIT', 
 'TRAFFIC_CONTROL_DEVICE', 
 'DEVICE_CONDITION', 
 'WEATHER_CONDITION', 
 'LIGHTING_CONDITION',
 'TRAFFICWAY_TYPE',
 'ALIGNMENT',
 'ROADWAY_SURFACE_COND',
 'ROAD_DEFECT',
 
 ### New columns
 'CRASH_ID' PK
 'LOCATION_ID' FK
 'Injury_ID' FK
 'Condition_ID' FK


## INJURY TABLE
 'INJURIES_TOTAL',
 'INJURIES_FATAL',
 'INJURIES_INCAPACITATING',
 'INJURIES_NON_INCAPACITATING',
 'INJURIES_REPORTED_NOT_EVIDENT',
 'INJURIES_NO_INDICATION',
 'INJURIES_UNKNOWN',

## DATETIME TABLE
    DAY
    MONTH
    YEAR
    TIME


 ##  LOCATION TABLE 
 CITY
 STREET
 STREET NUMBER
 STREET DIRECTION
 BEAT OF OCCURRENCE
 LATITUDE
 LONGITUDE
 LOCATION


 ## DAMAGE REIMBURSEMENT TABLE
PK Damage_Reimbursement_ID
FK Person_ID
FK Crash_ID
FK Vehicle_ID
 'DAMAGE_CATEGORY', 
 'DAMAGE COST', 

 ## CRASH CONDITION TABLE
 PK Crash_Condition_ID
'POSTED_SPEED_LIMIT', 
 'TRAFFIC_CONTROL_DEVICE', 
 'DEVICE_CONDITION', 
 'WEATHER_CONDITION', 
 'LIGHTING_CONDITION',
 'TRAFFICWAY_TYPE',
 'ALIGNMENT',
 'ROADWAY_SURFACE_COND',
 'ROAD_DEFECT',

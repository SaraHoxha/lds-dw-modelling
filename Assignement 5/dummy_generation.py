import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Generate 300 rows of dummy data
n_rows = 2000

data = {
    'Crash_Location_ID': range(1, n_rows + 1),  # Unique IDs from 1 to 300
    'Street_No': np.random.randint(1, 9999, n_rows),
    'Street_Direction': np.random.choice(['N', 'S', 'E', 'W'], n_rows),
    'Beat_Of_Occurrence': np.random.randint(1001, 1999, n_rows),
    'Latitude': np.random.uniform(41.6400, 42.0200, n_rows),  # Chicago area coordinates
    'Longitude': np.random.uniform(-87.9400, -87.5200, n_rows),  # Chicago area coordinates
    'Location': [f"POINT ({long:.4f} {lat:.4f})" for long, lat in 
                zip(np.random.uniform(-87.9400, -87.5200, n_rows),
                    np.random.uniform(41.6400, 42.0200, n_rows))]
}

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('CrashLocation.csv', index=False)

print("CSV file 'CrashLocation.csv' has been created successfully!")

# Define possible values for categorical fields
traffic_devices = ['TRAFFIC SIGNAL', 'STOP SIGN', 'YIELD SIGN', 'NO CONTROLS', 'RAILROAD CROSSING GATE']
device_conditions = ['FUNCTIONING PROPERLY', 'NOT FUNCTIONING', 'MISSING', 'DAMAGED']
weather_conditions = ['CLEAR', 'RAIN', 'SNOW', 'FOG/SMOKE', 'SLEET/HAIL', 'SEVERE CROSS WIND']
lighting_conditions = ['DAYLIGHT', 'DARKNESS', 'DARKNESS, LIGHTED ROAD', 'DAWN', 'DUSK']
trafficway_types = ['DIVIDED', 'NOT DIVIDED', 'ONE-WAY', 'ALLEY', 'PARKING LOT']
surface_conditions = ['DRY', 'WET', 'SNOW OR SLUSH', 'ICE', 'SAND/MUD/DIRT']
road_defects = ['NO DEFECTS', 'POTHOLES', 'WORN SURFACE', 'SHOULDER DEFECT', 'DEBRIS ON ROADWAY']
alignments = ['STRAIGHT AND LEVEL', 'STRAIGHT ON GRADE', 'CURVE LEVEL', 'CURVE ON GRADE']

data = {
    'Crash_Condition_ID': range(1, n_rows + 1),
    'Posted_Speed_Limit': np.random.choice([20, 25, 30, 35, 40, 45, 50, 55], n_rows),
    'Traffic_Control_Device': np.random.choice(traffic_devices, n_rows),
    'Traffic_Control_Device_Condition': np.random.choice(device_conditions, n_rows),
    'Weather_Condition': np.random.choice(weather_conditions, n_rows),
    'Lighting_Condition': np.random.choice(lighting_conditions, n_rows),
    'Trafficway_Type': np.random.choice(trafficway_types, n_rows),
    'Roadway_Surface_Condition': np.random.choice(surface_conditions, n_rows),
    'Road_Defect': np.random.choice(road_defects, n_rows),
    'Alignment': np.random.choice(alignments, n_rows)
}

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('CrashCondition.csv', index=False)

print("CSV file 'CrashCondition.csv' has been created successfully!")
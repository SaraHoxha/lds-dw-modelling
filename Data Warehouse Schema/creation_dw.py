import pyodbc 

SERVER = 'tcp:lds.di.unipi.it' 
DATABASE = 'Group_ID_4_DB' 
USERNAME = 'Group_ID_4' 
PASSWORD = 'LN50IBLZ' 
DRIVER = '{ODBC Driver 17 for SQL Server}'

table2sql= {
        "CrashLocation": """
            CREATE TABLE CrashLocation (
                Crash_Location_ID INT PRIMARY KEY,
                Street_No INT,
                Street_Direction VARCHAR(1),
                Beat_Of_Occurrence INT,
                Latitude FLOAT,
                Longitude FLOAT,
                Location VARCHAR(100)
            )
        """,
        "CrashCondition": """
            CREATE TABLE CrashCondition (
                Crash_Condition_ID INT PRIMARY KEY,
                Posted_Speed_Limit INT,
                Traffic_Control_Device VARCHAR(50),
                Traffic_Control_Device_Condition VARCHAR(50),
                Weather_Condition VARCHAR(50),
                Lighting_Condition VARCHAR(50),
                Trafficway_Type VARCHAR(50),
                Roadway_Surface_Condition VARCHAR(50),
                Road_Defect VARCHAR(50),
                Alignment VARCHAR(50)
            )
        """,
        "Injury": """
            CREATE TABLE Injury (
                Injury_ID INT PRIMARY KEY,
                Injuries_Total INT,
                Injuries_Fatal INT,
                Injuries_Incapacitating INT,
                Injuries_Non_Incapacitating INT,
                Injuries_No_Indication INT,
                Injuries_Reported_Not_Evident INT,
                Injuries_Unknown INT
            )
        """,
        "DateTime": """
            CREATE TABLE DateTime (
                DateTime_ID INT PRIMARY KEY,
                Day INT,
                Month INT,
                Year INT,
                Time TIME
            )
        """,
        "Crash": """
            CREATE TABLE Crash (
                Crash_ID INT PRIMARY KEY,
                Crash_Date_ID INT,
                Police_Notified_Date_ID INT,
                Crash_Location_ID INT,
                Crash_Condition_ID INT,
                Injury_ID INT,
                Primary_Contributory_Cause VARCHAR(100),
                Secondary_Contributory_Cause VARCHAR(100),
                Number_of_Units INT,
                Most_Severe_Injury VARCHAR(100),
                Difference_Between_Crash_Date_And_Police_Notified INT,
                FOREIGN KEY (Crash_Date_ID) REFERENCES DateTime(DateTime_ID),
                FOREIGN KEY (Police_Notified_Date_ID) REFERENCES DateTime(DateTime_ID),
                FOREIGN KEY (Crash_Location_ID) REFERENCES CrashLocation(Crash_Location_ID),
                FOREIGN KEY (Crash_Condition_ID) REFERENCES CrashCondition(Crash_Condition_ID),
                FOREIGN KEY (Injury_ID) REFERENCES Injury(Injury_ID)
            )
        """,
        "Person": """
            CREATE TABLE Person (
                Person_ID INT PRIMARY KEY,
                Type VARCHAR(100),
                Sex VARCHAR(1),
                Age INT,
                Safety_Equipment VARCHAR(100),
                Airbag_Deployment_Status VARCHAR(100),
                Driver_Action VARCHAR(100),
                Driver_Vision VARCHAR(100),
                Physical_Condition VARCHAR(100),
                Injury_Classification VARCHAR(100),
                BAC_Result VARCHAR(100),
                City VARCHAR(100),
                State VARCHAR(100)
            )
        """,
        "Vehicle": """
            CREATE TABLE Vehicle (
                Vehicle_ID INT PRIMARY KEY,
                Date_ID INT,
                Crash_ID INT,
                Unit_NO INT,
                Unit_Type VARCHAR(50),
                Make VARCHAR(50),
                Model VARCHAR(50),
                License_Plate_State VARCHAR(2),
                Year INT,
                Defect VARCHAR(50),
                Vehicle_Type VARCHAR(50),
                Vehicle_Use VARCHAR(50),
                Travel_Direction VARCHAR(50),
                Maneuver VARCHAR(50),
                Occupant_Count INT,
                First_Contact_Point VARCHAR(50),
                FOREIGN KEY (Date_ID) REFERENCES DateTime(DateTime_ID),
                FOREIGN KEY (Crash_ID) REFERENCES Crash(Crash_ID)
            )
        """,
        "DamageReimbursement": """
            CREATE TABLE DamageReimbursement (
                Damage_Reimbursement_ID INT PRIMARY KEY,
                Crash_ID INT,
                Person_ID INT,
                Vehicle_ID INT,
                Cost FLOAT,
                Category VARCHAR(100),
                FOREIGN KEY (Crash_ID) REFERENCES Crash(Crash_ID),
                FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID),
                FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
            )
        """
    }
def create_connection():
    return pyodbc.connect(
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD}'
    )


with create_connection() as connection:
    cursor = connection.cursor()

    try:
        for table_name, sql_statement in table2sql.items():
            try:
                print(f"Creating table {table_name}...")
                cursor.execute(sql_statement)
                print(f"Table '{table_name}' created successfully.")
            except pyodbc.Error as e:
                print(f"Error creating table '{table_name}':", e)
                raise
        
        # Commit all changes if table creation was successful
        connection.commit()
        print("All tables committed successfully.")

    except pyodbc.Error as e:
        connection.rollback()
        print("Error in committing the changes; transaction has been rolled back:", e)
#For now im creating the skeleton of the code
#Creating it with dummy data

#ID: Group_ID_4
#PW: LN50IBLZ
#DB: Group_ID_4_DB

#Importing the libraries
import pyodbc
import sys
import os
from utils.read_write import read_csv
from utils.utils import check_csv_files, check_existing_table, validate_schema

#Folder path
folder_path = os.path.join(os.getcwd(),'Data Preparation','dw_tables_csv')

#CSV table names and primary keys, CHANGE WHEN NEEDED
csv_tables_dict = [
    {'Name': 'CrashLocation.csv', 'Primary_Key': 'Crash_Location_ID'},
    {'Name': 'CrashCondition.csv', 'Primary_Key': 'Crash_Condition_ID'},
    {'Name': 'Injury.csv', 'Primary_Key': 'Injury_ID'},
    {'Name': 'dateTime.csv', 'Primary_Key': 'DateTime_ID'},
    {'Name': 'Person.csv', 'Primary_Key': 'Person_ID'},
    #crash
    #vehicle
    #damage_reimbursement
    
]

#Check if the csv files exist
try:
    check_csv_files(folder_path,csv_tables_dict)
    print("CSV files exist and are non empty")

except (FileNotFoundError, OSError) as e:
    print(f"Error: {e}")
    sys.exit(1)

#Connecting to the database
server = 'tcp:lds.di.unipi.it' 
database = 'Group_ID_4_DB' 
username = 'Group_ID_4' 
password = 'LN50IBLZ' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password

try:
    # Connection
    cnxn = pyodbc.connect(connectionString)
    
    # Wrap everything in a transaction
    for table in csv_tables_dict:
        with cnxn:
            try:
                with cnxn.cursor() as cursor:
                    # Sanitize table name
                    table_name = table['Name'].replace(';', '').replace('--', '')
                    table_name_db = table_name.replace('.csv', '')
                    
                    # Use proper path joining
                    csv_path = os.path.join(folder_path, table_name)
                    
                    # Reading the csv file
                    data_table = read_csv(csv_path, table['Primary_Key'])
                    
                    # Validate schema
                    validate_schema(cursor, table_name_db, data_table)
                    
                    # Check if table exists and has identical data
                    table_exists, data_identical = check_existing_table(cursor, table_name_db, data_table)
                    
                    if table_exists and data_identical:
                        print(f"Table {table_name_db} already exists with identical data. Skipping...")
                        continue
                    elif table_exists:
                        print(f"Table {table_name_db} exists but has different data. Proceeding with update...")
                        # Delete existing data
                        cursor.execute(f"DELETE FROM {table_name_db}")
                    
                    # Query to insert the data
                    columns = list(data_table['1'].keys())
                    placeholders = ','.join(['?' for _ in columns])
                    columns_str = ','.join(columns)

                    # Create dynamic SQL query
                    sql = f"INSERT INTO {table_name_db}({columns_str}) VALUES({placeholders})"

                    # Consider batch processing for inserts
                    batch_size = 1000
                    rows_to_insert = []
                    i = 0
                    for key, row_dict in data_table.items():
                        values = tuple(row_dict[col] for col in columns)
                        rows_to_insert.append(values)
                        if len(rows_to_insert) >= batch_size:
                            cursor.executemany(sql, rows_to_insert)
                            i += 1
                            print(f"Inserted {i} batche(s) of {batch_size} rows")
                            rows_to_insert = []
                    
                    if rows_to_insert:  # Insert remaining rows
                        cursor.executemany(sql, rows_to_insert)
                    
            except pyodbc.Error as e:
                raise Exception(f"Error processing table {table_name}: {str(e)}")
                
except pyodbc.Error as e:
    print(f"Database error: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    sys.exit(1)
finally:
    if 'cnxn' in locals():
        cnxn.close()

print("Data uploaded successfully")
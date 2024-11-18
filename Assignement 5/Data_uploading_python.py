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
folder_path = '../data/dw_csv_files'

#CSV table names and primary keys, CHANGE WHEN NEEDED
csv_tables_dict = [
    {'Name': 'csv_table_1.csv', 'Primary_Key': 'id_1'},
    {'Name': 'csv_table_2.csv', 'Primary_Key': 'id_2'},
    {'Name': 'csv_table_3.csv', 'Primary_Key': 'id_3'}
]

#Check if the csv files exist
try:
    check_csv_files(folder_path)
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
                    
                    # Use proper path joining
                    csv_path = os.path.join(folder_path, table_name)
                    
                    # Reading the csv file
                    data_table = read_csv(csv_path, table['Primary_Key'])
                    
                    # Validate schema
                    validate_schema(cursor, table_name, data_table)
                    
                    # Check if table exists and has identical data
                    table_exists, data_identical = check_existing_table(cursor, table_name, data_table)
                    
                    if table_exists and data_identical:
                        print(f"Table {table_name} already exists with identical data. Skipping...")
                        continue
                    elif table_exists:
                        print(f"Table {table_name} exists but has different data. Proceeding with update...")
                    
                    # Query to insert the data
                    columns = list(data_table['1'].keys())
                    placeholders = ','.join(['?' for _ in columns])
                    columns_str = ','.join(columns)

                    # Create dynamic SQL query
                    sql = f"INSERT INTO {table_name}({columns_str}) VALUES({placeholders})"

                    # Consider batch processing for inserts
                    batch_size = 1000
                    rows_to_insert = []
                    for key, row_dict in data_table.items():
                        values = tuple(row_dict[col] for col in columns)
                        rows_to_insert.append(values)
                        if len(rows_to_insert) >= batch_size:
                            cursor.executemany(sql, rows_to_insert)
                            rows_to_insert = []
                    
                    if rows_to_insert:  # Insert remaining rows
                        cursor.executemany(sql, rows_to_insert)
                    
            except pyodbc.Error as e:
                print(f"Error processing table {table_name}: {str(e)}")
                raise  # Re-raise to rollback transaction
                
except pyodbc.Error as e:
    print(f"Database error: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    sys.exit(1)
finally:
    if 'cnxn' in locals():
        cnxn.close()

""" 
#(I dont think this is needed)
for table in csv_tables_dict:
    #Creating the cursor
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT * FROM {table['Name']};") 
    rows = cursor.fetchall() 
    #print(rows)
    #Closing the cursor
    cursor.close()


#Closing the connection
cnxn.close() """
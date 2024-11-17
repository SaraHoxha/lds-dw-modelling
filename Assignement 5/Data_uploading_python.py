#For now im creating the skeleton of the code
#Creating it with dummy data

#ID: Group_ID_4
#PW: LN50IBLZ
#DB: Group_ID_4_DB

#Importing the libraries
import pyodbc
import sys
from utils.read_write import read_csv
from utils.utils import check_csv_files, check_existing_table

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
cnxn = pyodbc.connect(connectionString)

#Data table should run through all the csv files in the folder and do the following process from here.
#Loading the data as List of dictionaries
for table in csv_tables_dict:
    #Creating the cursor
    cursor = cnxn.cursor()
    
    try:
        data_table = read_csv('data/dw_csv_files'+ str(table['Name']), table['Primary_Key'])
        
        # Check if table exists and has identical data
        table_exists, data_identical = check_existing_table(cursor, table['Name'], data_table)
        
        if table_exists and data_identical:
            print(f"Table {table['Name']} already exists with identical data. Skipping...")
            continue
        elif table_exists:
            print(f"Table {table['Name']} exists but has different data. Proceeding with update...")
        
        # Query to insert the data
        columns = list(data_table['1'].keys())
        placeholders = ','.join(['?' for _ in columns])
        columns_str = ','.join(columns)

        # Create dynamic SQL query
        sql = f"INSERT INTO {table['Name']}({columns_str}) VALUES({placeholders})"

        # Insert data (This loop is nested inside of the loop that goes through all the csv files)
        for key, row_dict in data_table.items():
            values = tuple(row_dict[col] for col in columns)
            cursor.execute(sql, values)

        #Committing the changes
        cnxn.commit()

    except pyodbc.Error as e:
        print(f"Error processing table {table['Name']}: {str(e)}")
        continue
    finally:
        cursor.close()


#Rename table with a loop of names of the csv files (I dont think this is needed)
for table in csv_tables_dict:
    #Creating the cursor
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT * FROM {table['Name']};") 
    rows = cursor.fetchall() 
    #print(rows)
    #Closing the cursor
    cursor.close()


#Closing the connection
cnxn.close()
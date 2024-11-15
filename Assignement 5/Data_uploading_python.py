#For now im creating the skeleton of the code
#Creating it with dummy data

#ID: Group_ID_4
#PW: LN50IBLZ
#DB: Group_ID_4_DB

#Importing the libraries
import pyodbc
import os
from utils.read_write import read_csv
from utils.utils import check_csv_files

#Folder path
folder_path = 'data/dw_csv_files'

#CSV table names
csv_tables_dict = {
    {'Name': 'csv_table_1.csv', 'Primary_Key': 'id'},
    {'Name': 'csv_table_2.csv', 'Primary_Key': 'id'},
    {'Name': 'csv_table_3.csv', 'Primary_Key': 'id'}
}

#Check if the csv files exist
try:
    check_csv_files(folder_path)

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

#Creating the cursor
cursor = cnxn.cursor()

#Loop starts here
#Data table should run through all the csv files in the folder and do the following process from here.
#Loading the data as List of dictionaries
##......Complete this part
data_table = read_csv('data/dw_csv_files'+ str(csv_tables_dict[i]['Name']), csv_tables_dict[i]['Primary_Key'])

#Query to insert the data
# Get column names from the first dictionary in data_table
columns = list(data_table[0].keys())
placeholders = ','.join(['?' for _ in columns])
columns_str = ','.join(columns)

# Create dynamic SQL query
sql = f"INSERT INTO {csv_tables_dict[i]['Name']}({columns_str}) VALUES({placeholders})"

# Insert data (This loop is nested inside of the loop that goes through all the csv files)
for key, row_dict in data_table.items():
    values = tuple(row_dict[col] for col in columns)
    cursor.execute(sql, values)

#Committing the changes
cnxn.commit()

#Closing the cursor and the connection
cursor.close()
cnxn.close()

#Loop ends here

#Rename table with a loop of names of the csv files
cursor.execute(f"SELECT * FROM {csv_tables_dict[i]['Name']};") 

rows = cursor.fetchall() 
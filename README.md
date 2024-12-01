# Laboratory of Data Science Project
This repository contains code/report prepared for our project  for the "Laboratory of Data Science" course at University of Pisa.

For this project, we were provided with the Chicago Crashes dataset which included three files:
1. `People.csv`: It provides detailed information about individuals involved in traffic crashes in Chicago. It includes information such as person's address of residence, their age, their actions during the crash, and their physical condition and subsequent compensation they have to receive.
2. `Vehicles.csv`: Provides comprehensive information about  vehicles involved in crashes in Chicago. Each record in this table represents a distinct unit involved in a crash, with multiple units potentially being involved in the same incident.  
3. `Crashes.csv`: Provides comprehensive information about crashes that have occurred in Chicago. It includes information such as the location, time, road conditions, weather conditions etc.

Based on this data, we were asked to perform data cleaning, data warehouse modelling, and SSIS queries.

## Project Structure

The project is organized into the following directories:

### 1. **Data Understanding**
   - Assignment 1
   -  **Purpose**: This folder contains contains the Jupyter Notebook files used to explore the three CSVs
       
### 2. **Data Cleaning**
   - Assignment 2
   - **Purpose**: This folder contains all the python files that perform data cleaning, including filling missing values, removing duplicates, and fixing any errors/misspellings. The three processed files are saved as: `People_Processed.csv`, `Vehicles_Processed.csv`, `Crashes_Processed.csv`.

### 3. **Data Warehouse Schema**
 - Assignment 3
 - **Purpose**: This folder contains the Data Warehouse schema we have designed saved in both drawio and png format. It can be found [here](./Data%20Warehouse%20Schema/DW%20Schema.png). It also contains the python script `creation_dw.py` to create the tables based on this schema, as well as the `creation_dw_SSIS.py` to duplicate the tables without records.

### 4. **Data Preparation**
 - Assignment 4
 - **Purpose**: This folder contains the python script `dw_tables_csv_creation.py` that splits the three intiail csv files into different files, one for each table
in the schema proposed.

### 5. **Data Uploading with Python**
 - Assignment 5
 - **Purpose**: This folder containes the python script `Data_uploading_python.py` that populates the database Group_ID_4_DB according to the schema relations with all the csv files prepared in Data Preparation.

### 6. **SSIS-Tasks**
 - Assignment 6, 6a - 9a
 - **Purpose**: This folder containes the all the SSIS packages in one Visual Studio solution.
 -  `Data Uploading.dtsx`: SSIS package that duplicates each table without the records, renaming them as TABLENAME_SSIS and populates the new set of tables with 10% of the data in the original tables.
 -  `Query_6.dtsx`: SSIS package that implements query 6a.
 -  `Query_7.dtsx`: SSIS package that implements query 7a.
 -  `Query_8.dtsx`: SSIS package that implements query 8a.
 -  `Query_9.dtsx`: SSIS package that implements query 9a.



import os
import pyodbc


def check_csv_files(folder_path, csv_tables_dict):
    # Get all CSV files in the folder
    if csv_tables_dict is None:
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    # If specified get only the files specified in the dictionary
    else:
        csv_files = [f['Name'] for f in csv_tables_dict]
    
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the specified folder")
    
    # Check if files are not empty
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        if os.path.getsize(file_path) == 0:
            raise OSError(f"CSV file '{csv_file}' is empty")
            
    return True

def check_existing_table(cursor, table_name: str, new_data: dict) -> tuple[bool, bool]:
    """
    Check if a table exists and compare its contents with new data.
    
    Args:
        cursor: pyodbc cursor object
        table_name: Name of the table to check
        new_data: Dictionary containing the new data to compare
        
    Returns:
        tuple[bool, bool]: (table_exists, data_identical)
    """
    try:
        # Remove .csv extension if present
        clean_table_name = table_name.replace('.csv', '')
        
        # Check if table exists
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = '{clean_table_name}'
        """)
        table_exists = cursor.fetchone()[0] > 0

        if not table_exists:
            return False, False

        # Get data from existing table
        cursor.execute(f"SELECT * FROM {clean_table_name}")
        existing_data = cursor.fetchall()
        
        # Get column names
        columns = [column[0] for column in cursor.description]
        
        # Convert existing data to set of tuples for comparison
        existing_set = set(tuple(row) for row in existing_data)
        
        # Convert new data to set of tuples
        new_data_set = set(
            tuple(row_dict[col] for col in columns)
            for key, row_dict in new_data.items()
        )
        
        return True, existing_set == new_data_set

    except pyodbc.Error as e:
        print(f"Error checking table {table_name}: {str(e)}")
        raise

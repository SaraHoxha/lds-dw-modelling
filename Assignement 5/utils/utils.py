
import os

def check_csv_files(folder_path):
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the specified folder")
    
    # Check if files are not empty
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        if os.path.getsize(file_path) == 0:
            raise OSError(f"CSV file '{csv_file}' is empty")
            
    return True
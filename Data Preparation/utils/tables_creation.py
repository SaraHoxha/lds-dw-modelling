from utils.read_write import to_csv
from utils.utils import concatenate_values
from typing import List, Dict
import csv

def create_table(original_df, new_csv, index_column, new_column_names, original_column_names=None):
    print ("Creating table with key name:", index_column)
    try:
        with open(new_csv, "w", newline="") as out_file:
            writer = csv.writer(out_file)
            # Write header for the table
            writer.writerow([index_column] + new_column_names)
            
            index_id = 1
            seen_rows = set()  # To store unique rows
            
            for row in original_df:
                try:
                    if original_column_names is None:
                        original_column_names = new_column_names
                    
                    row_data = tuple(row[col.upper()] for col in original_column_names)
                    
                    if row_data not in seen_rows:
                        writer.writerow([index_id] + list(row_data))
                        seen_rows.add(row_data)
                        index_id += 1
                        
                except Exception as e:
                    print(f"Error processing row {row}: {e}.")
                    break
    except FileNotFoundError:
        print(f"Error: The file {new_csv} could not be found.")
    except Exception as e:
        print(f"Error while creating table: {e}")


def create_date_time_table(all_dates: List[Dict[str, str]], path: str) -> None:
    """
    Creates a date-time table from a list of date dictionaries and saves it as a CSV.

    Args:
        all_dates (List[Dict[str, str]]): A list of dictionaries containing date details.
            Each dictionary should have the keys 'DAY', 'MONTH', 'YEAR', and 'TIME'.
        path (str): The file path where the generated CSV will be saved.

    Raises:
        ValueError: If a required key is missing in the input dictionaries.
        IOError: If there is an error writing the output to the CSV file.
    """
    print("Creating date-time table...")
    date_time_table = {}

    # Unique identifier for each unique date-time
    date_time_id = 1

    try:
        for date in all_dates:
            # Create a unique key for the date-time
            key = concatenate_values(date, "DateTime_ID")

            # Add to the table if the key doesn't exist
            if key not in date_time_table:
                date_time_table[key] = {
                    "DateTime_ID": date_time_id,
                    "Day": date.get('DAY', date.get("DAY_POLICE_NOTIFIED")),
                    "Month": date.get("MONTH", date.get("MONTH_POLICE_NOTIFIED")),
                    "Year": date.get("YEAR", date.get("YEAR_POLICE_NOTIFIED")),
                    "Time": date.get("TIME", date.get("TIME_POLICE_NOTIFIED")),
                }
                date_time_id += 1

        # Write the resulting table to a CSV
        to_csv(date_time_table, path)
    except ValueError as ve:
        raise Exception(f"Error: {ve}")
    except IOError as ioe:
        raise Exception(f"Failed to write to CSV: {ioe}")\


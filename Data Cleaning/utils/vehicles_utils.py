LICENCE_PLATE = "LIC_PLATE_STATE"
MAKE = "MAKE"
VEHICLE_YEAR = "VEHICLE_YEAR"

def license_xx_to_u(dataset):
    """
    Maps 'LIC_PLATE_STATE' values of 'XX' to 'UNKNOWN' in the given dataset.

    Args:
        dataset (dict): A dictionary where each key is a unique identifier and each value is a dictionary representing a row of data.

    Returns:
        dict: The updated dataset with 'XX' values in 'LIC_PLATE_STATE' replaced by 'UNKNOWN'.
    """
    print("Map license plate state to UNKNOWN when missing")
    for row in dataset.values():
        try:
            if LICENCE_PLATE in row and row[LICENCE_PLATE] == 'XX':
                row[LICENCE_PLATE] = "UNKNOWN"
        except Exception as e:
            print(f"Error processing {LICENCE_PLATE} | Error: {e}")
    return dataset

def typos_fixing(dataset, typos, attribute):
    """
    Fixes typos in the specified attribute of the dataset using a provided mapping.

    Args:
        dataset (dict): A dictionary where each key is a unique identifier and each value is a dictionary representing a row of data.
        typos (dict): A dictionary mapping incorrect values to their correct counterparts.
        attribute (str): The attribute/column name in which to fix typos.

    Returns:
        dict: The updated dataset with typos corrected in the specified attribute.
    """
    print("Fixing typos in UNKNOWN values")
    for row in dataset.values():
        try:
            for true_val, typo_val in typos.items():
                if row[attribute] == typo_val:
                    row[attribute] = true_val
        except Exception as e:
            print(f"No typos values in {attribute} | Error: {e}")
    return dataset

def set_vehicle_year(dataset):
    """
    Sets 'VEHICLE_YEAR' to NaN for years greater than 2024 and corrects the year 9999 to 1999.

    Args:
        dataset (dict): A dictionary where each key is a unique identifier and each value is a dictionary representing a row of data.

    Returns:
        dict: The updated dataset with 'VEHICLE_YEAR' corrected.
    """
    print("Fixing vehicle years where year is higher than 2024")
    for row in dataset.values():
        try:
            if row.get(VEHICLE_YEAR):
                if float(row[VEHICLE_YEAR]) == 9999:
                    row[VEHICLE_YEAR] = float(1999)
                elif float(row[VEHICLE_YEAR]) > 2024:
                    row[VEHICLE_YEAR] = float('nan')
        except Exception as e:
            print(f"Error processing {VEHICLE_YEAR} | Error: {e}")
    return dataset


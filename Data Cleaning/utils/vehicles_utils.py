LICENCE_PLATE = "LIC_PLATE_STATE"
MAKE = "MAKE"
VEHICLE_YEAR = "VEHICLE_YEAR"

# Make following mapping for 'LIC_PLATE_STATE' values: XX values -> UNKNOWN
def license_xx_to_u(dataset):
    for row in dataset.values():
        if LICENCE_PLATE in row and row[LICENCE_PLATE] == 'XX':
            row[LICENCE_PLATE] = "UNKNOWN"
    return dataset

#Typo fixing for the MAKE of cars:
    #('NEW HOLLAND, DIV. OF SPERRY NEW HOLLAND', 'NEW HOLLAND, (DIV. OF SPERRY NEW HOLLAND)')
    #('AMC (LAWN & GARDEN TRACTORS BY AMERICAN MOTORS)', 'AMC (LAWN & GARDEN TRACTORS BY AMMERICAN MOTORS)')
    #('ROLLS ROYCE', 'ROLLS-ROYCE')

#Typo fixing for the MODEL of cars:
#('UNKNOWN', 'UNKOWN')
def typos_fixing(dataset,typos,attribute):
    for row in dataset.values():
        for true_val, typo_val in typos.items():
                if row[attribute] == typo_val:
                    row[attribute] = true_val       
    return dataset

# Set a nan value for 'VEHICLE_YEAR' for observations when "VEHICLE_YEAR" > 2024
def set_vehicle_year(dataset):
    for row in dataset.values():
                if  row.get(VEHICLE_YEAR):
                    if float(row[VEHICLE_YEAR]) == 9999:
                         row[VEHICLE_YEAR] = float(1999)
                    elif float(row[VEHICLE_YEAR]) > 2024:
                        row[VEHICLE_YEAR] = float('nan')
    return dataset


from utils.read_write import to_csv
from utils.utils import concatenate_values

def createDateTimeTable (allDates, path):
    print ("Creating date time table...")
    dateTimeTable = {}

    dateTimeID = 1
    for date in allDates:
        key = concatenate_values (date)
        if key not in dateTimeTable:
            dateTimeTable[key] = {"DateTime_ID": dateTimeID, "Day":date['DAY'], "Month":date["MONTH"], "Year":date["YEAR"], "Time":date["TIME"]}
            dateTimeID += 1

    to_csv(dateTimeTable, path)

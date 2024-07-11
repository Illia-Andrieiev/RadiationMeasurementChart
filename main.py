import pandas as pd
from datetime import datetime

# Replace 'your_file.csv' with your actual file path
infile = 'data.csv'

# Define a date parser function
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

# Read the CSV file and parse the 'DateTime' column
df = pd.read_csv(infile, parse_dates=['DateTime'], date_parser=dateparse)

# Now you can work with the parsed datetime values in the DataFrame 'df'
print(df.head(2))
time_measure_file = 'timeMeasurements.csv'

# Define a date parser function
timeparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

# Read the CSV file and parse the 'DateTime' column
time_measurements = pd.read_csv(time_measure_file, parse_dates=['Time'], date_parser=timeparse)
print(time_measurements.head(2))

point = 1
height = 0
while True:
    if(height == 5):
        height = 0
        point += 1



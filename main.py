import point
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
point_nomer = 1
height = 0
current_index = 0
points = []
cur_point = point.Point(point_nomer)
for index, row in time_measurements.iterrows():
    cur_level_cps = point.LevelData()
    cur_level_Sv = point.LevelData()
    if height == 5:
        height = 0
        point_nomer += 1
        points.append(cur_point)
        cur_point = point.Point(point_nomer)
    start_time = row['Time']
    end_time = start_time + pd.Timedelta(seconds=30)
    # Find the relevant rows in 'df' based on time intervals
    relevant_rows = df[(df['DateTime'] >= start_time) & (df['DateTime'] < end_time)]

    for index, row in relevant_rows.iterrows():
        cur_level_cps.data.append(row['CPS'])
        cur_level_Sv.data.append(row['DoseRate'])
        cur_level_Sv.height = height * 0.5
        cur_level_cps.height = height * 0.5
        current_index += 1
    cur_point.Svdata.append(cur_level_Sv)
    cur_point.cpsdata.append(cur_level_cps)
    height += 1

for p in points:
    p.print()
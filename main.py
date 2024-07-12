import point
import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Parse points from data and measurements files
def parse_points():
    # Replace 'your_file.csv' with your actual file path
    infile = 'data.csv'

    # Define a date parser function
    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    # Read the CSV file and parse the 'DateTime' column
    df = pd.read_csv(infile, parse_dates=['DateTime'], date_parser=dateparse)

    # Now you can work with the parsed datetime values in the DataFrame 'df'
    time_measure_file = 'timeMeasurements.csv'

    # Define a date parser function
    timeparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    # Read the CSV file and parse the 'DateTime' column
    time_measurements = pd.read_csv(time_measure_file, parse_dates=['Time'], date_parser=timeparse)
    point_nomer = 1  # start count points from 1
    level = 0  # start height
    points = []  # result points
    cur_point = point.Point(point_nomer)  # current point
    for index, row in time_measurements.iterrows():  # for each time measurement write level date into one point
        cur_level_cps = point.LevelData()  # current level radiation in cps
        cur_level_Sv = point.LevelData()  # current level radiation in Sievert
        if level == 5:  # each point have 5 measurement levels (starts with 0). Add point and set default value
            level = 0
            point_nomer += 1
            points.append(cur_point)
            cur_point = point.Point(point_nomer)

        start_time = row['Time']  # start time for level measurement
        end_time = start_time + pd.Timedelta(seconds=30)
        # Find the relevant rows in 'df' based on time intervals
        relevant_rows = df[(df['DateTime'] >= start_time) & (df['DateTime'] < end_time)]

        for i, relevant_row in relevant_rows.iterrows():  # fill point level data
            cur_level_cps.data.append(relevant_row['CPS'])
            cur_level_Sv.data.append(relevant_row['DoseRate'])
            cur_level_Sv.height = level * 0.5
            cur_level_cps.height = level * 0.5
        cur_point.Svdata.append(cur_level_Sv)
        cur_point.cpsdata.append(cur_level_cps)
        level += 1  # increase level

    points.append(cur_point)  # add last point
    return points


# fill two_dimensional_array using simple array in decline columns order
def fill_two_dimensional_array(simple_array, rows, columns):
    res = [[None] * columns for _ in range(rows)]
    for index, elem in enumerate(simple_array):
        row_index = int(index / columns)
        column_index = columns - 1 - index % columns
        res[row_index][column_index] = simple_array[index]
    return res


# return matrix with each point`s concrete attribute
def get_parameter_data_matrix(pointed_area, level, radiation_data_type, attribute_name):
    res = [[0]*len(pointed_area) for _ in range(len(pointed_area[0]))]
    for i, row in enumerate(pointed_area):
        for j, point in enumerate(row):
            res[i][j] = getattr(getattr(point, radiation_data_type)[level], attribute_name)
    return res


# calculate statistic for each point in area
def calculate_pointed_area_statistic(pointed_area):
    for row in pointed_area:
        for p in row:
            p.calculate_statistics()


# create interpolated and non-interpolated heat maps
def create_heat_map(data_matrix, is_show, title=""):
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # 1 row, 2 columns, area 18x6 inches

    # create interpolated heat map
    axes[0].imshow(data_matrix, cmap='plasma', interpolation='bicubic')
    axes[0].set_title(title)
    fig.colorbar(axes[0].images[0], ax=axes[0])

    # create non-interpolated heat map
    im = axes[1].imshow(data_matrix, cmap='plasma')
    # write values on heat map
    for i in range(data_matrix.shape[0]):
        for j in range(data_matrix.shape[1]):
            axes[1].annotate(f"{data_matrix[i, j]:.2f}", (j, i), color='black', ha='center', va='center')
    axes[1].set_title(title)  # set title
    fig.colorbar(im, ax=axes[1])
    if is_show:
        plt.show()
    return plt


# save plot as image in path. Path should have file name
def save_plot(plot, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plot.savefig(path, dpi=300, bbox_inches='tight')


def main():
    pointed_area = fill_two_dimensional_array(parse_points(), 5, 5)  # define data for pointed area
    calculate_pointed_area_statistic(pointed_area)  # calculate statistic
    for row in pointed_area:
        for p in row:
            p.print()
    average_matrix = get_parameter_data_matrix(pointed_area, 4, "Svdata", "max")
    for row in average_matrix:
        for p in row:
            print(p)
    map = create_heat_map(np.array(average_matrix),False, "Average CPS")
    save_plot(map, 'plots/heatmap.png')
    # res = [[None] * 5 for _ in range(5)]
    # for i, row in enumerate(pointed_area):
    #     for j, p in enumerate(row):
    #         res[i][j] = p.nomer
    # create_heat_map(np.array(res), "nomers")


main()

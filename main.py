import point
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


# Parse points from data and measurements files
def parse_points():
    # Replace 'your_file.csv' with your actual file path
    infile = 'data.csv'

    # Define the date format
    date_format = '%Y-%m-%d %H:%M:%S'

    # Read the CSV file and parse the 'DateTime' column
    df = pd.read_csv(infile, parse_dates=['DateTime'], date_format=date_format)

    # Now you can work with the parsed datetime values in the DataFrame 'df'
    time_measure_file = 'timeMeasurements.csv'

    # Read the time measurements file and parse the 'Time' column
    time_measurements = pd.read_csv(time_measure_file, parse_dates=['Time'], date_format=date_format)

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
        cur_point.CPSdata.append(cur_level_cps)
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


def save_param(pointed_area, radiation_data_type, attribute_name):
    """
    Saves heat maps for a given parameter.

    Parameters:
    pointed_area (str): The specified area for analysis.
    radiation_data_type (str): The type of radiation data.
    attribute_name (str): The name of the attribute for analysis.

    """
    for i in range(5):
        # Get the data matrix for the current level
        data_matrix = get_parameter_data_matrix(pointed_area, i, radiation_data_type, attribute_name)
        # Create the heat map
        plot = create_heat_map(np.array(data_matrix), False, attribute_name + " " + radiation_data_type +
                               " " + str(i * 0.5) + " M")
        # Save the heat map to a file
        save_plot(plot, "plots/" + radiation_data_type + "/" + attribute_name + "/" + "level" + str(i) + ".png")
        # Close the current plot to free up memory
        plt.close()


def save_radiation_datatype(pointed_area, radiation_data_type, attribute_names):
    """
    Saves heat maps for all attributes of a given radiation data type.

    Parameters:
    pointed_area (str): The specified area for analysis.
    radiation_data_type (str): The type of radiation data.
    attribute_names (list): A list of attribute names for analysis.

    """
    for attribute in attribute_names:
        # Save heat maps for each attribute
        save_param(pointed_area, radiation_data_type, attribute)


def main():
    pointed_area = fill_two_dimensional_array(parse_points(), 5, 5)  # define data for pointed area
    calculate_pointed_area_statistic(pointed_area)  # calculate statistic
    statistics_names = ["moda", "min", "max", "average", "dispersion"]  # names of statistic parameters
    save_radiation_datatype(pointed_area, "Svdata", statistics_names)  # save Sievert data heatmaps
    save_radiation_datatype(pointed_area, "CPSdata", statistics_names)  # save CPS data heatmaps


main()

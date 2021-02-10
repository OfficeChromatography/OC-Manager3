import math
import json
import numpy as np
from scipy.optimize import minimize
from finecontrol.calculations.flowCalc import FlowCalc
from types import SimpleNamespace
from finecontrol.gcode.GcodeGenerator import GcodeGenerator


def calculate_drop_estimated_volume(data):
    working_area = calculate_working_area(data)

    if int(data.main_property) == 1:
        nbands, length = precalculations_when_nbands_option_selected(data, working_area[0])
    else:
        nbands, length = precalculations_when_length_option_selected(data, working_area[0])

    results = []
    for table in data.table:

        drop_volume = FlowCalc(pressure=float(data.pressure), nozzleDiameter=data.nozzlediameter,
                              timeOrFrequency=float(data.frequency), fluid=table['type'], density=table['density'],
                              viscosity=table['viscosity']).calcVolumeFrequency()

        x_number_of_points = calculate_number_of_points(length, data.delta_x)
        y_number_of_points = calculate_number_of_points(data.height, data.delta_y)

        vol2 = (x_number_of_points - 1) * (y_number_of_points - 1) * drop_volume
        vol = y_number_of_points * y_number_of_points * drop_volume
        # print(vol,vol2)

        # THIS GOES IN THE CLEAN FORM NOT HERE
        volume_per_band = (table['volume'])
        if volume_per_band == "" or volume_per_band == "null":
            volume_per_band = 0
        volume_per_band = float(volume_per_band)

        times_to_apply, real_volume = calculate_number_of_times_to_apply(volume_per_band, vol, vol2)

        values = {"estimated_volume": real_volume,
                  "estimated_drop_volume": drop_volume,
                  "times": times_to_apply,
                  "minimum_volume": vol}
        results.append(values)
    return results


def minusOneUntilZero(number):
    number = number - 1
    if number < 0: number = 0
    return number


def calculate_number_of_times_to_apply(volume_per_band, vol, vol2):
    times_to_apply = 0
    real_volume = 0
    dif = volume_per_band - real_volume
    while dif >= 0:
        if times_to_apply % 2:
            real_volume += vol2
        else:
            real_volume += vol
        dif = volume_per_band - real_volume
        times_to_apply += 1

    if times_to_apply % 2:
        if abs(dif) > vol / 2:
            times_to_apply -= 1
            real_volume -= vol
    else:
        if abs(dif) > vol2 / 2:
            times_to_apply -= 1
            real_volume -= vol2
    return times_to_apply, real_volume


def calculate_number_of_points(length, distance_between_points):
    number_of_points = int(length/distance_between_points) + 1
    return number_of_points


def calculate_working_area(data):
    x_working_area = data.size_x - data.offset_left - data.offset_right
    y_working_area = data.size_y - data.offset_top - data.offset_bottom
    return [x_working_area, y_working_area]


def precalculations_when_nbands_option_selected(data, x_working_area):
    n_bands = int(data.value)
    number_of_gaps = n_bands - 1
    sum_gaps_size = data.gap * number_of_gaps
    length = (x_working_area - sum_gaps_size) / n_bands
    return n_bands, length


def precalculations_when_length_option_selected(data, x_working_area):
    length = data.value
    n_bands = int(math.trunc(x_working_area / (length + data.gap)))
    return n_bands, length


def calculate(data):
    data = SimpleNamespace(**data)

    working_area = calculate_working_area(data)

    if int(data.main_property) == 1:
        n_bands, length = precalculations_when_nbands_option_selected(data, working_area[0])
    else:
        n_bands, length = precalculations_when_length_option_selected(data, working_area[0])

    volume_estimated = calculate_drop_estimated_volume(data)

    sampleTimes = [data_band['times'] for data_band in volume_estimated]

    list_of_bands = []

    deltaX = float(data.delta_x)
    deltaY = float(data.delta_y)
    j = 0
    while sum(sampleTimes) != 0:
        for i in range(0, n_bands):
            if sampleTimes[i] == 0: continue
            bandlist = []
            zeros = (i * (length + data.gap)) + data.offset_left
            if j % 2:
                current_height = deltaY / 2
                while current_height <= data.height:
                    applicationline = []
                    current_length = deltaX / 2
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += deltaX
                    bandlist.append(applicationline)
                    current_height += deltaY
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline = []
                    current_length = 0.
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += deltaX
                    bandlist.append(applicationline)
                    current_height += deltaY
            list_of_bands.append(bandlist)
        j += 1
        sampleTimes = list(map(minusOneUntilZero, sampleTimes))
        # print(sampleTimes)

    # Creates the Gcode for the application and return it
    return gcode_generation(list_of_bands, data.motor_speed, data.frequency, data.temperature, data.pressure,
                            [data.zero_x, data.zero_y])


def gcode_generation(list_of_bands, speed, frequency, temperature, pressure, zeroPosition):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)
        generate.hold_bed_temperature(temperature)
        generate.report_bed_temperature(4)

    # Move to the home
    # generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)

    # Application
    # generate.pressurize(pressure)

    generate.rinsing()
    generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
    jj = 0
    for band in list_of_bands:
        for index, list_of_points in enumerate(band):
            if jj > 50:
                generate.rinsing()
                generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
                jj = 0
            for point in list_of_points:
                generate.linear_move_xy(point[0], point[1], speed)
                generate.finish_moves()
                generate.pressurize(pressure)
                generate.open_valve(frequency)
                generate.finish_moves()
                jj += 1
    # Stop heating
    if (temperature != 0):
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    # Homming
    generate.homming("XY")
    # print(generate.list_of_gcodes)
    return generate.list_of_gcodes

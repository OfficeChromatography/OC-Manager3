import math
import json
import numpy as np
from scipy.optimize import minimize
from finecontrol.calculations.flowCalc import FlowCalc
from types import SimpleNamespace
from finecontrol.gcode.GcodeGenerator import GcodeGenerator


def calculate_volume_application_info(data):
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
        vol = x_number_of_points * y_number_of_points * drop_volume


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
        #print(values)
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
    #print(f"DISTANCE: {distance_between_points}")
    #print(f"LENGTH: {length}")
    number_of_points = int(length / distance_between_points) + 1
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

    application_volume_info = calculate_volume_application_info(data)

    band_application_times = [info_band['times'] for info_band in application_volume_info]

    list_of_bands = []

    delta_x = float(data.delta_x)
    delta_y = float(data.delta_y)

    j = 0
    while sum(band_application_times) != 0:
        for i in range(0, n_bands):
            if band_application_times[i] == 0: continue
            bandlist = []
            zeros = (i * (length + data.gap)) + data.offset_left
            if j % 2:
                current_height = delta_y / 2
                while current_height <= data.height:
                    applicationline = []
                    current_length = delta_x / 2
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += delta_x
                    bandlist.append(applicationline)
                    current_height += delta_y
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline = []
                    current_length = 0.
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += delta_x
                    bandlist.append(applicationline)
                    current_height += delta_y
            list_of_bands.append(bandlist)
        j += 1
        band_application_times = list(map(minusOneUntilZero, band_application_times))

    print_process = PrintingProcess(list_of_bands,
                                    data.motor_speed,
                                    data.frequency,
                                    data.temperature,
                                    data.pressure,
                                    [data.zero_x, data.zero_y],
                                    data.wait)

    # Creates the Gcode for the application and return it
    return print_process.printing_process()


class PrintingProcess:
    def __init__(self, list_of_bands, speed, frequency, temperature, pressure, zeroPosition, waitTime) -> object:
        self.list_of_bands = list_of_bands
        self.speed = speed
        self.frequency = frequency
        self.temperature = temperature
        self.pressure = pressure
        self.zeroPosition = zeroPosition
        self._gcode_generator = GcodeGenerator(save_in_list=True)
        self.waitTime = waitTime

    def printing_process(self):
        self._set_temperature()
        self._rinse()
        self._set_yhome()
        self._bands_printing()
        self._final_steps_after_print()
        return self._gcode_generator.list_of_gcodes

    def _set_temperature(self):
        if self.temperature != 0:
            self._gcode_generator.wait_bed_temperature(self.temperature)
            self._gcode_generator.hold_bed_temperature(self.temperature)
            self._gcode_generator.report_bed_temperature(4)

    def _set_yhome(self):
        self._gcode_generator.set_new_zero_position_y(self.zeroPosition[1], self.speed)

    def _rinse(self):
        self._gcode_generator.rinsing()
        self._gcode_generator.set_new_zero_position_x(self.zeroPosition[0], self.speed)

    def _bands_printing(self):
        '''
        will rinse after 50 drops applied
        will wait for waitTime before going in -y direction
        '''
        number_of_drops_applied = 0
        directionY = 0
        for band in self.list_of_bands:
            for index, list_of_points in enumerate(band):
                if number_of_drops_applied > 50:
                    self._rinse()
                    number_of_drops_applied = 0
                for point in list_of_points:
                    if (directionY-point[0])>0:
                        self._gcode_generator.wait(self.waitTime)
                    self._gcode_generator.linear_move_xy(point[0], point[1], self.speed)
                    self._gcode_generator.finish_moves()
                    self._gcode_generator.pressurize(self.pressure)
                    self._gcode_generator.open_valve(self.frequency)
                    self._gcode_generator.finish_moves()
                    number_of_drops_applied += 1
                    directionY = point[0]


    def _final_steps_after_print(self):
        self._gcode_generator.hold_bed_temperature(0)
        self._gcode_generator.report_bed_temperature(0)
        self._gcode_generator.homming("XY")

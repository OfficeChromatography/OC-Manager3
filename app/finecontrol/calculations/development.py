import numpy as np
from scipy.interpolate import CubicSpline

from types import SimpleNamespace

from finecontrol.gcode.GcodeGenerator import GcodeGenerator
from finecontrol.calculations.volumeToZMovement import volumeToZMovement


def cubicSpline(data):
    step = 100 / (len(data) - 1)
    x = np.arange(0, 100 + step, step)
    y = np.array([float(i['value']) for i in data])
    cs = CubicSpline(x, y)
    t = np.linspace(0, 100, len(data))
    coordinates = list(map(cs, t))

    return coordinates


def speedWeighting(speeds: list):
    """weights the speed so that the volume of one band (the overall speed) stays constant, even if the speed is
    changing. """
    integral = 0
    for entry in speeds:
        integral += entry / len(speeds)

    vol_coefficient = 1 / integral

    weighted_speeds = [vol_coefficient * x for x in speeds]

    return weighted_speeds


def calculateDevelopment(data):
    data = SimpleNamespace(**data)
    length = float(data.size_x) - float(data.offset_left) - float(data.offset_right)
    start_point = [round(float(data.offset_left) + float(data.zero_x), 3),
                   round(float(data.offset_bottom) + float(data.zero_y), 3)]

    z_movement = volumeToZMovement(data.volume, True)

    speed_spline_list = cubicSpline(data.flowrate)
    speed_factors = speedWeighting(speed_spline_list)

    return GcodeGenDevelopment(start_point, length, z_movement, data.applications, data.printBothways,
                               float(data.motor_speed) * 60, data.temperature, data.pressure, data.waiting_times,
                               speed_factors)


def GcodeGenDevelopment(start_point, length, z_movement, applications, print_both_ways, speed, temperature, pressure,
                        waiting_times, speed_factors):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)
        generate.hold_bed_temperature(temperature)
        generate.report_bed_temperature(4)

    # Move to the home
    generate.homming("XY")
    generate.linear_move_y(start_point[1], speed)
    generate.linear_move_x(start_point[0], speed)
    generate.finish_moves()
    # Set relative coordinates
    generate.set_relative()
    jj = 0
    for x in range(int(applications) * 2):
        # moving to the end of the line
        if (x % 2) == 0:
            generate.pressurize(pressure)
            generate.open_valve()
            for speed_factor in speed_factors:
                generate.linear_move_xz(round(length / len(speed_factors), 3),
                                        round(z_movement * speed_factor / float(applications) / len(speed_factors), 3),
                                        speed)
            generate.close_valve()
            generate.check_pressure()
            generate.wait(waiting_times[x].get("waitTime"))
            jj += 1
        # moving back to the start of the line
        else:
            if print_both_ways == 'True':
                generate.pressurize(pressure)
                generate.open_valve()
                for speed_factor in speed_factors:
                    generate.linear_move_xz(-1 * round(length / len(speed_factors), 3),
                                            round(z_movement * speed_factor / float(applications) / len(speed_factors),
                                                  3), speed)
                generate.close_valve()
                generate.check_pressure()
                generate.wait(waiting_times[x].get("waitTime"))
                jj += 1
            else:
                generate.linear_move_x(-1 * length, speed)
        if jj >= int(applications):
            break
    # Stop heating
    if temperature != 0:
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    # set to absolute again
    generate.set_absolute()
    # Homing
    generate.homming("XY")
    return generate.list_of_gcodes

from types import SimpleNamespace

from finecontrol.gcode.GcodeGenerator import GcodeGenerator
from finecontrol.calculations.volumeToZMovement import volumeToZMovement


def calculateDerivatization(data):
    data = SimpleNamespace(**data)
    length = float(data.size_x) - float(data.offset_left) - float(data.offset_right)
    width = float(data.size_y) - float(data.offset_top) - float(data.offset_bottom)
    start_point = [round(float(data.offset_left) + float(data.zero_x), 3),
                   round(float(data.offset_bottom) + float(data.zero_y), 3)]

    z_movement = volumeToZMovement(data.volume, True)

    return gcode_generator(start_point, length, z_movement, data.applications, width, float(data.motor_speed) * 60,
                           data.temperature, data.pressure, data.waitTime, data.printBothways)


def gcode_generator(start_point, length, z_movement, applications, width, speed, temperature, pressure, wait_time,
                    print_both_ways):
    width = float(width) / (int(applications) - 1)

    generate = GcodeGenerator(True)

    # No HEAT BED CASE
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

            generate.linear_move_xz(round(length, 3), round(z_movement / float(applications), 3), speed)
            if jj >= int(applications):
                break
            generate.linear_move_y(round(width, 3), speed)
            generate.wait(wait_time)
            jj += 1
        # moving back to the start of the line
        else:

            if print_both_ways == 'True':
                generate.linear_move_xz(-1 * round(length, 3), round(z_movement / float(applications), 3), speed)
                if jj >= int(applications):
                    break
                generate.linear_move_y(round(width, 3), speed)
                generate.wait(wait_time)
                jj += 1
            else:
                generate.linear_move_x(-1 * length, speed)

    # Stop heating
    if temperature != 0:
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    # set to absolute again
    generate.set_absolute()
    # homing
    generate.homming("XY")
    return generate.list_of_gcodes

class GcodeGenerator:

    def __init__(self, save_in_list):
        self.list_of_gcodes = []
        self.save_in_list = save_in_list

    def check_return(self, gcode):
        if self.list_of_gcodes:
            self.list_of_gcodes.append(gcode)
            return
        else:
            return gcode

    def linear_move_xyz(self, pos_x, pos_y, pos_z, speed):
        """"A linear move traces a straight line from one point to another, ensuring that the specified axes will arrive
        simultaneously at the given coordinates (by linear interpolation). The speed may change over time following an
        acceleration curve, according to the acceleration and jerk settings of the given axes."""
        pos_x = str(round(pos_x, 3))
        pos_y = str(round(pos_y, 3))
        pos_z = str(round(pos_z, 3))
        return self.check_return(f"G1X{pos_x}Y{pos_y}Z{pos_z}F{speed}")

    def linear_move_x(self, pos_x, speed):
        return self.linear_move_xyz(pos_x, 0, 0, speed)

    def linear_move_y(self, pos_y, speed):
        return self.linear_move_xyz(0, pos_y, 0, speed)

    def linear_move_z(self, pos_z, speed):
        return self.linear_move_xyz(0, 0, pos_z, speed)

    def linear_move_xy(self, pos_x, pos_y, speed):
        return self.linear_move_xyz(pos_x, pos_y, 0, speed)

    def linear_move_xz(self, pos_x, pos_z, speed):
        return self.linear_move_xyz(pos_x, 0, pos_z, speed)

    def linear_move_yz(self, pos_y, pos_z, speed):
        return self.linear_move_xyz(0, pos_y, pos_z, speed)

    def wait_bed_temperature(self, temperature):
        """This command optionally sets a new target bed temperature and waits for the target temperature
        to be reached before proceeding. """
        return self.check_return(f"M190R{temperature}")

    def homming(self, axis):
        """Auto-home one or more axes, moving them towards their endstops until triggered."""
        return self.check_return(f"G28{axis.upper()}")

    def set_position_xyz(self, pos_x, pos_y, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Y{pos_y}Z{pos_z}")

    def set_position_x(self, pos_x):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}")

    def set_position_y(self, pos_y):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Y{pos_y}")

    def set_position_z(self, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Z{pos_z}")

    def set_position_xy(self, pos_x, pos_y):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Y{pos_y}")

    def set_position_xz(self, pos_x, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Z{pos_z}")

    def set_position_yz(self, pos_y, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Y{pos_y}Z{pos_z}")

    def finish_moves(self):
        """This command causes G-code processing to pause and wait in a loop until all
        moves in the planner are completed."""
        return self.check_return(f"M400")

    def pressurize(self, pressure):
        """This command increase the pressure in the system"""
        return self.check_return(f"G97P{pressure}")

    def toggle_valve(self, frequency):
        """This command open and close the valve at a certain frequency"""
        return self.check_return(f"G98F{frequency}")

    def set_pin_state(self, pin, state):
        """For custom hardware not officially supported in Marlin, you can often just connect
        up an unused pin and use M42 to control it."""
        return self.check_return(f"M42P{pin}S{state}")

def gcode_generation(list_of_lines, speed, frequency, temperature, pressure, zeroPosition):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)

    # Move to the home
    generate.homming("XY")
    generate.linear_move_xy(zeroPosition[0], zeroPosition[1], speed)
    generate.set_position_xy(0, 0)
    generate.finish_moves()

    # Application
    generate.pressurize(pressure)
    for list_of_points in list_of_lines:
        for point in list_of_points:
            generate.linear_move_xy(point[1], point[0], speed)
            generate.finish_moves()
            generate.pressurize(pressure)
            generate.toggle_valve(frequency)
            generate.finish_moves()
    generate.homming("XY")
    return generate.list_of_gcodes



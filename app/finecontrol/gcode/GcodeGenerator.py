class GcodeGenerator:

    def __init__(self, save_in_list):
        self.list_of_gcodes = []
        self.save_in_list = save_in_list

    def check_return(self, gcode):
        if self.save_in_list:
            self.list_of_gcodes.append(gcode)
            return
        else:
            return gcode

    def linear_move_xyz(self, pos_x, pos_y, pos_z, speed):
        """"A linear move traces a straight line from one point to another, ensuring that the specified axes will arrive
        simultaneously at the given coordinates (by linear interpolation). The speed may change over time following an
        acceleration curve, according to the acceleration and jerk settings of the given axes."""
        if pos_x != "":
            pos_x = str(round(float(pos_x), 3))
        if pos_y != "":
            pos_y = str(round(float(pos_y), 3))
        if pos_z != "":
            pos_z = str(round(float(pos_z), 3))
        return self.check_return(f"G1X{pos_x}Y{pos_y}Z{pos_z}F{speed}")

    def linear_move_x(self, pos_x, speed):
        return self.linear_move_xyz(pos_x, "", "", speed)

    def linear_move_y(self, pos_y, speed):
        return self.linear_move_xyz("", pos_y, "", speed)

    def linear_move_z(self, pos_z, speed):
        return self.linear_move_xyz("", "", pos_z, speed)

    def linear_move_xy(self, pos_x, pos_y, speed):
        return self.linear_move_xyz(pos_x, pos_y, "", speed)

    def linear_move_xz(self, pos_x, pos_z, speed):
        return self.linear_move_xyz(pos_x, "", pos_z, speed)

    def linear_move_yz(self, pos_y, pos_z, speed):
        return self.linear_move_xyz("", pos_y, pos_z, speed)

    def wait_bed_temperature(self, temperature):
        """This command optionally sets a new target bed temperature and waits for the target temperature
        to be reached before proceeding. """
        return self.check_return(f"M190R{temperature}")

    def hold_bed_temperature(self, temperature):
        '''This command sets a new bed temperature and proceeds without waiting. The temperature will be held in the background'''
        return self.check_return(f"M140S{temperature}")

    def report_bed_temperature(self, timeIntervall):
        '''
        It can be useful for host software to track temperatures, display and graph them over time, but polling with M105 is less than optimal. 
        With M155 hosts simply set an interval and Marlin will keep sending data automatically. This method is preferred over polling with M105.
        timeIntervall in seconds
        '''
        return self.check_return(f"M155S{timeIntervall}")


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

    def open_valve(self, frequency):
        """This command open and close the valve at a certain frequency"""
        return self.check_return(f"G98F{frequency}")

    def toggle_valve(self):
        """This command toggles the valve. 
        open -> close, close -> open"""
        return self.check_return(f"G40")

    def set_pin_state(self, pin, state):
        """For custom hardware not officially supported in Marlin, you can often just connect
        up an unused pin and use M42 to control it."""
        return self.check_return(f"M42P{pin}S{state}")
    
    def wait(self, time):
        """pauses the command queue and waits for a period of time in seconds"""
        return self.check_return(f"G4S{time}")
    
    def set_relative(self):
        """In this mode all coordinates are interpreted as relative to the last position."""
        return self.check_return(f"G91")

    def set_absolute(self):
        """In absolute mode all coordinates given in G-code are interpreted as positions in the logical coordinate space."""
        return self.check_return(f"G90")

    def check_pressure(self):
        return self.check_return(f"G95P")

    def rinsing(self):
        self.homming("XY")
        self.pressurize("60")
        self.open_valve("1")

    def set_new_zero_position(self, x, y,speed):
        self.homming("XY")
        self.linear_move_xy(x, y, speed)
        self.set_position_xy(0, 0)
        self.finish_moves()



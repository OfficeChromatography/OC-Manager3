from serial import Serial
import serial.tools.list_ports
import time
import sys


class ArdComm(Serial):

    @staticmethod
    def ArduinosConnected():
        list=[]
        a=serial.tools.list_ports.comports()
        for devices in a:
            if str(devices.description) != 'n/a':
                list.append(devices)
        return list

    def connectArduino(self, port):
        # returns TRUE if connected if not, FALSE
        self.closeArduino()
        # Connect to selected port
        self.port = port
        self.queue = 0
        error=0
        while error<10:
            try:
                self.open()
                success = True
                break
            except:
                success = False
                error+=1
        if success:
            time.sleep(3)
        return success

    def closeArduino(self):
        # Close any posible connection and clean the monitor
        self.__del__()
        return

    def readArduino(self):
        formated = ""
        while True:
            try:
                ser_bytes = self.read_until()  # (‘\n’ by default)
                decoded_bytes = ser_bytes[:-1].decode("utf-8")
                formated += str(decoded_bytes)+str('\n')
                if (formated[-1] == '\n' and formated[-2] == '\n'):
                    break
            except:
                formated="Error reading, command might be or not apply\n"
                ser_bytes=""
                break
        return formated

    def writeArduino(self, menssage):
        self.queue+=1
        # sys.stdout.flush()

        print(self.queue)
        if self.queue==1:
            menssage += 2*'\n'
            self.write(menssage.encode('utf-8'))
            menssage = menssage[0:-1]
            menssage += self.readArduino()
            self.queue-=1
        else:
            menssage = "Error "+self.name+" busy, try "+ menssage +" later\n"
            print("ERROR")
            self.queue-=1
        return menssage

    def isrunning(self):
        try:
            self.write("G0".encode('utf-8'))
            self.readArduino()
            return True
        except:
            print("error")
            return False

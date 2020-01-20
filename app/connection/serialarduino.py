from serial import Serial
import serial.tools.list_ports
import time


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
        self.closeArduino()
        # Connect to selected port
        self.queue_read=0
        self.queue_write=0
        self.port = port
        self.open()
        # self.readArduino()
        return

    def closeArduino(self):
        # Close any posible connection and clean the monitor
        self.close()
        return

    def readArduino(self):
        formated = ""
        self.queue_read+=1
        while True:
            try:
                ser_bytes = self.read_until()  # (‘\n’ by default)
                decoded_bytes = ser_bytes[:-1].decode("utf-8")
                formated += str(decoded_bytes)+str('\n')
                if (formated[-1] == '\n' and formated[-2] == '\n'):
                    self.queue_read-=1
                    break
            except:
                formated="Error reading, command might be or not apply\n"
                ser_bytes=""
        return formated

    def writeArduino(self, menssage):
        self.queue_write+=1
        print(self.queue_write)
        if self.queue_write==1:
            menssage += 2*'\n'
            self.write(menssage.encode('utf-8'))
            menssage = menssage[0:-1]
            self.queue_write-=1
        else:
            menssage = "Error "+self.name+" busy, try "+ menssage +" later\n"
            self.queue_write-=1
        return menssage

    def isrunning(self):
        try:
            self.write("G0".encode('utf-8'))
            self.readArduino()
            return True
        except:
            print("error")
            return False

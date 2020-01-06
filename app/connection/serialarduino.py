from serial import Serial


class ArdComm(Serial):

    def connectArduino(self, port):
        self.closeArduino()
        # Connect to selected port
        self.port = port
        self.open()
        # self.readArduino()
        return

    def closeArduino(self):
        # Close any posible connection and clean the monitor
        self.close()
        return

    def readArduino(self):  # Read 1 sec mssg
        formated = ""
        while True:
            ser_bytes = self.read_until()  # (‘\n’ by default)
            decoded_bytes = ser_bytes[:-1].decode("utf-8")
            formated += str(decoded_bytes)+str('\n')
            if formated[-1] == '\n' and formated[-2] == '\n':
                break
        return formated

    def writeArduino(self, menssage):
        menssage += 2*'\n'
        self.write(menssage.encode('utf-8'))
        return

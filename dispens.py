import serial
import time
from datetime import datetime

def command(ser, command):
  start_time = datetime.now()
  ser.write(str.encode(command)) 
  time.sleep(1)

  while True:
    line = ser.readline()
    print(line)

    if line == b'ok\n':
      break

ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)
command(ser, "G1Y101F2000\r\n")
input("Press Enter to continue...")
command(ser, "G0Y93F400\r\n") 
time.sleep(0.5)  # stop time at Y93 = lower edge of the plate
command(ser, "G1Y0F600\r\n")    #F value = speed for application (mm/min)
time.sleep(2)
ser.close()
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
command(ser, "G93 R0 B0 G0\r\n")
command(ser, "G28Y0\r\n")
time.sleep(2)
ser.close()
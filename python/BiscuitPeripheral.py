import serial
import os

TX = serial.Serial()

if os.name == 'posix':
  TX.port = '/dev/tty.usbmodem1431'
else:
  TX.port = 'COM5'
TX.baudrate = 115200
TX.open()

print 'Waiting for data from Biscuit central...'
while 1:
  print TX.readline()

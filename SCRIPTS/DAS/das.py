import serial.tools.list_ports
import struct
import time as t

portsList = []
com = []

while len(portsList) == 0:
    ports = serial.tools.list_ports.comports()

    for p in ports:
        portsList.append(str(p))
        print(str(p))

    if len(portsList) == 0:
        print("Connect Arduino to Computer")
        t.sleep(1)
    elif len(portsList) == 1:
        com = portsList[0]
        com = com[:4]
    else:
        com = input("Select Arduino port by #: ")
        for i in range(len(portsList)):
            if portsList[i].startswith("COM" + com):
                com = "COM" + str(com)
                print(com + " is selected")
            else:
                print("Select valid COM number")

serial = serial.Serial()
serial.baudrate = 115200
serial.port = com
t.sleep(1)
serial.close()
serial.open()
print(com + " is connected")

while True:
    if serial.read(1) == b'\xAA':
        data = serial.read(10)

        encoder, timestamp, pressure = struct.unpack('<lLH', data)

        print(encoder, timestamp, pressure)

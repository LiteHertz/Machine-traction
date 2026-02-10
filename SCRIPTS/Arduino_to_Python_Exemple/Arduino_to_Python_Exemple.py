import serial.tools.list_ports
import time as t

serialInst = serial.Serial()
serialInst.baudrate = 115200
portsList = []

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

serialInst.port = com
t.sleep(1)
serialInst.close()
serialInst.open()
print(com + " is connected")

while True:
    command = input("Arduino Command (ON, OFF, STATE, exit): ")
    if command == "ON" or command == "OFF":
        serialInst.write(command.encode("utf-8"))
    elif command == "STATE":
        for i in range(10):
            if serialInst.inWaiting() == 0:
                pass
            serialInst.reset_input_buffer()
            print(str(serialInst.readline().decode("utf-8").strip()))
            t.sleep(0.1)
    elif command == "exit":
        exit()

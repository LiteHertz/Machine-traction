import serial.tools.list_ports

serialInst = serial.Serial()
serialInst.baudrate = 9600
ports = serial.tools.list_ports.comports()
portsList = []

for p in ports:
    portsList.append(str(p))
    print(str(p))

if portsList:
    com = input("Select Arduino port by #: ")
else:
    com = ""
    print("Connect Arduino to Computer")


for i in range(len(portsList)):
    if portsList[i].startswith("COM" + com):
        com = "COM" + str(com)
        print(com + " is selected")
    else:
        print("Select valid COM number")

serialInst.port = com
serialInst.open()

while True:
    command = input("Arduino Command (ON, OFF, exit): ")
    serialInst.write(command.encode("utf-8"))

    if command == "exit":
        exit()

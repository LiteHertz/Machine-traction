import serial
import serial.tools.list_ports
import struct
import time

# ===== Detect COM Port =====
def select_port():
    while True:
        ports = list(serial.tools.list_ports.comports())

        if not ports:
            print("Connect Arduino to Computer...")
            time.sleep(1)
            continue

        print("\nAvailable ports:")
        for i, p in enumerate(ports):
            print(f"{i}: {p.device}")

        if len(ports) == 1:
            return ports[0].device

        selection = input("Select port number: ")

        try:
            return ports[int(selection)].device
        except:
            print("Invalid selection.\n")


com_port = select_port()

# ===== Open Serial =====
ser = serial.Serial(com_port, 115200)
time.sleep(2)  # allow Arduino reset

print(f"{com_port} connected.\n")

# ===== Read Data =====
PACKET_SIZE = 10  # after start byte

while True:
    if ser.read(1) == b'\xAA':
        data = ser.read(PACKET_SIZE)

        if len(data) == PACKET_SIZE:
            timestamp, rawPressure, encoderStep = struct.unpack('<LHl', data) # The < means little-endian, l is a 4-byte signed int, L is a 4-byte unsigned int, H is a 2-byte unsigned int. They have to be in the right order to match how the data is packed on the Arduino side.
            voltsPressure = rawPressure / 1023 * 5 # Bring to ratio over 1 and then multiply by 5V to get the actual voltage reading from the pressure sensor.
            MPaPressure = (voltsPressure - 0.5) * 3.75
            mmDisplacement = encoderStep * 0.05 / 2
            print(timestamp, rawPressure, encoderStep,  " // ",f"{voltsPressure:.5f}", "V, " f"{MPaPressure:.5f}", "MPa, ", f"{mmDisplacement:.5f}", "mm") #f"{}" is used to format the output, the .5f means to show 5 decimal places.
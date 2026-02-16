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
            pressure, encoder, timestamp = struct.unpack('<lLH', data)
            print(timestamp, pressure, encoder)
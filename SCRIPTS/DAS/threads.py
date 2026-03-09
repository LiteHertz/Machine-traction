import serial
import serial.tools.list_ports
import struct
import time
import threading
import queue

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

# ===== ===== ===== Externally defined functions ===== ===== =====
# ===== Math transformations =====
def transform_data(rawPressure, encoderStep):
    voltsPressure = rawPressure / 1023 * 5 # Bring to ratio over 1 and then multiply by 5V to get the actual voltage reading from the pressure sensor.
    MPaPressure = (voltsPressure - 0.5) * 3.75
    mmDisplacement = encoderStep * 0.05 / 2
    return MPaPressure, mmDisplacement

def set_default_csv_filename():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"data_{timestamp}.csv"

# ===== Queues and Event  Definition =====
data_queue = queue.Queue()
gui_queue = queue.Queue()
stop_event = threading.Event()


# ===== Read Data Loop =====
def data_read_loop():
    PACKET_SIZE = 10  # after start byte

    while True:
        if ser.read(1) == b'\xAA':
            data = ser.read(PACKET_SIZE)

            if len(data) == PACKET_SIZE:
                timestamp, rawPressure, encoderStep = struct.unpack('<LHl', data) # The < means little-endian, l is a 4-byte signed int, L is a 4-byte unsigned int, H is a 2-byte unsigned int. They have to be in the right order to match how the data is packed on the Arduino side.
                MPaPressure, mmDisplacement = transform_data(rawPressure, encoderStep)
                data_queue.put((timestamp, MPaPressure, mmDisplacement)) # Put the transformed data into the queue for the csv file writing thread to consume.
                #print(timestamp, f"{MPaPressure:.5f}", "MPa, ", f"{mmDisplacement:.5f}", "mm") #f"{}" is used to format the output, the .5f means to show 5 decimal places. | Was used before for testing purposes |

# ===== Ask for file name =====
file_name = input("Enter CSV file name (without extension, default is 'data_<timestamp>'): ")
if not file_name:
    file_name = set_default_csv_filename()

# ===== CSV Writing Loop =====
def csv_write_loop():
    with open(file_name, 'w') as csv_file: # Open the CSV file for writing.
        csv_file.write("Timestamp,MPa Pressure,mm Displacement\n") # Write the header of the CSV file.
        while not stop_event.is_set() or not data_queue.empty(): # Keep writing until the stop event is set and the data queue is empty.
            try:
                timestamp, MPaPressure, mmDisplacement = data_queue.get(timeout=0.1) # Wait for data to be available in the queue, with a timeout to allow checking for the stop event.
                csv_file.write(f"{timestamp},{MPaPressure},{mmDisplacement}\n") # Write the data to the CSV file
            except queue.Empty:
                pass

# ===== Start Threads =====
threading.Thread(target=data_read_loop, daemon=True).start() # Daemon thread will automatically close when the main program exits.
threading.Thread(target=csv_write_loop, daemon=True).start() # Daemon thread will automatically close when the main program exits.


stop = input("Press Enter to stop program...\n")
stop_event.set() # Signal the threads to stop

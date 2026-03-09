import serial
import serial.tools.list_ports
import struct
import time
import threading
import queue


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# CONFIGURATION
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

START_THRESHOLD = 1.0    # MPa — pressure to begin recording
STOP_THRESHOLD  = 1.0    # MPa — pressure to end recording (only after peak)
PEAK_THRESHOLD  = 15.0   # MPa — must be reached before stop is allowed
BAUD_RATE       = 115200
PACKET_SIZE     = 10     # bytes after start byte


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# SHARED STATE  (queue, event, flags)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

data_queue  = queue.Queue()
stop_event  = threading.Event()


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# HELPER FUNCTIONS  (pure, no side effects)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def transform_data(rawPressure, encoderStep):
    # Convert raw Arduino values to engineering units.
    voltsPressure  = rawPressure / 1023 * 5          # 0-1023 → 0-5 V
    MPaPressure    = (voltsPressure - 0.5) * 3.75     # 0.5-4.5 V → 0-15 MPa
    mmDisplacement = encoderStep * 0.05 / 2           # steps → mm
    return MPaPressure, mmDisplacement


def set_default_csv_filename():
    # Generate a timestamped default filename.
    return f"data_{time.strftime('%Y%m%d-%H%M%S')}.csv"


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# SETUP  (runs before threads start)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def select_port():
    # Prompt the user to select a COM port, retrying until one is available.
    while True:
        ports = list(serial.tools.list_ports.comports())

        if not ports:
            print("No ports found. Connect Arduino and waiting...")
            time.sleep(1)
            continue

        print("\nAvailable ports:")
        for i, p in enumerate(ports):
            print(f"  {i}: {p.device}")

        if len(ports) == 1:
            print(f"Auto-selected: {ports[0].device}")
            return ports[0].device

        selection = input("Select port number: ")
        try:
            return ports[int(selection)].device
        except (ValueError, IndexError):
            print("Invalid selection.\n")


def get_csv_filename():
    # Ask the user for a CSV filename, falling back to a timestamped default.
    name = input("Enter CSV file name (without extension, or press Enter for default [data_<timestamp>]: ").strip()
    return (name + ".csv") if name else set_default_csv_filename()


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# RECORDING STATE CONTROLLER
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def update_recording_state(MPaPressure):
    # Hysteresis state machine:
    #   IDLE        → RECORDING     when pressure >= START_THRESHOLD
    #   RECORDING   → ARMED         when pressure >= PEAK_THRESHOLD
    #   ARMED       → IDLE          when pressure <= STOP_THRESHOLD
    global recording, peak_reached

    # Start recording
    if not recording and MPaPressure >= START_THRESHOLD:
        recording = True
        peak_reached = False
        print(f"  [+] Recording started  ({MPaPressure:.2f} MPa)")

    # Mark peak as reached (independent check — must not be elif)
    if recording and MPaPressure >= PEAK_THRESHOLD:
        if peak_reached == False: 
            print(f"  [!] Recording reached peak  ({MPaPressure:.2f} MPa)")
        peak_reached = True

    # Stop recording — only allowed after peak was seen
    if recording and peak_reached and MPaPressure <= STOP_THRESHOLD:
        recording = False
        stop_event.set()
        print(f"  [-] Recording stopped  ({MPaPressure:.2f} MPa)")


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# THREADS
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def data_read_loop(ser):
    # Reader thread: reads binary packets from Arduino, converts to engineering units, updates recording state, and enqueues data.
    while not stop_event.is_set():
        if ser.read(1) == b'\xAA':
            data = ser.read(PACKET_SIZE)

            if len(data) == PACKET_SIZE:
                timestamp, rawPressure, encoderStep = struct.unpack('<LHl', data)
                MPaPressure, mmDisplacement = transform_data(rawPressure, encoderStep)

                update_recording_state(MPaPressure)

                if recording:
                    data_queue.put((timestamp, MPaPressure, mmDisplacement))


def csv_write_loop(file_name):
    # Recorder thread: drains the data queue and writes rows to CSV. Exits only when stop_event is set AND the queue is fully drained.
    with open(file_name, 'w') as csv_file:
        csv_file.write("Timestamp,MPa Pressure,mm Displacement\n")

        while not stop_event.is_set() or not data_queue.empty():
            try:
                timestamp, MPaPressure, mmDisplacement = data_queue.get(timeout=0.1)
                csv_file.write(f"{timestamp},{MPaPressure},{mmDisplacement}\n")
            except queue.Empty:
                pass

    print(f"  [✓] Data saved to {file_name}")


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# MAIN  (entry point — runs setup, starts threads, waits)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

if __name__ == "__main__":

    # --- Setup ---
    com_port  = select_port()
    ser = serial.Serial(com_port, BAUD_RATE)
    time.sleep(2)  # allow Arduino to reset after connection
    print(f"\n{com_port} connected.\n")

    # --- Start threads ---
    reader_thread   = threading.Thread(target=data_read_loop, args=(ser,), daemon=True)
    reader_thread.start()

    while True:
        stop_event.clear()
        recording = False
        peak_reached = False

        file_name = get_csv_filename()
        print("Waiting for pressure to exceed threshold...\n")

        # Relaunch recorder thread (reader stays alive the whole time)
        recorder_thread = threading.Thread(target=csv_write_loop, args=(file_name,))
        recorder_thread.start()

        # Wait for this run to finish naturally (via stop_event)
        recorder_thread.join()

         # Ask if another run is needed
        again = input("\nRun another test? (Enter to continue, exit to exit): ").strip().lower()
        if again == 'exit' or again == 'e':
            break

    ser.close()
    print("Program exited cleanly.")

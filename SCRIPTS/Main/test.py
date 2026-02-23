import serial
import struct
import csv
import time
from multiprocessing import Process, Queue, Event
import matplotlib.pyplot as plt
from collections import deque

PORT = "COM3"
BAUDRATE = 115200
PACKET_SIZE = 10  # 4 + 2 + 4 bytes
CSV_FILE = "data.csv"


# ==========================
# 1️⃣ Serial Reader Process
# ==========================
def serial_reader(data_queue, plot_queue, stop_event):
    ser = serial.Serial(PORT, BAUDRATE)

    while not stop_event.is_set():
        if ser.read(1) == b'\xAA':
            data = ser.read(PACKET_SIZE)

            if len(data) == PACKET_SIZE:
                timestamp, rawPressure, encoderStep = struct.unpack('<LHl', data)

                pressure = 15 / 1023 * rawPressure
                displacement = encoderStep * 0.05 / 2

                row = (timestamp, pressure, displacement)

                # Send to CSV writer
                data_queue.put(row)

                # Send to plotter
                plot_queue.put(row)


# ==========================
# 2️⃣ CSV Writer Process
# ==========================
def csv_writer(data_queue, stop_event):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pressure_MPa", "displacement_mm"])

        while not stop_event.is_set() or not data_queue.empty():
            try:
                row = data_queue.get(timeout=0.1)
                writer.writerow(row)
            except:
                pass


# ==========================
# 3️⃣ Live Plot Process
# ==========================
def live_plot(plot_queue, stop_event):
    plt.ion()
    fig, ax = plt.subplots()

    x_data = deque(maxlen=500)
    y_data = deque(maxlen=500)

    line, = ax.plot([], [])

    ax.set_xlabel("Displacement (mm)")
    ax.set_ylabel("Pressure (MPa)")

    while not stop_event.is_set():
        while not plot_queue.empty():
            _, pressure, displacement = plot_queue.get()
            x_data.append(displacement)
            y_data.append(pressure)

        line.set_xdata(x_data)
        line.set_ydata(y_data)

        ax.relim()
        ax.autoscale_view()

        plt.pause(0.01)

    plt.close()


# ==========================
# 4️⃣ Main Orchestrator
# ==========================
if __name__ == "__main__":
    data_queue = Queue(maxsize=10000)
    plot_queue = Queue(maxsize=2000)
    stop_event = Event()

    reader = Process(target=serial_reader, args=(data_queue, plot_queue, stop_event))
    writer = Process(target=csv_writer, args=(data_queue, stop_event))
    plotter = Process(target=live_plot, args=(plot_queue, stop_event))

    reader.start()
    writer.start()
    plotter.start()

    input("Press ENTER to stop...\n")
    stop_event.set()

    reader.join()
    writer.join()
    plotter.join()
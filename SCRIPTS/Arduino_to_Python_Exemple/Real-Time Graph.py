import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ttkbootstrap as ttk

root = ttk.Window("Machine Essais de Traction", "darkly")
root.title("Machine Essais de Traction")
root.geometry("1600x900")

refreshRate = 1000/10
Sampling = int(refreshRate * 1000)

time = [float(0)]  * Sampling
pressureValue = [0] * Sampling
displacementValue = [0] * Sampling

def graphUpdate():
    global time
    global pressureValue
    global displacementValue

    time = time[1:Sampling]
    time.append(time[-1] + refreshRate / 1000)

    pressureValue = pressureValue[1:Sampling]
    pressureValue.append(int(pressureSlider.get()))
    pressureValueLabel.config(text=pressureValue[-1])
    displacementValue = displacementValue[1:Sampling]
    displacementValue.append(int(displacementSlider.get()))
    displacementValueLabel.config(text=displacementValue[-1])

    pressure_line.set_data(time, pressureValue)
    displacement_line.set_data(time, displacementValue)

    if len(time) > 1:
        pressure_plot.set_xlim(time[0], time[-1])
        displacement_plot.set_xlim(time[0], time[-1])

    pressure_plot.relim()
    pressure_plot.autoscale_view()

    displacement_plot.relim()
    displacement_plot.autoscale_view()

    graph.draw_idle()

    root.after(int(refreshRate), graphUpdate)


pressureSlider = ttk.Scale(root,
    length=350,
    from_=15,
    to=0,
    orient="vertical")
pressureSlider.grid(column=0, row=0, pady=10)
pressureTitleLabel = ttk.Label(root, text="Pressure [MPa]")
pressureTitleLabel.grid(column=0, row=1, padx=10)
pressureValueLabel = ttk.Label(root, text="0")
pressureValueLabel.grid(column=0, row=2)

displacementSlider = ttk.Scale(root,
    length=350,
    from_=150,
    to=0,
    orient="vertical")
displacementSlider.grid(column=1, row=0, pady=10)
displacementTitleLabel = ttk.Label(root, text="Displacement [um]")
displacementTitleLabel.grid(column=1, row=1, padx=10)
displacementValueLabel = ttk.Label(root, text="0")
displacementValueLabel.grid(column=1, row=2)

plt.style.use('dark_background')
graphFigure = plt.figure(figsize=(10, 4))
graphFigure.subplots_adjust(wspace=0.5)

pressure_plot = graphFigure.add_subplot(1, 2, 1)
pressure_plot.set_xlabel("Time [s]")
pressure_plot.set_ylabel("Pressure [MPa]")
pressure_line, = pressure_plot.plot([], [], label="Pressure")

displacement_plot = graphFigure.add_subplot(1, 2, 2)
displacement_plot.set_xlabel("Time [s]")
displacement_plot.set_ylabel("Displacement [um]")
displacement_line, = displacement_plot.plot([], [], label="Displacement")

graph = FigureCanvasTkAgg(graphFigure, master=root)
graph.get_tk_widget().grid(row=0, rowspan=3, column=2)

graphUpdate()
root.mainloop()


import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ttkbootstrap as ttk

root = ttk.Window("GRAPH", "darkly")
root.title("GRAPH")
root.geometry("1600x900")

time = [0]
pressureValueActual = [0]
displacementValueActual = [0]

def values(e):
    global pressureValueActual
    pressureValueActual = int(pressureSlider.get())
    pressureValueLabel.config(text=pressureValueActual)

    global displacementValueActual
    displacementValueActual = int(displacementSlider.get())
    displacementValueLabel.config(text=displacementValueActual)

pressureSlider = ttk.Scale(root,
    length=350,
    from_=15,
    to=0,
    orient="vertical",
    command=values)
pressureSlider.grid(column=0, row=0, pady=10)
pressureTitleLabel = ttk.Label(root, text="Pressure [MPa]")
pressureTitleLabel.grid(column=0, row=1, padx=10)
pressureValueLabel = ttk.Label(root, text="0")
pressureValueLabel.grid(column=0, row=2)

displacementSlider = ttk.Scale(root,
    length=350,
    from_=150,
    to=0,
    orient="vertical",
    command=values)
displacementSlider.grid(column=1, row=0, pady=10)
displacementTitleLabel = ttk.Label(root, text="Displacement [um]")
displacementTitleLabel.grid(column=1, row=1, padx=10)
displacementValueLabel = ttk.Label(root, text="0")
displacementValueLabel.grid(column=1, row=2)

plt.style.use('dark_background')
graphFigure = plt.figure(figsize=(6, 4))
pressure_plot = graphFigure.add_subplot(1, 2, 1)
pressure_plot.set_xlabel("Time [s]")
pressure_plot.set_ylabel("Pressure [MPa]")
displacement_plot = graphFigure.add_subplot(1, 2, 2)
displacement_plot.set_xlabel("Time [s]")
displacement_plot.set_ylabel("Displacement [um]")

graph = FigureCanvasTkAgg(graphFigure, master=root)
graph.get_tk_widget().grid(row=0, rowspan=3, column=2)

def valueUpdate(frame):
    global time
    global pressureValue
    global displacementValue

    time.append(time[-1]+1)
    pressure_plot.clear()
    displacement_plot.clear()
    pressureValue.append(pressureSlider.get())
    pressure_plot.plot(time, pressureValue)
    displacementValue.append(displacementSlider.get())
    displacement_plot.plot(time, displacementValue)


ani = FuncAnimation(graphFigure, valueUpdate, interval=1000)

root.mainloop()

# plt.style.use('dark_background')
#
# index = count()
# x_vals = []
# y_vals = []
#
# def graph(i):
#     x_vals.append(next(index))
#     y_vals.append(random.randint(0, 15))
#
#     plt.cla()
#     plt.plot(x_vals, y_vals)
#
# root = FuncAnimation(plt.gcf(), graph, interval=1000)
#
# plt.tight_layout()
# plt.show()

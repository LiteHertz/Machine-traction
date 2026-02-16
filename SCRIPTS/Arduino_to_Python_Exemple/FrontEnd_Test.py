import ttkbootstrap as ttk
from tkinter import Canvas

root = ttk.Window("Test", "darkly")

blank_window = Canvas(root, width=200, height=120)
blank_window.pack()

ledGreen = blank_window.create_oval(20, 20, 60, 60, fill="green")
ledYellow = blank_window.create_oval(80, 20, 120, 60, fill="yellow")
ledRed = blank_window.create_oval(140, 20, 180, 60, fill="red")



root.mainloop()


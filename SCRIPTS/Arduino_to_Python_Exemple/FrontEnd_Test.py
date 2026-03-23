import ttkbootstrap as ttk
from tkinter import Canvas, Text, END
import time as t

root = ttk.Window("Test", "darkly")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)


lightFrame = Canvas(root, width=300, height=80)
lightFrame.grid(row=1, column=0, columnspan=3)

dx = 40
ledGreen = lightFrame.create_oval(50, 20, 50+dx, 60, fill="gray")
ledYellow = lightFrame.create_oval(130, 20, 130+dx, 60, fill="gray")
ledRed = lightFrame.create_oval(210, 20, 210+dx, 60, fill="gray")

def toggle(led, color):
    if lightFrame.itemcget(led, "fill") == "gray":
        lightFrame.itemconfig(led, fill=color)
    else:
        lightFrame.itemconfig(led, fill="gray")

title = Text(root, height=1, width=20, font=("Arial", 18))
title.grid(row=0, column=0, columnspan=3)

title.tag_configure("red", foreground="red")
title.tag_configure("green", foreground="green")
title.tag_configure("yellow", foreground="yellow")
title.tag_configure("center", justify="center")

cnt = 0
def color_changing_title():
    global title
    global cnt

    title.delete("1.0", "end")

    if cnt == 0:
        title.insert(END, "Three ", "green")
        title.insert(END, "Lights ", "yellow")
        title.insert(END, "Test", "red")
        cnt += 1
    elif cnt == 1:
        title.insert(END, "Three ", "red")
        title.insert(END, "Lights ", "green")
        title.insert(END, "Test", "yellow")
        cnt += 1
    elif cnt == 2:
        title.insert(END, "Three ", "yellow")
        title.insert(END, "Lights ", "red")
        title.insert(END, "Test", "green")
        cnt = 0

    title.tag_add("center", "1.0", "end")
    root.after(500, color_changing_title)

buttonFrame = ttk.Frame(root)
buttonFrame.grid(row=2, column=0, columnspan=3)

buttonGreen = ttk.Button(buttonFrame, text="Green", command=lambda: toggle(led=ledGreen,color="light green"), width=6)
buttonGreen.grid(row=0, column=0, padx=10)

buttonYellow = ttk.Button(buttonFrame, text="Yellow", command=lambda: toggle(led=ledYellow,color="yellow"), width=6)
buttonYellow.grid(row=0, column=1, padx=10)

buttonRed = ttk.Button(buttonFrame, text="Red", command=lambda: toggle(led=ledRed,color="red"), width=6)
buttonRed.grid(row=0, column=2, padx=10)


color_changing_title()
root.mainloop()
exit()


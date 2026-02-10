import tkinter as tk
#from ttkbootstrap import Style

#style = Style(theme="darkly")

label = tk.Label(
    text="THIS IS A LABEL",
    foreground="white",  # Set the text color to white
    background="black"  # Set the background color to black
)

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

entry = tk.Entry(
    width=25,
    bg="purple",
    fg="blue",
)

label.pack()
button.pack()
entry.pack()

window = tk.Tk()
window.title("Machine Traction")
window.geometry("400x300")
window.mainloop()
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def select_file():
    global filepath 
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "r") as input_file:
        global text
        text = input_file.read().splitlines()
    root.title(f"Simple Text Editor - {filepath}")
    root.destroy()


def get_text():
    return text


def get_manual_input():
    minterms = ",".join(str(e1.get()).split())
    dc = ",".join(str(e2.get()).split())
    global text
    text = list()
    text.append("m(" + minterms + ")+d(" + dc + ")")
    root.destroy()


def manual_input():
    manual_enter = tk.Toplevel(root)

    manual_enter.title("Manually Enter Input")
    manual_enter.geometry("600x120")
    newFrame = tk.Frame(manual_enter)

    global e1
    global e2

    tk.Label(manual_enter, text="Enter just the terms with a single space between them.").grid(row=0, column = 0)

    tk.Label(manual_enter, text="Minterms:").grid(row=2, column = 0)
    tk.Label(manual_enter, text="Don't Cares:").grid(row=3, column=0)

    e1 = tk.Entry(manual_enter, width = 50)
    e2 = tk.Entry(manual_enter, width = 50)

    e1.grid(row=2, column=1)
    e2.grid(row=3, column=1)

    sub = tk.Button(manual_enter, text='Submit', command=get_manual_input).grid(row=5, column=1, sticky=tk.W, pady=4)


#Root frame
root = tk.Tk()
root.title("Boolean Logic Minimizer")
root.geometry("500x120")
frame = tk.Frame(root)

label = tk.Label(root, fg="dark green",font=("Helvetica", 16), borderwidth=15)
label.config(text="Select input type")
label.pack()

frame.pack()

button = tk.Button(frame, text="File", command=select_file, width=10, height=3)
button.pack(side=tk.LEFT)
slogan = tk.Button(frame, text="Manual", command=manual_input, width=10, height=3)
slogan.pack(side=tk.LEFT)

root.mainloop()
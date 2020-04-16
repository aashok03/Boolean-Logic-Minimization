import tkinter as tk
from tkinter import *

def show_output(all_answers):

	parent = tk.Tk()
	parent.title("Boolean Logic Minimizer")
	parent.geometry("750x400")
	canvas = tk.Canvas(parent)
	scroll_y = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

	frame = tk.Frame(canvas)

	tk.Label(frame, fg="dark green", text="Minimized Functions:", font=("Helvetica", 16), borderwidth=20).pack()

	# group of widgets
	for i in range(len(all_answers)):
	    tk.Label(frame, text=all_answers[i], font=("Helvetica", 12), borderwidth=15).pack()

	tk.Label(frame, fg="blue", text="Step-by-step calculations for each inputted function can be viewed on the terminal.", font=("Helvetica", 14), borderwidth=20).pack()
	tk.Label(frame, fg="blue", text="SOP and POS calculations can be seen individually.", font=("Helvetica", 14), borderwidth=20).pack()

	# put the frame in the canvas
	canvas.create_window(0, 0, anchor='nw', window=frame)
	# make sure everything is displayed before configuring the scrollregion
	canvas.update_idletasks()

	canvas.configure(scrollregion=canvas.bbox('all'), 
	                 yscrollcommand=scroll_y.set)
	                 
	canvas.pack(fill='both', expand=True, side='left')
	scroll_y.pack(fill='y', side='right')

	parent.mainloop()
import tkinter as tk

root = tk.Tk()

tk.Label(root, text="Username").grid(row=0, column=0)
tk.Label(root, text="Password").grid(row=1, column=0)

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

root.mainloop()

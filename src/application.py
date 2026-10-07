import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from programState import ProgramState

class Application(ttk.Frame):
	def __init__(self, container):
		super().__init__(container)
		self.container = container

		options = {'padx': 5, 'pady': 5}

		# label
		self.label = ttk.Label(self, text='Bye, Tkinter!')
		self.label.pack(**options)

		# button
		self.button = ttk.Button(self, text='Click Me')
		self.button['command'] = self.button_clicked
		self.button.pack(**options)

		# show the frame on the container
		self.pack(**options)

	def button_clicked(self):
		self.container.change_state(ProgramState.MainMenu)

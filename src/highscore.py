import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from programState import ProgramState

class Highscore(ttk.Frame):
	def __init__(self, container):
		super().__init__(container)
		self.container = container

		options = {'padx': 5, 'pady': 5}

		# label
		self.label = ttk.Label(self, text='Fastest Times')
		self.label.pack(**options)

		self.button = ttk.Button(self, text='Back')
		self.button['command'] = lambda: self.button_clicked(ProgramState.MainMenu)
		self.button.pack(**options)

		# show the frame on the container
		self.pack(**options)

	def button_clicked(self, scene):
		self.container.change_state(scene)

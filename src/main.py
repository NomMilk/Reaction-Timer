import tkinter as tk
from highscore import Highscore
from mainMenu import MainMenu 
from application import Application
from programState import ProgramState

class ReactionApp(tk.Tk):
	def __init__(self):
		super().__init__()

		self.title("Reaction App")
		self.geometry("800x600")
		self.resizable(False, False)

		self.state = ProgramState.MainMenu
		self.frame = None

		self.change_state(self.state)

	def change_state(self, new_state):
		if self.frame is not None:
			self.frame.destroy()

		self.state = new_state

		if self.state == ProgramState.MainMenu:
			self.frame = MainMenu(self)

		elif self.state == ProgramState.Application:
			self.frame = Application(self)

		elif self.state == ProgramState.Normal:
			self.frame = Application(self)

		elif self.state == ProgramState.Advance:
			self.frame = Application(self)

		elif self.state == ProgramState.Highscore:
			self.frame = Highscore(self)

		self.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
	app = ReactionApp()
	app.mainloop()

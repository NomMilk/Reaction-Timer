import tkinter as tk
from enum import Enum

#the program states will have frames associated with them
class ProgramState(Enum):
	MainMenu = 0
	Login = 1
	Application = 2
	Highscore = 3
 
class ReactionApp(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Reaction App")
 
if __name__ == "__main__":
	app = ReactionApp()
	app.mainloop()

import tkinter as tk
import theme
from highscore import Highscore
from mainMenu import MainMenu
from application import Application
from normal import NormalMode
from movement import MovementMode
from programState import ProgramState

# Dictionary: which screen class belongs to each program state.
SCREENS = {
    ProgramState.MainMenu: MainMenu,
    ProgramState.Application: Application,
    ProgramState.Normal: NormalMode,
    ProgramState.Movement: MovementMode,
    ProgramState.Highscore: Highscore,
}


class ReactionApp(tk.Tk):
    """The main window. It shows one screen (frame) at a time."""

    def __init__(self):
        super().__init__()

        self.title("Reaction App")
        self.geometry("800x600")
        self.minsize(640, 480)

        theme.apply_theme(self)

        self.fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        self.current_state = ProgramState.MainMenu
        self.frame = None

        self.change_state(self.current_state)

    def toggle_fullscreen(self, event=None):
        """Switch full screen on or off (F11)."""
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        """Leave full screen (Escape)."""
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def change_state(self, new_state):
        """Remove the current screen and show the one for `new_state`."""
        if self.frame is not None:
            self.frame.destroy()

        self.current_state = new_state
        self.frame = SCREENS[new_state](self)
        self.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = ReactionApp()
    app.mainloop()

# Justin's version

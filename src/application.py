from tkinter import ttk
from programState import ProgramState


class Application(ttk.Frame):
    """The Modes menu: choose Normal or Movement mode."""

    def __init__(self, container):
        super().__init__(container)
        self.container = container

        options = {'padx': 5, 'pady': 5}

        # inner frame stays centred however large the window is
        inner = ttk.Frame(self)
        inner.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(inner, text='Modes').pack(**options)

        normal_button = ttk.Button(inner, text='Normal Mode')
        normal_button['command'] = lambda: self.button_clicked(ProgramState.Normal)
        normal_button.pack(**options)

        movement_button = ttk.Button(inner, text='Movement Mode')
        movement_button['command'] = lambda: self.button_clicked(ProgramState.Movement)
        movement_button.pack(**options)

        back_button = ttk.Button(inner, text='Back')
        back_button['command'] = lambda: self.button_clicked(ProgramState.MainMenu)
        back_button.pack(**options)

        self.pack(fill='both', expand=True)

    def button_clicked(self, scene):
        """Ask the main window to switch to another screen."""
        self.container.change_state(scene)

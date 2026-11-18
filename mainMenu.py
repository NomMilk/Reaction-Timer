from tkinter import ttk
import theme
from programState import ProgramState


class MainMenu(ttk.Frame):
    """The first screen: Start or view the high scores."""

    def __init__(self, container):
        super().__init__(container)
        self.container = container

        options = {'padx': 5, 'pady': 6}

        # inner frame stays centred however large the window is
        inner = ttk.Frame(self)
        inner.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(inner, text='Reaction Timer', style='MenuTitle.TLabel').pack(pady=(0, 4))
        ttk.Label(inner, text='How fast can you react?',
                  style='MenuSubtitle.TLabel').pack(pady=(0, 26))

        start_button = ttk.Button(inner, text='Start', style='MenuAccent.TButton',
                                  width=22, cursor='hand2')
        start_button['command'] = lambda: self.button_clicked(ProgramState.Application)
        start_button.pack(**options)

        highscore_button = ttk.Button(inner, text='Highscore', style='Menu.TButton',
                                      width=22, cursor='hand2')
        highscore_button['command'] = lambda: self.button_clicked(ProgramState.Highscore)
        highscore_button.pack(**options)

        theme.CrosshairPicker(inner).pack(pady=(22, 0))

        self.pack(fill='both', expand=True)

    def button_clicked(self, scene):
        """Ask the main window to switch to another screen."""
        self.container.change_state(scene)

from tkinter import ttk
from programState import ProgramState
from scores import MODES, top_scores


class Highscore(ttk.Frame):
    """Shows the five fastest times for each mode."""

    def __init__(self, container):
        super().__init__(container)
        self.container = container

        options = {'padx': 5, 'pady': 5}

        # inner frame stays centred however large the window is
        inner = ttk.Frame(self)
        inner.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(inner, text='Fastest Times', font=("Arial", 18, "bold")).pack(**options)

        for mode in MODES:
            ttk.Label(inner, text=f'{mode} Mode', font=("Arial", 14, "bold")).pack(**options)
            ttk.Label(inner, text=self.format_scores(mode), justify="center").pack(**options)

        back_button = ttk.Button(inner, text='Back')
        back_button['command'] = lambda: self.button_clicked(ProgramState.MainMenu)
        back_button.pack(**options)

        self.pack(fill='both', expand=True)

    def format_scores(self, mode):
        """Return the text for one mode's score list."""
        entries = top_scores(mode)
        if not entries:
            return "No scores yet."
        lines = [f"{rank}. {entry['best']} ms  (average {entry.get('average', '?')} ms)  "
                 f"{entry.get('date', '')}"
                 for rank, entry in enumerate(entries, start=1)]  # list comprehension
        return "\n".join(lines)

    def button_clicked(self, scene):
        """Ask the main window to switch to another screen."""
        self.container.change_state(scene)

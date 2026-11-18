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

        ttk.Label(inner, text='Fastest Times', style='Heading.TLabel').pack(pady=(0, 10))

        for mode in MODES:
            card = ttk.Frame(inner, style='Card.TFrame', padding=(24, 12))
            card.pack(fill='x', **options)
            ttk.Label(card, text=f'{mode} Mode', style='CardHeading.TLabel').pack(anchor='w', pady=(0, 6))
            ttk.Label(card, text=self.format_scores(mode), style='Card.TLabel',
                      justify="left").pack(anchor='w')

        back_button = ttk.Button(inner, text='Back', width=22, cursor='hand2')
        back_button['command'] = lambda: self.button_clicked(ProgramState.MainMenu)
        back_button.pack(padx=5, pady=(14, 5))

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

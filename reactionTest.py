import tkinter as tk
from tkinter import ttk
import theme
from programState import ProgramState
from scores import calculate_stats, save_score

ROUNDS = 5


class ReactionTest(theme.Effects, ttk.Frame):
    """Shared screen for both game modes.

    It draws the rectangle, keeps the list of reaction times, and shows the
    final results. Subclasses set `mode_name` and `program_state`, and write
    `start_round` and `on_click`.
    """
    mode_name = ""
    program_state = None

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.times = []            # reaction times in ms, one per finished round
        self.pending_job = None    # id of the timer waiting to fire, if any

        self.info = ttk.Label(self, text="", style="Info.TLabel")
        self.info.pack(padx=5, pady=(16, 4))

        self.message = (theme.SURFACE_ALT, "", theme.TEXT)   # last message drawn, for redrawing on resize
        self.canvas = tk.Canvas(self, width=600, height=350, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=24, pady=8)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Configure>", self.redraw)
        self.setup_effects()

        self.quit_button = ttk.Button(self, text="Quit to Menu", width=18,
                                      cursor="hand2", command=self.go_to_menu)
        self.quit_button.pack(padx=5, pady=(8, 16))

    def start_round(self):
        """Begin one round. Written by each mode."""
        raise NotImplementedError

    def on_click(self, event):
        """React to a click on the canvas. Written by each mode."""
        raise NotImplementedError

    def schedule(self, delay_ms, callback):
        """Run `callback` after `delay_ms`, remembering the timer so it can be cancelled."""
        self.cancel_pending()
        self.pending_job = self.after(delay_ms, callback)

    def cancel_pending(self):
        """Cancel the waiting timer, if there is one."""
        if self.pending_job is not None:
            self.after_cancel(self.pending_job)
            self.pending_job = None

    def destroy(self):
        """Stop any timer before the screen is removed, so it cannot fire late."""
        self.cancel_pending()
        self.cancel_effects()
        super().destroy()

    def draw_message(self, color, text, text_color=theme.TEXT):
        """Remember a message, then fill the canvas with its color and centre the text."""
        self.message = (color, text, text_color)
        self.redraw()

    def redraw(self, event=None):
        """Draw the current message to fit the canvas. Also runs when the window is resized."""
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        color, text, text_color = self.message
        self.draw_panel(width, height, color)
        self.canvas.create_text(width / 2, height / 2, text=text, fill=text_color,
                                font=(theme.FONT, max(16, height // 14), "bold"),
                                width=max(100, width - 40), justify="center", tags="scene")
        self.draw_extras()
        self.finish_draw()

    def record_time(self, milliseconds):
        """Store a finished round's time (rounded to whole ms) and return it."""
        reaction = round(milliseconds)
        self.times.append(reaction)
        return reaction

    def go_to_menu(self):
        """Leave the game and return to the main menu."""
        self.container.change_state(ProgramState.MainMenu)

    def finish(self):
        """Save the score and replace the game with the results screen."""
        best, average = calculate_stats(self.times)
        saved = save_score(self.mode_name, best, average)

        self.cancel_effects()
        for widget in self.winfo_children():
            widget.destroy()
        box = ttk.Frame(self, style="Card.TFrame", padding=(48, 28))   # centred however large the window is
        box.place(relx=0.5, rely=0.5, anchor="center")

        lines = [f"Round {number}: {time} ms"
                 for number, time in enumerate(self.times, start=1)]  # list comprehension
        ttk.Label(box, text=f"{self.mode_name} Mode Complete!",
                  style="CardTitle.TLabel").pack(padx=5, pady=(0, 12))
        ttk.Label(box, text="\n".join(lines), justify="center",
                  style="Card.TLabel").pack(padx=5, pady=5)
        ttk.Label(box, text=f"Best reaction time: {best} ms",
                  style="CardHeading.TLabel").pack(padx=5, pady=(12, 2))
        ttk.Label(box, text=f"Average reaction time: {average} ms",
                  style="Stat.TLabel").pack(padx=5, pady=2)
        note = "Score added to the high scores." if saved else "Could not save the score file."
        ttk.Label(box, text=note, style="CardMuted.TLabel").pack(padx=5, pady=(8, 12))

        ttk.Button(box, text="Play Again", style="Accent.TButton", width=22, cursor="hand2",
                   command=lambda: self.container.change_state(self.program_state)
                   ).pack(padx=5, pady=5)
        ttk.Button(box, text="Back to Menu", width=22, cursor="hand2",
                   command=self.go_to_menu).pack(padx=5, pady=5)

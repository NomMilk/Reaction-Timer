import random
import time
from reactionTest import ReactionTest, ROUNDS
from programState import ProgramState


class NormalMode(ReactionTest):
    """Click the rectangle as soon as it turns green."""
    mode_name = "Normal"
    program_state = ProgramState.Normal

    def __init__(self, container):
        super().__init__(container)
        self.phase = "waiting"   # waiting, too_soon, go, or result
        self.go_time = 0.0
        self.start_round()

    def start_round(self):
        """Show the red rectangle and pick a random delay before it turns green."""
        self.phase = "waiting"
        self.info.config(text=f"Round {len(self.times) + 1} of {ROUNDS}")
        self.draw_message("red", "Wait for green")
        self.schedule(random.randint(1500, 4000), self.turn_green)

    def turn_green(self):
        """Turn the rectangle green and start the stopwatch."""
        self.phase = "go"
        self.draw_message("green", "Click now!")
        self.canvas.update_idletasks()   # make sure it is drawn before timing starts
        self.go_time = time.perf_counter()

    def on_click(self, event):
        """Decide what a click means based on the current phase."""
        if self.phase == "waiting":            # clicked before green
            self.cancel_pending()
            self.phase = "too_soon"
            self.draw_message("blue", "Too soon! Click to try again.")
        elif self.phase == "too_soon":         # retry the same round
            self.start_round()
        elif self.phase == "go":               # a valid click
            reaction = self.record_time((time.perf_counter() - self.go_time) * 1000)
            self.phase = "result"
            self.draw_message("#444444", f"{reaction} ms\nClick to continue")
        elif self.phase == "result":
            if len(self.times) == ROUNDS:
                self.finish()
            else:
                self.start_round()

import random
import time
from reactionTest import ReactionTest, ROUNDS
import theme
from programState import ProgramState

CIRCLE_RADIUS = 20
COUNTDOWN_START = 3


class MovementMode(ReactionTest):
    """Wait for a small circle to appear somewhere, then click it as fast as you can."""
    mode_name = "Movement"
    program_state = ProgramState.Movement

    def __init__(self, container):
        super().__init__(container)
        self.phase = "countdown"   # countdown, waiting, too_soon, circle, or pause
        self.show_time = 0.0
        self.circle_position = (0.5, 0.5)   # circle centre as fractions of the canvas size
        self.retry_countdown = False   # after a too-soon click, restart the countdown?
        self.start_countdown()

    def start_countdown(self):
        """Begin the 3-2-1 countdown on a blank area."""
        self.phase = "countdown"
        self.info.config(text="Get ready...")
        self.run_countdown(COUNTDOWN_START)

    def run_countdown(self, seconds_left):
        """Show the number, then call itself again one second later."""
        if seconds_left == 0:
            self.start_round()
            return
        self.draw_message(theme.GAME_BG, str(seconds_left))
        self.schedule(1000, lambda: self.run_countdown(seconds_left - 1))

    def start_round(self):
        """Show a blank area and pick a random delay before the circle appears."""
        self.phase = "waiting"
        self.info.config(text=f"Round {len(self.times) + 1} of {ROUNDS}")
        self.draw_message(theme.GAME_BG, "")
        self.schedule(random.randint(1000, 4000), self.show_circle)

    def show_circle(self):
        """Pick a random spot for the circle, draw it, and start the stopwatch."""
        self.phase = "circle"
        self.circle_position = (random.uniform(0.05, 0.95), random.uniform(0.08, 0.92))
        self.redraw()
        self.canvas.update_idletasks()   # make sure it is drawn before timing starts
        self.show_time = time.perf_counter()
        x, y = self.circle_center()
        self.spawn_ring(x, y, theme.CIRCLE_OUTLINE, CIRCLE_RADIUS, CIRCLE_RADIUS + 24, 400)

    def circle_center(self):
        """Return the circle's centre in pixels for the current canvas size."""
        return (self.circle_position[0] * self.canvas.winfo_width(),
                self.circle_position[1] * self.canvas.winfo_height())

    def draw_extras(self):
        if self.phase == "circle":
            x, y = self.circle_center()
            self.canvas.create_oval(x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
                                    x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
                                    fill=theme.CIRCLE, outline=theme.CIRCLE_OUTLINE, width=3,
                                    tags="scene")

    def clicked_circle(self, event):
        """Return True if the click landed inside the circle."""
        x, y = self.circle_center()
        return (event.x - x) ** 2 + (event.y - y) ** 2 <= CIRCLE_RADIUS ** 2

    def on_click(self, event):
        """Decide what a click means based on the current phase."""
        if self.phase in ("countdown", "waiting"):     # clicked too early
            was_countdown = self.phase == "countdown"
            self.cancel_pending()
            self.phase = "too_soon"
            self.retry_countdown = was_countdown
            self.draw_message(theme.EARLY, "Too soon! Don't click until the circle appears. "
                                      "Click to try again.")
            self.click_effect(event.x, event.y, "TOO SOON", theme.MISS)
        elif self.phase == "too_soon":
            if self.retry_countdown:
                self.start_countdown()
            else:
                self.start_round()
        elif self.phase == "circle":
            if self.clicked_circle(event):
                reaction = self.record_time((time.perf_counter() - self.show_time) * 1000)
                self.phase = "pause"
                self.draw_message(theme.GAME_BG, f"{reaction} ms")
                self.click_effect(event.x, event.y, f"{reaction}ms", theme.HIT)
                self.schedule(1200, self.next_step)
            else:
                self.info.config(text="Missed! Click on the circle.")
                self.click_effect(event.x, event.y, "MISS", theme.MISS)

    def next_step(self):
        """After the short pause, go to the next round or show the results."""
        if len(self.times) == ROUNDS:
            self.finish()
        else:
            self.start_round()

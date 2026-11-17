import json
import os
from datetime import date

# Tuple: the game modes never change, so a tuple fits.
MODES = ("Normal", "Movement")
SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscores.json")


def calculate_stats(times):
    """Return (best, average) for a list of reaction times in milliseconds."""
    best = min(times)
    average = round(sum(times) / len(times), 1)
    return best, average


def load_scores():
    """Return a dictionary {mode: [score entries]} read from the score file.

    A missing or damaged file gives empty lists instead of crashing the program.
    """
    scores = {mode: [] for mode in MODES}  # dictionary comprehension
    try:
        with open(SCORE_FILE, "r") as file:
            saved = json.load(file)
        for mode in MODES:
            if isinstance(saved.get(mode), list):
                scores[mode] = saved[mode]
    except (OSError, ValueError, AttributeError):
        pass  # no file yet, or it is unreadable: start fresh
    return scores


def save_score(mode, best, average):
    """Add one finished game to the score file. Return True if it was saved."""
    scores = load_scores()
    scores[mode].append({"best": best, "average": average, "date": str(date.today())})
    try:
        with open(SCORE_FILE, "w") as file:
            json.dump(scores, file, indent=2)
        return True
    except OSError:
        return False


def top_scores(mode, count=5):
    """Return the `count` fastest entries for a mode, fastest first."""
    entries = load_scores()[mode]
    valid = [e for e in entries
             if isinstance(e, dict) and isinstance(e.get("best"), (int, float))]
    return sorted(valid, key=lambda entry: entry["best"])[:count]

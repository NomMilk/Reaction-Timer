"""Three test cases. Expected answers were worked out by hand first.

Run with:  python tests.py
"""
import os
import tempfile
import scores


def test_stats():
    """Times 300, 250, 400, 350, 200: best is 200, average is 1500 / 5 = 300.0."""
    assert scores.calculate_stats([300, 250, 400, 350, 200]) == (200, 300.0)


def test_top_scores_sorted():
    """Saving 300, 200, 250 and asking for the top 2 should give 200 then 250."""
    scores.SCORE_FILE = os.path.join(tempfile.mkdtemp(), "test_scores.json")
    for best in (300, 200, 250):
        assert scores.save_score("Normal", best, best + 10)
    assert [entry["best"] for entry in scores.top_scores("Normal", 2)] == [200, 250]


def test_damaged_file():
    """A damaged score file must not crash: every mode gets an empty list."""
    scores.SCORE_FILE = os.path.join(tempfile.mkdtemp(), "bad.json")
    with open(scores.SCORE_FILE, "w") as file:
        file.write("not json {{{")
    assert scores.load_scores() == {"Normal": [], "Movement": []}


if __name__ == "__main__":
    test_stats()
    test_top_scores_sorted()
    test_damaged_file()
    print("All 3 tests passed.")

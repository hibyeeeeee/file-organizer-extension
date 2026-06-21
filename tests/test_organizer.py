import os
from organizer import cleanup, stats, load_state


def test_cleanup_creates_folders(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")

    cleanup(tmp_path)

    assert (tmp_path / "txt" / "test.txt").exists()


def test_stats_counts(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("x")
    (tmp_path / "c.jpg").write_text("x")

    stats(tmp_path)

    captured = capsys.readouterr().out
    assert "txt" in captured
    assert "jpg" in captured


def test_history_logged(tmp_path):
    file = tmp_path / "test2.txt"
    file.write_text("hi")

    cleanup(tmp_path)

    state = load_state()
    assert len(state["history"]) > 0
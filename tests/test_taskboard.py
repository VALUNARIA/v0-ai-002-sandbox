import pytest

from taskboard import TaskBoard


def test_add_and_list_open_tasks():
    board = TaskBoard()
    board.add("first")
    board.add("second")
    assert board.open_titles() == ["first", "second"]


def test_complete_removes_task_from_open_titles():
    board = TaskBoard()
    board.add("first")
    board.complete(0)
    assert board.open_titles() == []


def test_blank_title_is_rejected():
    board = TaskBoard()
    with pytest.raises(ValueError, match="title must not be empty"):
        board.add("   ")


def test_summary_for_empty_board():
    board = TaskBoard()
    assert board.summary() == {
        "total": 0,
        "completed": 0,
        "open": 0,
        "completion_rate": 0.0,
    }


def test_summary_with_one_of_two_tasks_completed():
    board = TaskBoard()
    board.add("first")
    board.add("second")
    board.complete(0)
    assert board.summary() == {
        "total": 2,
        "completed": 1,
        "open": 1,
        "completion_rate": 0.5,
    }

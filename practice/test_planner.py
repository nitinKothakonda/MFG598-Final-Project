import logging

from planner import astar

GRID_A = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0],
]


def test_finds_shortest_path_on_known_grid():
    path = astar(GRID_A, (0, 0), (3, 3))
    assert path[0] == (0, 0)
    assert path[-1] == (3, 3)
    assert len(path) - 1 == 6  # the cheapest route takes 6 steps


def test_returns_none_when_goal_is_walled_off():
    grid = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    assert astar(grid, (0, 0), (2, 2)) is None


def test_blocked_start_returns_none_and_logs_warning(caplog):
    with caplog.at_level(logging.WARNING, logger="planner"):
        assert astar(GRID_A, (1, 0), (3, 3)) is None
    assert "blocked" in caplog.text


def test_time_budget_exceeded_returns_none_and_logs_error(caplog):
    with caplog.at_level(logging.ERROR, logger="planner"):
        assert astar(GRID_A, (0, 0), (3, 3), time_budget_s=-1) is None
    assert "time budget" in caplog.text

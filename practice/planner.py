"""A small A* grid planner with logging and a time budget.

Grid convention: grid[row][col], 0 = free cell, 1 = wall.
Cells are (row, col) tuples. Moves are 4-directional, each step costs 1.
"""
import heapq
import logging
import time

log = logging.getLogger("planner")


def manhattan(a, b):
    """Admissible heuristic for 4-directional moves with step cost 1."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal, time_budget_s=1.0):
    """Return the cheapest path as a list of (row, col) cells, or None.

    None means: start or goal is blocked, no path exists, or the time
    budget ran out. The reason is written to the log.
    """
    rows, cols = len(grid), len(grid[0])

    def is_free(cell):
        r, c = cell
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0

    if not is_free(start) or not is_free(goal):
        log.warning("start %s or goal %s is blocked or outside the grid", start, goal)
        return None

    deadline = time.monotonic() + time_budget_s
    open_heap = [(manhattan(start, goal), 0, start)]  # (f, g, cell)
    best_g = {start: 0}
    came_from = {}
    expanded = 0

    while open_heap:
        if time.monotonic() > deadline:
            log.error(
                "time budget of %.2fs exceeded after %d expansions", time_budget_s, expanded
            )
            return None

        _, cost, cell = heapq.heappop(open_heap)
        if cost > best_g[cell]:
            continue  # stale heap entry: a cheaper route to this cell was found later

        if cell == goal:
            path = [cell]
            while cell in came_from:
                cell = came_from[cell]
                path.append(cell)
            path.reverse()
            log.info("path found: %d steps, %d cells expanded", len(path) - 1, expanded)
            return path

        expanded += 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cell[0] + dr, cell[1] + dc)
            if not is_free(nxt):
                continue
            new_cost = cost + 1
            if new_cost < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_cost
                came_from[nxt] = cell
                heapq.heappush(open_heap, (new_cost + manhattan(nxt, goal), new_cost, nxt))

    log.info("no path from %s to %s (%d cells expanded)", start, goal, expanded)
    return None

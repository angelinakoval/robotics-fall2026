"""Mission 1 starter, created in student_submission/mission_1/planners.py.

Open that submission file in your editor and implement the four functions.
The guide creates it automatically and never overwrites an existing file.

Each function receives ctx with start, goal, grid, heuristic(cell) and
expand(cell, frontier_size). Return a list of (row, column) cells including
start and goal, or [] after exhausting the search. Call ctx.expand once per
expanded node. Record the actual frontier size, not the number of visited cells.
The runner enforces an expansion budget and a separate process time limit.
Use only the Python standard library. Do not import planning.reference_path.
When a free start is already the goal, return the single starting cell with
zero moves. No expansion is required for that case. Use the six small checks
on the Mission 1 page before running the full canonical-map evaluation.
"""
from collections import deque
from heapq import heappush, heappop
from planning.core import reconstruct


def bfs(ctx):
    """FIFO queue. Mark discovered cells when enqueuing and store parents.
    Use ctx.expand(current, len(frontier)+1) to obtain neighbours.
    BFS minimizes number of unit-cost edges, not execution time on a robot.
    """
    start = ctx.start
    goal = ctx.goal

    if ctx.grid[start[0]][start[1]] == 1 or ctx.grid[goal[0]][goal[1]] == 1:
        return []

    if start == goal:
        return [start]

    frontier = deque([start])
    parent = {start: None}

    while frontier:
        current = frontier.popleft()

        if current == goal:
            return reconstruct(parent, goal)

        for nxt in ctx.expand(current, len(frontier) + 1):
            if nxt not in parent:
                parent[nxt] = current
                frontier.append(nxt)

    return []


def dfs(ctx):
    """LIFO stack. Track discovered cells and parents to avoid cycles.
    A valid DFS path need not be shortest. Keep the supplied neighbour order.
    """
    start = ctx.start
    goal = ctx.goal

    if ctx.grid[start[0]][start[1]] == 1 or ctx.grid[goal[0]][goal[1]] == 1:
        return []

    if start == goal:
        return [start]

    frontier = [start]
    parent = {start: None}

    while frontier:
        current = frontier.pop()

        if current == goal:
            return reconstruct(parent, goal)

        for nxt in ctx.expand(current, len(frontier) + 1):
            if nxt not in parent:
                parent[nxt] = current
                frontier.append(nxt)

    return []


def iddfs(ctx):
    """Run depth-limited DFS with bounds 0, 1, 2, ... .
    Prevent cycles on the current path. Do not keep a global visited set across
    depth limits. Count expansions again on every iteration. Return [] only
    after exhaustive failure. Catch no budget exceptions. The runner records
    resource_limit honestly if this expensive method reaches its budget.
    """
    start = ctx.start
    goal = ctx.goal

    if ctx.grid[start[0]][start[1]] == 1 or ctx.grid[goal[0]][goal[1]] == 1:
        return []

    if start == goal:
        return [start]

    limit = 0
    while True:
        frontier = [(start, 0)]
        path = []
        on_path = set()
        cutoff = False

        while frontier:
            current, depth = frontier.pop()

            while len(path) > depth:
                on_path.discard(path.pop())
            path.append(current)
            on_path.add(current)

            if current == goal:
                return list(path)

            if depth == limit:
                cutoff = True
                continue

            for nxt in ctx.expand(current, len(frontier) + 1):
                if nxt not in on_path:
                    frontier.append((nxt, depth + 1))

        if not cutoff:
            return []

        limit += 1


def astar(ctx):
    """Use a heap ordered by g + ctx.heuristic(cell).
    Keep best g costs and parents. Ignore outdated heap entries. Each edge
    costs 1. Stop when the goal is removed from the priority queue.
    """
    start = ctx.start
    goal = ctx.goal

    if ctx.grid[start[0]][start[1]] == 1 or ctx.grid[goal[0]][goal[1]] == 1:
        return []

    if start == goal:
        return [start]

    frontier = []
    heappush(frontier, (ctx.heuristic(start), 0, start))
    g = {start: 0}
    parent = {start: None}

    while frontier:
        priority, cost_so_far, current = heappop(frontier)

        if cost_so_far > g[current]:
            continue

        if current == goal:
            return reconstruct(parent, goal)

        for nxt in ctx.expand(current, len(frontier) + 1):
            new_g = cost_so_far + 1
            if nxt not in g or new_g < g[nxt]:
                g[nxt] = new_g
                parent[nxt] = current
                heappush(frontier, (new_g + ctx.heuristic(nxt), new_g, nxt))

    return []

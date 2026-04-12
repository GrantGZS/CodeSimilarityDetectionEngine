from collections import deque
import sys
import ast
sys.setrecursionlimit(10**6)

def num_islands_dfs(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid)
    count = 0

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or str(grid[r][c]) == "0":
            return
        grid[r][c] = "0"
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if str(grid[r][c]) == "1":
                count += 1
                dfs(r, c)
    return count

# BFS
def num_islands_bfs(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                queue = deque([(r, c)])
                grid[r][c] = "0"

                while queue:
                    x, y = queue.popleft()
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                            grid[nx][ny] = "0"
                            queue.append((nx, ny))

    return count

# Input
print("grid:")
raw_input = input().strip()
grid = ast.literal_eval(raw_input)

# Output
print("DFS Output:", num_islands_dfs([row[:] for row in grid]))
print("BFS Output:", num_islands_bfs([row[:] for row in grid]))
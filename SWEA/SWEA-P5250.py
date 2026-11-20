import heapq

def abs(x):
    if x < 0:
        x = -x
    return x

def coord(N, idx):
    return idx // N, idx % N

def _1d(N, row, col):
    return N * row + col

def cost(grid, start, end):
    n = len(grid)
    sr, sc = coord(n, start)
    er, ec = coord(n, end)

    if abs(sr - er) + abs(sc - ec) == 1:
        step_cost = grid[er][ec] - grid[sr][sc]
    else:
        raise ValueError
    return max(step_cost, 0) + 1

T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    grid = [list(map(int, input().split())) for _ in range(N)]

    g_size = N * N
    graph = []
    for i in range(g_size):
        graph.append([])
        irow, icol = coord(N, i)

        if irow > 0:
            graph[i].append((cost(grid, i, i - N), i - N))
        if irow < N - 1:
            graph[i].append((cost(grid, i, i + N), i + N))
        if icol > 0:
            graph[i].append((cost(grid, i, i - 1), i - 1))
        if icol < N - 1:
            graph[i].append((cost(grid, i, i + 1), i + 1))

    D = [float("inf")] * g_size
    P = [None] * g_size
    visited = [False] * g_size
    D[0] = 0
    heap = [(0, 0)]

    while heap:
        mincost, minidx = heapq.heappop(heap)
        if visited[minidx]:
            continue
        if minidx == g_size - 1:
            break
        visited[minidx] = True
        for weight, v in graph[minidx]:
            if not visited[v] and D[minidx] + weight < D[v]:
                D[v] = D[minidx] + weight
                P[v] = minidx
                heapq.heappush(heap, (D[v], v))

    print(f"#{test_case} {D[g_size - 1]}")

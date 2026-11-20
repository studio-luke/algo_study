import heapq

T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    grid = [list(map(int, input().split())) for _ in range(N)]

    dist = [[float('inf')] * N for _ in range(N)]
    visited = [[False] * N for _ in range(N)]
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    dist[0][0] = 0
    heap = [(0, 0, 0)]  # dist, row, col
    while heap:
        fuel, r, c = heapq.heappop(heap)

        if visited[r][c]:
            continue

        if r == N - 1 and c == N - 1:
            break

        visited[r][c] = True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            next_dist = fuel + max(grid[nr][nc] - grid[r][c], 0) + 1
            if not visited[nr][nc] and dist[nr][nc] > next_dist:
                dist[nr][nc] = next_dist
                heapq.heappush(heap, (next_dist, nr, nc))

    print(f"#{test_case} {dist[N-1][N-1]}")
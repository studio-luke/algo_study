T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    grid = [list(map(int, input().split())) for _ in range(N)]
    min_cost = [[float("inf")] * N for _ in range(N)]

    min_cost[0][0] = 0
    for i in range(1, N):
        min_cost[0][i] = (
                min_cost[0][i-1] +
                max(grid[0][i] - grid[0][i-1], 0)
                + 1
        )
        min_cost[i][0] = (
            min_cost[i-1][0] +
            max(grid[i][0] - grid[i-1][0], 0)
            + 1
        )

    for row in range(1, N):
        for col in range(1, N):
            min_cost[row][col] = (
                min(
                    min_cost[row-1][col]
                    + max(
                        grid[row][col]
                        - grid[row-1][col], 0),
                    min_cost[row][col-1]
                    + max(
                        grid[row][col]
                        - grid[row][col-1], 0)
                    )
                + 1
            )

    print(f"#{test_case} {min_cost[N-1][N-1]}")
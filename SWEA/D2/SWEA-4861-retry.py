T = int(input())

for test_case in range(1, T+1):
    N, M = map(int, input().split())

    grid = [input() for _ in range(N)]

    ans = ""
    for row in range(N):
        for col in range(N - M + 1):
            for i in range(M // 2):
                if grid[row][col + i] != grid[row][col + M - 1 - i]:
                    break
            else:
                ans = grid[row][col:col+M]
                break
        if ans:
            break
    if ans:
        print(f"#{test_case} {ans}")
        continue

    for col in range(N):
        for row in range(N - M + 1):
            for i in range(M // 2):
                if grid[row + i][col] != grid[row + M - 1 - i][col]:
                    break
            else:
                ans = "".join([grid[x][col] for x in range(row, row + M)])
        if ans:
            break

    print(f"#{test_case} {ans}")
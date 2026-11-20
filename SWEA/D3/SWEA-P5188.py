"""
동적계획법(Dynamic Programming)
백트랙킹(Backtracking)
"""

from itertools import combinations, permutations

T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    grid = [list(map(int, input().split())) for _ in range(N)]

    dp = [[0] * N for _ in range(N)]

    dp[0][0] = grid[0][0]
    for row in range(1, N):
        dp[row][0] = dp[row-1][0] + grid[row][0]

    for col in range(1, N):
        dp[0][col] = dp[0][col-1] + grid[0][col]

    for row in range(1, N):
        for col in range(1, N):
            dp[row][col] = min(dp[row-1][col], dp[row][col-1]) + grid[row][col]

    print(f'#{test_case} {dp[N-1][N-1]}')





    

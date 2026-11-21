f = {10: 1, 20: 3}


def how_many_cases(N):
    if N not in f:
        f[N] = (
            how_many_cases(N - 10) +
            2 * how_many_cases(N - 20)
        )
    return f[N]


T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    print(f"#{test_case} {how_many_cases(N)}")
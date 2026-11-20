"""
점화식 활용 가능.
from math import comb

comb(n-k, k)
"""

T = int(input())

def falling_factorial(N, a):
    """return N * (N-1) * ... * (N-a+1)"""
    if a == 0:
        return 1
    return N * falling_factorial(N-1, a-1)

for test_case in range(1, T+1):
    N = int(input())
    N = N // 10 # 0 빼고 생각하기

    tot_case = 0
    for n_squ in range(N//2 + 1):
        # number of cases to arrange n_squ squares
        case = falling_factorial(N - n_squ, n_squ) // falling_factorial(n_squ, n_squ)
        # Each width-20 block is one square or two horizontal rectangles.
        tot_case += (case * (2 ** n_squ))

    print(f"#{test_case} {tot_case}")




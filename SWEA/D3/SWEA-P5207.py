T = int(input())


def binary_search(L, l, r, x, direction=None):
    """return (left?, right?, found?)"""
    if l >= r:
        return (False, False)
    
    m = (l+r-1)//2
    zigzag = True
    if L[m] == x:
        return (zigzag, True)
    elif L[m] < x:
        if direction == "L":
            zigzag = False
        result = binary_search(L, m+1, r, x, "L")
        return (zigzag and result[0], result[1])
    else:
        if direction == "R":
            zigzag = False
        result = binary_search(L, l, m, x, "R")
        return (zigzag and result[0], result[1])
    

for test_case in range(1, T+1):
    NA, NB = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    A.sort()
    cnt = 0
    for v in B:
        result = binary_search(A, 0, NA, v)
        if result[0] and result[1]:
            cnt += 1
    print(f"#{test_case} {cnt}")


num_test = int(input())

for T in range(1, num_test+1):
    N, M = map(int, input().split())

    nlist = list(map(int, input().split()))

    max_sum = 0
    min_sum = float('inf')
    for i in range(N - M + 1):
        s = sum(nlist[i:i+M])
        if max_sum < s: max_sum = s
        if min_sum > s: min_sum = s

    print("#"+str(T), max_sum-min_sum)



from collections import deque

N_LIMIT = 1000000


def find_min_ops(N, M):
    if N == M:
        return 0

    dist = {M: 0}
    queue = deque([M])

    while queue:
        v = queue.popleft()

        cand = []
        if v < N_LIMIT:
            cand.append(v + 1)
        if v <= N_LIMIT - 10:
            cand.append(v + 10)
        if v > 1:
            cand.append(v - 1)
        if v % 2 == 0:
            cand.append(v // 2)

        for pm in cand:
            if pm == N:
                return dist[v] + 1
            if pm not in dist:
                dist[pm] = dist[v] + 1
                queue.append(pm)

    return -1


T = int(input())

for test_case in range(1, T+1):
    N, M = map(int, input().split())

    print(f"#{test_case} {find_min_ops(N, M)}")



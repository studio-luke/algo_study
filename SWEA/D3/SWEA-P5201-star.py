from collections import deque

T = int(input())

for test_case in range(1, T+1):
    N, M = map(int, input().split())
    weights = sorted((map(int, input().split())), reverse=True)
    trucks = sorted(map(int, input().split()), reverse=True)

    tot_weight = 0
    w_idx, t_idx = 0, 0

    while (w_idx <  N and t_idx < M):
        if weights[w_idx] > trucks[t_idx]:
            w_idx += 1
        else:
            tot_weight += weights[w_idx]
            w_idx += 1
            t_idx += 1

    print(f"#{test_case} {tot_weight}")    
        

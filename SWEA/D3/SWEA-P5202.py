T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    schedules = []
    for _ in range(N):
        s, e = map(int, input().split())
        schedules.append((s,e))
    
    schedules = sorted(schedules, key=lambda x: x[1])

    idx = 0
    last_end = 0
    tot_schedule = 0
    while idx < N:
        if last_end <= schedules[idx][0]:
            tot_schedule += 1
            last_end = schedules[idx][1]
        idx += 1
    print(f"#{test_case} {tot_schedule}")
    




def find_min_time(time_info, N):
    min_time = float('inf')

    visited = [False] * N
    def burn_candle(visited, cur_time,
                    remain_n,
                    remaining_burn_time):
        nonlocal min_time
        min_remain_time = cur_time + remaining_burn_time
        if min_time <= min_remain_time:
            return
        if remain_n == 0:
            min_time = min_remain_time
            return

        for candle in range(N):
            if visited[candle]:
                continue
            visited[candle] = True
            t_candle = time_info[candle][0]
            r_candle = time_info[candle][1]
            burn_candle(visited, cur_time + t_candle,
                        remain_n - 1,
                        max(remaining_burn_time - t_candle,
                            r_candle))
            
            visited[candle] = False
    burn_candle(visited, 0, N, 0)
    return min_time
        
N = int(input())
time_info = []
for _ in range(N):
    time_info.append(tuple(map(int, input().split())))

print(find_min_time(time_info, N))
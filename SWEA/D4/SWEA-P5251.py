import heapq

T = int(input())

for test_case in range(1, T+1):
    N, E = map(int, input().split())
    graph = [[] for _ in range(N+1)]
    for _ in range(E):
        start, end, weight = map(int, input().split())
        graph[start].append((weight, end))

    dist = [float('inf')] * (N+1)
    visited = [False] * (N+1)

    heap = [(0, 0)]  # cur_dist, start
    dist[0] = 0
    while heap:
        cur_dist, start = heapq.heappop(heap)

        if visited[start]:
            continue

        if start == N:
            break

        visited[start] = True
        for w, end in graph[start]:
            next_dist = cur_dist + w
            if not visited[end] and dist[end] > next_dist:
                dist[end] = next_dist
                heapq.heappush(heap, (next_dist, end))

    print(f'#{test_case} {dist[N]}')
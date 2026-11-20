T = int(input())

def traversal(cost_table, N, cur_pos, visited):
    min_cost = float('inf')
    if len(visited) == N - 1:
        return cost_table[cur_pos][0] # back to home
    for dest in range(1, N):
        if dest not in visited:
            visited.add(dest)
            cost = (
                cost_table[cur_pos][dest]
                + traversal(cost_table, N, dest, visited)
            )
            if min_cost > cost:
                min_cost = cost
            visited.remove(dest)
    return min_cost

for test_case in range(1, T+1):
    N = int(input())
    cost_table = [list(map(int, input().split())) for _ in range(N)]
    visited = set()
    print(f"#{test_case} {traversal(cost_table, N, 0, visited)}")


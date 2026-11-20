import heapq


class DisjointSet(object):
    def __init__(self, N):
        self.p = list(range(N+1))
        self.rank = [0] * (N+1)

    def find(self, x):
        if x != self.p[x]:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def __getitem__(self, item):
        return self.find(item)

    def union(self, x, y):
        px, py = self[x], self[y]
        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            self.p[px] = py
        else:
            self.p[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
        return True


T = int(input())

for test_case in range(1, T+1):
    V, E = map(int, input().split())
    DS = DisjointSet(V)
    heap = []

    for _ in range(E):
        start, end, weight = map(int, input().split())
        heap.append((weight, start, end))

    heapq.heapify(heap)

    tot_weight = 0
    selected_edges = 0
    while heap and selected_edges <= V:
        weight, start, end = heapq.heappop(heap)

        if DS.union(start, end):
            selected_edges += 1
            tot_weight += weight

    print(f"#{test_case} {tot_weight}")
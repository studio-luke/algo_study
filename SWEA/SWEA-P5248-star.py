class DisjointSet(object):
    def __init__(self, N):
        self.p = list(range(N+1))
        self.rank = [0] * (N+1)  # do not use 0 index

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        px, py = self[x], self[y]
        if px == py:
            return

        if self.rank[px] < self.rank[py]:
            self.p[px] = self.p[py]
        else:
            self.p[py] = self.p[px]
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1

    def __getitem__(self, item):
        return self.find(item)


T = int(input())

for test_case in range(1, T+1):
    N, M = map(int, input().split())

    G = DisjointSet(N)

    line_input = map(int, input().split())

    for s1, s2 in zip(line_input, line_input):
        G.union(s1, s2)

    roots = {G[i] for i in range(1, N+1)}

    print(f"#{test_case} {len(roots)}")

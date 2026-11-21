def tree_size(tree, root):
    size = 1  # counting root
    for i in range(len(tree[root])):
        size += tree_size(tree, tree[root][i])
    return size


T = int(input())

for test_case in range(1, T+1):
    E, N = map(int, input().split())
    edges = map(int, input().split())

    tree = {i: [] for i in range(1, E + 2)}
    for start, end in zip(edges, edges):
        tree[start].append(end)

    print(f"#{test_case} {tree_size(tree, N)}")




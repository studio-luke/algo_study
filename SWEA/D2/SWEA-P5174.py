"""
map object는 subscribable하지 않음
zip 사용법
python의 기본 최대 재귀 깊이는 1000이다.

import sys
sys.setrecursionlimit(1001)

while, stack 써서 다시 풀어보기
"""

T = int(input())

def count_nodes(tree, root):
    node_cnt = 1
    for child in tree[root]:
        node_cnt += count_nodes(tree, child)
    return node_cnt


for test_case in range(1, T+1):
    E, N = map(int, input().split())

    tree = [[] for _ in range(E+2)]
    
    e_input = iter(map(int, input().split()))
    
    for parent, child in zip(e_input, e_input):
        tree[parent].append(child)

    print(f"#{test_case} {count_nodes(tree, N)}")


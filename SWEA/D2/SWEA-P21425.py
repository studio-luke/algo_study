
num_test = int(input())

for _ in range(num_test):
    A, B, N = map(int, input().split())
    i = 0
    while (A <= N and B <= N):
        if A < B: A += B
        else: B += A
        i += 1
    print(i)


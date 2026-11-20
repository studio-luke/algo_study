test_num = int(input())

for T in range(1, test_num + 1):
    N = int(input())
    r_space = [[False] * 10 for _ in range(10)]
    b_space = [[False] * 10 for _ in range(10)]
    for _ in range(N):
        r1, c1, r2, c2, color = map(int, input().split())

        if color == 1: tar_space = r_space
        else: tar_space = b_space

        for i in range(r1, r2+1):
            for j in range(c1, c2+1):
                tar_space[i][j] = True

    pur = 0
    for i in range(10):
        for j in range(10):
            if r_space[i][j] and b_space[i][j]:
                pur += 1
    print("#"+str(T), pur)

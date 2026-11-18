def quick_sort(values, start, end):
    if end - start <= 1:
        return
    pivot = values[start]
    i = start + 1
    j = end - 1

    while i <= j:
        while i < end and values[i] <= pivot:
            i += 1
        while values[j] > pivot:
            j -= 1
        if i < j:
            values[i], values[j] = values[j], values[i]
    values[start], values[j] = values[j], values[start]

    quick_sort(values, start, j)
    quick_sort(values, i, end)


T = int(input())

for test_case in range(1, T+1):
    N = int(input())
    values = list(map(int, input().split()))
    quick_sort(values, 0, N)
    print(f"#{test_case} {values[N//2]}")

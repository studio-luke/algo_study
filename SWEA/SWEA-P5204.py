T = int(input())

def merge_sort(nlist, s, e):
    count = 0
    if e - s <= 1:
        return 0
    mid = (s+e) // 2

    count += merge_sort(nlist, s, mid)
    count += merge_sort(nlist, mid,e)

    
    if nlist[mid-1] > nlist[e-1]:
        count += 1

    left = s
    right = mid
    merged = []
    
    while left < mid and right < e:
        if nlist[left] <= nlist[right]:
            merged.append(nlist[left])
            left += 1
        else:
            merged.append(nlist[right])
            right += 1

    while left < mid:
        merged.append(nlist[left])
        left += 1

    while right < e:
        merged.append(nlist[right])
        right += 1

    nlist[s:e] = merged
    return count


for test_case in range(1, T+1):
    N = int(input())
    nlist = list(map(int, input().split()))
    case = merge_sort(nlist, 0, N)
    print(f"#{test_case} {nlist[N//2]} {case}")



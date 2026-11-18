

"""Find the index of max(A)"""
def _find_max_idx(A, n = None):
    if n is None:
        n = len(A)
    if n == 1:
        return 0
    
    i = _find_max_idx(A, n-1)
    if A[i] > A[n-1]:
        return i
    else:
        return n-1



"""Sort A[0:n] with Selection Sort and return A"""
def selection_sort(A, n = None):
    if n is None:
        n = len(A)

    if n > len(A):
        raise ValueError("n must be 0<= n <=len(A)")

    if n > 1:
        i = _find_max_idx(A, n)
        A[i], A[n-1] = A[n-1], A[i]
        return selection_sort(A, n-1)

    return A

"""Insert A[n-1] in ordered list A[:n-1] in order"""
def _insert_in_order(A, n = None):
    if n is None:
        n = len(A)
    if n <= 1 or n > len(A):
        return
    if A[n-2] > A[n-1]:
        A[n-2], A[n-1] = A[n-1], A[n-2]
    _insert_in_order(A, n-1)

"""Sort A[0:n] with Insertion Sort and return A"""
def insertion_sort(A, n = None):
    if n is None:
        n = len(A)
    
    if n < 0 or n > len(A):
        raise ValueError("n must be 0 <= n <= len(A)")
    
    if n <= 1: return A


    _insert_in_order(A, len(A) - n + 2)
    return insertion_sort(A, n-1)


"""Bubble-swap A[:n]"""
def _bubble_row(A, n = None):
    if n is None:
        n = len(A)
    if n <= 1: return
    if A[n-2] > A[n-1]:
        A[n-2], A[n-1] = A[n-1], A[n-2]
    _bubble_row(A, n-1)

    
"""Sort A[0:n] with Bubble Sort and return A"""
def bubble_sort(A, n = None):
    if n is None:
        n = len(A)

    if not 0 <= n <= len(A):
        raise ValueError("n must be 0 <= n <= len(A)")

    if n <= 1: return A

    _bubble_row(A, n)
    return bubble_sort(A, n - 1)

"""Find x in sorted array A[a:b]"""
def binary_search(A, x, a=0, b=None):
    if b is None: b = len(A)
    if a >= b: return False
    mid = (a+b)//2
    if x > A[mid]:
        return binary_search(A, x, mid+1, b)
    elif x < A[mid]:
        return binary_search(A, x, a, mid)
    else: return True



def merge_sort(nlist, s=0, e=None):
    if e is None:
        e = len(nlist)
    if e - s <= 1:
        return
    mid = (s+e) // 2

    merge_sort(nlist, s, mid)
    merge_sort(nlist, mid,e)

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

def quick_sort(values, start=0, end=None):
    if end is None:
        end = len(values)
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
"""
Python의 dict comprehension 문법
dict의 in 연산자의 평균 소요 시간은 O(1)이다.
"""

T = int(input())

for test_case in range(1, T+1):
    str1 = input()
    str2 = input()

    freq = {char:0 for char in str1}

    for char in str2:
        if char in freq:
            freq[char] += 1
        
    print(f"#{test_case} {max(freq.values())}")

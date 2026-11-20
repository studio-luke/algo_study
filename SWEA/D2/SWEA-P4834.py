T = int(input())


for test_case in range(1, T + 1):
    N = int(input())
    freq = [0] * 10
    nums = input()
    for digit in nums:
        freq[int(digit)] += 1

    best_digit = 0
    for digit in range(1, 10):
        if freq[digit] >= freq[best_digit]:
            best_digit = digit

    print("#"+str(test_case), best_digit, freq[best_digit])
    

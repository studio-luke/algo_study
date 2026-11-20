"""
const 변수는 테스트 for 문 바깥에서 선언하기
"""

T = int(input())

pair = {
    ']': '[',
    '}': '{',
    ')': '('
}
open_parentheses = pair.values()

for test_case in range(1, T+1):
    line = input()
    stack = []

    valid = 1
    for char in line:
        if char in open_parentheses:
            stack.append(char)
        elif char in pair:
            if stack and stack[-1] == pair[char]:
                stack.pop()
            else:
                valid = 0
                break

    if stack:
        valid = 0

    print(f"#{test_case} {valid}")

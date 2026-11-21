"""
- 이어 들어오는 input을 무시하고 조기 종료해버리면 에러가 발생한다
- str->list 는 list(str) 하면 되지만 list->str는 ''.join(list)로 하기!
- list와 str의 len() 시간복잡도는 O(1)이다
- 변수명: row, col, start, offset, candidate 등
- 반복되는 부분 함수화하기

"""

T = int(input())


def is_palindrome(line):
    """return True if line is palindrome"""
    for offset in range(len(line)//2):
        if line[offset] != line[-1-offset]:
            return False
    return True

def find_palindrome(line, length):
    for start in range(len(line) - length + 1):
        candidate = line[start:start+length]
        if is_palindrome(candidate):
            return candidate
    return ''


for test_case in range(1, T+1):
    N, M = map(int, input().split())

    grid = [input() for _ in range(N)]
    answer = ''

    # Read horizontally
    for line in grid:
        answer = find_palindrome(line, M)
        if answer:
            break
    
    if not answer:
        # Read vertically
        for col in range(N):
            line = ''.join([grid[row][col] for row in range(N)])
            answer = find_palindrome(line, M)
            if answer:
                break

    print(f"#{test_case} {answer}")

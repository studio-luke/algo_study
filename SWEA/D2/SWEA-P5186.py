
T = int(input())
NUM_MAX = 12
float_len = 0
float_list = ""

for _ in range(T):
    N = float(input())
    exp = -1
    for _ in range(NUM_MAX):
        cur = 2**exp
        print("cur, N:", cur, N)
        if N == cur:
            N -= cur
            float_list += "1"
            print(float_list)
            break
        elif N > cur: 
            N -= cur
            float_list += "1"
        else: float_list += "0"
        
        exp -= 1
    if N > 0:
        print("overflow")
        

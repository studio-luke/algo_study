num_test = int(input())



def binary_search(x, a, b, turn=0):
    if a >= b: return turn
    mid = int((a + b) / 2)
    if x == mid: return turn
    elif x < mid: return binary_search(x, a, mid, turn + 1)
    else: return binary_search(x, mid, b, turn + 1)


for T in range(1, num_test + 1):
    P, Pa, Pb = map(int, input().split())
    A_turn = binary_search(Pa, 1, P)
    B_turn = binary_search(Pb, 1, P)

    if A_turn < B_turn: print("#"+str(T), "A")
    elif A_turn > B_turn: print("#"+str(T), "B")
    else: print("#"+str(T), "0")


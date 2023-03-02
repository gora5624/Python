input()
ai = input().strip('\n').strip().split(' ')
ai = [int(x) for x in ai]
def test(ai):
    maxA = max(ai)
    for i in range(len(ai)-1):
        if ai[i] > ai[i+1]:
            print(-1)
            return
        continue
    print(str(max(ai) - min(ai)))
test(ai)
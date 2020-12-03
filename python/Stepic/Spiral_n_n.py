n = int(input())
mass = []
for j in range(n):
    Str = []
    for i in range(n):
        Str.append(0)
    mass.append(Str)
x, y = 0, 0
dx, dy = 1, 0
for N in range(1, n**2+1):
    mass[x][y] = N
    new_x, new_y = x+dx, y+dy
    if 0 <= new_x < n and 0 <= new_y < n and mass[new_x][new_y] == 0:
        x, y = new_x, new_y
    else:
        dx, dy = -dy, dx
        x, y = x+dx, y+dy
for x in list(zip(*mass)):
    print(*x)

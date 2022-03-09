def f(x):
    return x**2


n = int(input())
c = 0
data = {}
input_list = []
while c < n:
    c += 1
    tmp = int(input())
    input_list.append(tmp)
    if tmp not in data:
        data.update({tmp: f(tmp)})
for tmp in input_list:
    print(data[tmp])

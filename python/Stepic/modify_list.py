l = [1, 9, 3, 15, 5, 6, 6, 2, 10]


def modify_list(l):
    tmp = []
    for i in l:
        if i % 2 == 1:
            tmp.append(i)
    for i in tmp:
        l.remove(i)
    for n, i in enumerate(l):
        l[n] = i//2


modify_list(l)


print(l)

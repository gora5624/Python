d = {}
key = 1
value = -1


def update_dictionary(d, key, value):

    if key in d.keys():
        d[key].append(value)
    elif key*2 in d.keys():
        d[key*2].append(value)
    else:
        d[key*2] = []
        d.update({key*2: [value]})


update_dictionary(d, key, value)

key = 2
value = -2
update_dictionary(d, key, value)
key = 1
value = -3
update_dictionary(d, key, value)
print(d)

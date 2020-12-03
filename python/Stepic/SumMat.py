my_mas = []
my_str = []
while True:
    input_str = input()
    if input_str == 'end':
        break
    input_str_new = input_str.split(' ')
    for let in input_str_new:
        my_str.append(int(let))
    my_mas.append(my_str)
    my_str = []
new_mas = []
new_str = []
for j, Str in enumerate(my_mas):
    for i, num in enumerate(Str):
        if i+1 == len(Str) and j+1 < len(my_mas):
            num_new = my_mas[j][0]+my_mas[j][i-1]+my_mas[j+1][i]+my_mas[j-1][i]
        elif i+1 < len(Str) and j+1 == len(my_mas):
            num_new = my_mas[j][i+1]+my_mas[j][i-1]+my_mas[0][i]+my_mas[j-1][i]
        elif i+1 == len(Str) and j+1 == len(my_mas):
            num_new = my_mas[j][0]+my_mas[j][i-1]+my_mas[0][i]+my_mas[j-1][i]
        elif i+1 < len(Str) and j+1 < len(my_mas):
            num_new = my_mas[j][i+1]+my_mas[j][i-1] + \
                my_mas[j+1][i]+my_mas[j-1][i]
        new_str.append(str(num_new))
    print(' '.join(new_str))
    new_str = []

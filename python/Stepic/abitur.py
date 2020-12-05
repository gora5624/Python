data = []
with open(r'C:\Users\user\Downloads\dataset_3363_4.txt', 'r') as file:
    data.extend(file.read().split('\n'))

data_new = []
for n, line in enumerate(data):
    if line != '':
        data_new.append(line.split(';'))
        num = (int(data_new[n][1])+int(data_new[n][2])+int(data_new[n][3]))/3
        with open(r'C:\Users\user\Downloads\file.txt', 'a') as file:
            file.writelines(str(num)+'\n')
count_1 = 0
count_2 = 0
count_3 = 0
for line in data_new:
    count_1 += int(line[1])
    count_2 += int(line[2])
    count_3 += int(line[3])
count_1 = str(count_1/len(data_new))
count_2 = str(count_2/len(data_new))
count_3 = str(count_3/len(data_new))
with open(r'C:\Users\user\Downloads\file.txt', 'a') as file:
    Str = count_1 + ' ' + count_2 + ' ' + count_3
    file.write(Str)

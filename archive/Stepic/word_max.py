with open(r'C:\Users\user\Downloads\dataset_3363_3.txt', 'r') as file:
    data = []

    for line in file:
        data.extend(line.lower().strip().split(' '))
print(data)
dict_data = {}
Max = 0
Max_word = 'zzz'
for word in data:
    if data.count(word) > Max:
        Max = data.count(word)
        Max_word = word
    elif data.count(word) == Max and word < Max_word:
        Max = data.count(word)
        Max_word = word
with open(r'C:\Users\user\Downloads\file.txt', 'a') as file:
    info = Max_word+' '+str(Max)
    file.write(info)

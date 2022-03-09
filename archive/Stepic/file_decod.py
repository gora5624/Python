with open(r'C:\Users\user\Downloads\dataset_3363_2.txt', 'r') as file:
    data = ''
    for line in file:
        data += line.strip()
for n, let in enumerate(data):
    if let.isalpha():
        count = 1
        num = ''
        while data[n+count].isdigit():
            num += data[n+count]
            count += 1
            if n+count > len(data)-1:
                break
        for _ in range(int(num)):
            with open(r'C:\Users\user\Downloads\file.txt', 'a') as file:
                file.write(let)

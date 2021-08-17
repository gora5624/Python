words = input()

List_Words = words.lower().split(' ')
Tmp_List = []
for word in List_Words:
    if word not in Tmp_List:
        Count = List_Words.count(word)
        Tmp_List.append(word)
        print(word, ' ', Count)

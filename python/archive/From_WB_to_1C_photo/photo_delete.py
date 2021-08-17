import os

list_file = os.listdir(r'D:\доделать\new')
for file in list_file:
    list_name = os.listdir(os.path.join(r'D:\доделать\new', file))
    for name in list_name:
        if len(name) > 6:
            os.remove(os.path.join(r'D:\доделать\new', file, name))

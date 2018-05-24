names = ["sarada", "adi", "ushe", "nagesh"]
print(names)
print('-'*50)
for name in names:
    if len(name) > 5 and ('n' in name or 'N' in name):
        print(name)

while(len(names) != 0):
    names.pop()

print(names)
print('-'*50)
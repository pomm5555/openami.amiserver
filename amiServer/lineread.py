
file = open(r'data.txt')
f = file.readlines()

i = 0
for elem in f:
    i+=1
    if i == 1:
        print elem.split("\n")[0]+",",
    else:
        i=0
        print elem,


file.close()
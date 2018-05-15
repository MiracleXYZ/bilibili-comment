import re

f = open("vsinger.txt", "r", encoding='UTF-8')
f2 = open("vsinger_2.txt", "w", encoding='UTF-8')
count = 0
dr = re.compile(r'<[^>]+>',re.S)
while 1:
    line = f.readline()
    if not line:
        break
    pass
    dd = dr.sub('',line)
    count = count + 1
    f2.writelines(dd)
print(count)

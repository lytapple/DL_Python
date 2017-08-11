f = open('123.txt', 'rw')
newf = open('1234.txt', 'w')
for line in f:
    line = line + '\n'
    newf.write(line)
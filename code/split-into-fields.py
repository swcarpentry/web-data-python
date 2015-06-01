reader = open('test01.csv', 'r')
for line in reader:
    fields = line.split(',')
    print(fields)
reader.close()

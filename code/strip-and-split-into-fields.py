reader = open('test01.csv', 'r')
for line in reader:
    fields = line.strip().split(',')
    print(fields)
reader.close()

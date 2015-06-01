reader = open('test01.csv', 'r')
for line in reader:
    print(len(line))
reader.close()

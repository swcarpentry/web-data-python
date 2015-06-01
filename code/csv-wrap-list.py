import csv

raw = open('test01.csv', 'r')
lines = raw.readlines()
raw.close()
cooked = csv.reader(lines)
for record in cooked:
    print(record)

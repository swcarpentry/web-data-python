import csv

raw = open('test01.csv', 'r')
cooked = csv.reader(raw)
for record in cooked:
    print(record)
raw.close()

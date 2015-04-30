import os
import csv

data = u'first\nsecond\nthird\n'
wrapper = csv.reader(data.strip().split(os.linesep))

for record in wrapper:
    print(record)

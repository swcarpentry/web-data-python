import os
import csv

data = '1901,12.3\n1902,45.6\n1903,78.9\n'
wrapper = csv.reader(data.strip().split(os.linesep))

for record in wrapper:
    print(record)

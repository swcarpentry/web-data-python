import io
import csv

data = u'1901,12.3\n1902,45.6\n1903,78.9\n'
reader = io.StringIO(data)
wrapper = csv.reader(reader)
for record in wrapper:
    print(record)

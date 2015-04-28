import io
import csv

data = u'first\nsecond\nthird\n'
reader = io.StringIO(data)
wrapper = csv.reader(reader)
for record in wrapper:
    print(record)

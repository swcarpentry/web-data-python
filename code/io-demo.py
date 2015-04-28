import io

data = 'first\nsecond\nthird\n'
reader = io.StringIO(data)
for line in reader:
    print line

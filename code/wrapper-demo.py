import os

data = 'first\nsecond\nthird\n'

reader = data.strip().split(os.linesep)

for line in reader:
    print(line)

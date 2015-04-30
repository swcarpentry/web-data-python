---
layout: page
title: Working With Data on the Web
subtitle: Handling CSV Data
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Explain what CSV is, and read CSV data sets.

Our little program gets the data we want,
but returns it as one long character string rather than as a list of numbers.
There are two ways we could convert the former to the latter:

*   Write a function to split that string on newline characters to create lines,
    then split the lines on commas and convert the second part of each to a number.
*   Use a couple of Python libraries to do this for us.

Most experienced programmers would say that the second approach is easier,
but "easy" is relative:
using standard libraries is only more effective in practice if we know those libraries exist,
and know enough about them to think about our problem in terms of what they can do.

Let's give both methods a try.
Here's a small program to test the first approach:

~~~ {.python}
input_data = '''1901,12.3
1902,45.6
1903,78.9'''

as_lines = input_data.split('\n')
print('input data as lines:')
print(as_lines)

for line in as_lines:
    fields = line.split(',') # turn '1901,12.3' into ['1901', '12.3']
    year = int(fields[0])    # turn the text '1901' into the integer 1901
    value = float(fields[1]) # turn the text '12.3' into the number 12.3
    print(year, ':', value)
~~~
~~~ {.output}
input data as lines:
['1901,12.3', '1902,45.6', '1903,78.9']
1901 : 12.3
1902 : 45.6
1903 : 78.9
~~~

We start by defining a string in our program to use as input data so that we can easily check the correctness of our output.
The first three lines of code turn this one multi-line string into a list of strings
by splitting on the newline characters (which are written `\n` in our program).
The `for` loop then extracts the year and value from each line
by splitting the line on the comma and converting the digits to numbers.

> ## Escape Sequences {.callout}
>
> Programmers need a way to put quotes, double quotes, and other special characters in strings.
To do this, they use [escape sequences](reference.html#escape-sequence):
> `\'` for a single quote, `\"` for a double quote, `\n` for a newline, and so on.

Now let's have a look at how we could parse the data using standard Python libraries.  The library we'll use is called `csv`.
It doesn't read data itself:
instead, it takes the lines read by something else and turns them into lists of values by splitting on commas. We will also need to split the string on line separators before `csv` can read it:

~~~ {.python}
import csv
import os

data = '''first,FIRST
second,SECOND
third,THIRD'''
wrapper = csv.reader(data.strip().split(os.linesep))
for record in wrapper:
    print(record)
~~~
~~~ {.output}
['first', 'FIRST']
['second', 'SECOND']
['third', 'THIRD']
~~~

Putting it all together, we can get data for Canada like this:

~~~ {.python}
import requests
import os
import csv
url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split(os.linesep))
    for record in wrapper:
        year = int(record[0])
        value = float(record[1])
        print(year, ':', value)
~~~
~~~ {.error}
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-6-da21db395042> in <module>()
      7     wrapper = csv.reader(reader)
      8     for record in wrapper:
----> 9         year = int(record[0])
     10         value = float(record[1])
     11         print year, ':', value

ValueError: invalid literal for int() with base 10: 'year'
~~~

That error occurs because the first line of data is:

~~~
year,data
~~~

When we try to convert the string `'year'` to an integer,
Python quite rightly complains.
The fix is straightforward:
we just need to ignore lines that start with the word `year`.
And while we're at it,
we'll put our results into a list instead of just printing them:

~~~ {.python}
import requests
import os
import csv

url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split(os.linesep))
    results = []
    for record in wrapper:
        if record[0] != 'year':
            year = int(record[0])
            value = float(record[1])
            results.append([year, value])
    print('first five results')
    print(results[:5])
~~~
~~~ {.output}
first five results
[[1901, -7.67241907119751], [1902, -7.862711429595947], [1903, -7.910782814025879], [1904, -8.155729293823242], [1905, -7.547311305999756]]
~~~


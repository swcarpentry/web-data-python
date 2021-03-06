---
title: "Handling CSV Data"
teaching: 15
exercises: 0
questions:
- "FIXME"
objectives:
- "Parse CSV data using the `csv` library."
- "Test a program that parses CSV using multiline strings."
keypoints:
- "FIXME"
---

Our little program gets the data we want,
but returns it as one long character string rather than as a list of numbers.
There are two ways we could convert the former to the latter:

*   Write a function to split that string on newline characters to create lines,
    then split the lines on commas and convert the second part of each to a number.
*   Use a python library to do this for us.

Most experienced programmers would say that the second approach is easier,
but "easy" is relative:
using standard libraries is only easier if we know that those libraries exist and how to use them.

Let's try the first approach.
To begin,
we create a file called `test01.csv` that contains the following three lines:

~~~
1901,12.3
1902,45.6
1903,78.9
~~~
{: .source}

It's easy to read this file line by line and (for example) report the length of each line:

~~~
with open('test01.csv', 'r') as reader:
    for line in reader:
        print(len(line))
~~~
{: .python}
~~~
10
10
10
~~~
{: .output}

We can also split each line on commas to turn each one into a list of string fragments:

~~~
with open('test01.csv', 'r') as reader:
    for line in reader:
        fields = line.split(',')
        print(fields)
~~~
{: .python}
~~~
['1901', '12.3\n']
['1902', '45.6\n']
['1903', '78.9\n']
~~~
{: .output}

The dates are correct,
but the values all end with `\n`.
This is an [escape sequence]({{ site.github.url }}/reference/#escape-sequence) that represents
the newline character at the end of each line.
To get rid of it,
we should strip leading and trailing whitespace from each line before splitting it on commas:

~~~
with open('test01.csv', 'r') as reader:
    for line in reader:
        fields = line.strip().split(',')
        print(fields)
~~~
{: .python}
~~~
['1901', '12.3']
['1902', '45.6']
['1903', '78.9']
~~~
{: .output}

Now let's have a look at how we could parse the data using standard Python libraries instead.
The library we'll use is called `csv`.
It doesn't read data itself:
instead, it takes the lines read by something else and turns them into lists of values by splitting on commas.
Here's one way to use it:

~~~
import csv

with open('test01.csv', 'r') as raw:
    cooked = csv.reader(raw)
    for record in cooked:
        print(record)
~~~
{: .python}
~~~
['1901', '12.3']
['1902', '45.6']
['1903', '78.9']
~~~
{: .output}

Here,
`raw` reads data in the normal way,
while `cooked` is a [wrapper]({{ site.github.url }}/reference#wrapper)
that takes a line of text and turns it into a list of fields.

We can equally well give a `csv.reader` a list of strings rather than a file:

~~~
import csv

with open('test01.csv', 'r') as raw:
    lines = raw.readlines()
cooked = csv.reader(lines)
for record in cooked:
    print(record)
~~~
{: .python}
~~~
['1901', '12.3']
['1902', '45.6']
['1903', '78.9']
~~~
{: .output}

Using the `csv` library doesn't seem any simpler than just splitting strings,
but look at what happens when we have data like this:

~~~
"Meltzer, Marlyn Wescoff",1922,2008
"Spence, Frances Bilas",1922,2012
"Teitelbaum,Ruth Lichterman",1924,1986
~~~
{: .source}

With simple string splitting, our output is:

~~~
['"Meltzer', ' Marlyn Wescoff"', '1922', '2008']
['"Spence', ' Frances Bilas"', '1922', '2012']
['"Teitelbaum', 'Ruth Lichterman"', '1924', '1986']
~~~
{: .output}

The double quotes are still there,
and the field containing each person's name has been split into pieces.
If we use the `csv` library,
on the other hand,
the output is:

~~~
['Meltzer, Marlyn Wescoff', '1922', '2008']
['Spence, Frances Bilas', '1922', '2012']
['Teitelbaum,Ruth Lichterman', '1924', '1986']
~~~
{: .output}

because the library understands how to handle text fields containing commas
(and a lot more).

We need to do one more thing before using `csv` with the climate data.
When we use the World Bank's API to get data for a particular country,
it comes back as one long string:

~~~
year,data
1901,-7.67241907119751
1902,-7.862711429595947
1903,-7.910782814025879
⋮   ⋮   ⋮
~~~
{: .source}

We have to break this into lines before giving it to `csv.reader`,
and we can do that by splitting the string on the same `\n` escape sequence
we encountered a few moments ago.
To see how this works,
let's read `test01.csv` into memory and split it into pieces:

~~~
with open('test01.csv', 'r') as reader:
    data = reader.read()
    lines = data.split('\n')
    print(lines)
~~~
{: .python}
~~~
['1901,12.3', '1902,45.6', '1903,78.9', '']
~~~
{: .output}

That's *almost* right, but why is there an empty string at the end of the list?
The answer is that the last line of the file ends in a newline,
so Python does the same thing it does in the example below:

~~~
fields = 'a-b-'.split('-')
print(fields)
~~~
{: .python}
~~~
['a', 'b', '']
~~~
{: .output}

The solution once again is to strip leading and trailing whitespace before splitting:

~~~
with open('test01.csv', 'r') as reader:
    data = reader.read()
    lines = data.strip().split('\n')
    print(lines)
~~~
{: .python}
~~~
['1901,12.3', '1902,45.6', '1903,78.9']
~~~
{: .output}

Putting this all together, we can get data for Canada like this:

~~~
import requests
import csv

url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    for record in wrapper:
        print(record)
~~~
{: .python}
~~~
['year', 'data']
['1901', '-7.67241907119751']
['1902', '-7.862711429595947']
['1903', '-7.910782814025879']
['1904', '-8.155729293823242']
['1905', '-7.547311305999756']
⋮   ⋮   ⋮
~~~
{: .output}

That looks like progress,
so let's convert the data from strings to the numbers we actually want:

~~~
import requests
import csv

url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    for record in wrapper:
        year = int(record[0])
        value = float(record[1])
        print(year, value)
~~~
{: .python}
~~~
Traceback (most recent call last):
  File "api-with-naive-converting.py", line 11, in <module>
    year = int(record[0])
ValueError: invalid literal for int() with base 10: 'year'
~~~
{: .error}

The error occurs because the first line of data is:

~~~
year,data
~~~
{: .source}

When we try to convert the string `'year'` to an integer,
Python quite rightly complains.
The fix is straightforward:
we just need to ignore lines that start with the word `year`:

~~~
import requests
import csv

url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    results = []
    for record in wrapper:
        if record[0] != 'year':
            year = int(record[0])
            value = float(record[1])
            print(year, value)
~~~
{: .python}
~~~
1901 -7.67241907119751
1902 -7.862711429595947
1903 -7.910782814025879
1904 -8.155729293823242
1905 -7.547311305999756
...
~~~
{: .output}

> ## The Makeup of CSV Files
>
> CSV Files need to be separated into:
>
> 1.  Records (fields) then rows(lines).
> 2.  Rows(lines) then records (fields).
> 3.  Newline characters.
> 4.  Commas and other characters.
{: .challenge}

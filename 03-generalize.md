---
layout: page
title: Working With Data on the Web
subtitle: Generalizing and Handling Errors
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Turn a script into a function.
> *   Make a function more robust by explicitly handling errors.

Now that we know how to get the data for Canada,
let's create a function that will do the same thing for an arbitrary country.
The steps are simple:

1.  copy the code we've written into a function that takes a 3-letter country code as a parameter,
2.  insert that country code into the URL at the appropriate place, and
3.  return the result as a list instead of printing it.

The resulting function looks like:

~~~ {.python}
def annual_mean_temp(country):
    '''Get the annual mean temperature for a country given its 3-letter ISO code (such as "CAN").'''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/' + country + '.csv'
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
                results.append([year, value])
        return results
~~~

This works:

~~~ {.python}
canada = annual_mean_temp('CAN')
print('first three entries for Canada:', canada[:3])
~~~
~~~ {.output}
first three entries for Canada: [[1901, -7.67241907119751], [1902, -7.862711429595947], [1903, -7.910782814025879]]
~~~

However,
there's a problem.
Look what happens when we pass in an invalid country identifier:

~~~ {.python}
latveria = annual_mean_temp('LTV')
print 'first three entries for Latveria:', latveria[:3]
~~~
~~~ {.output}
first three entries for Latveria: []
~~~

Latveria doesn't exist,
so why is our function returning an empty list rather than printing an error message?
The non-appearance of an error message must mean that the response code was 200;
if it was anything else,
we would have gone into the `if` branch,
printed a message,
and returned `None`
(which is what functions do when they're not told to return anything specific).

So if the response code was 200 and there was no data, that would explain what we're seeing.
Let's check:

~~~ {.python}
def annual_mean_temp(country):
    '''Get the annual mean temperature for a country given its 3-letter ISO code (such as "CAN").'''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/' + country + '.csv'
    print('url used is', url)
    response = requests.get(url)
    print('response code:', response.status_code)
    print('length of data:', len(response.text))
    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
    else:
        wrapper = csv.reader(response.text.strip().split('\n'))
        results = []
        for record in wrapper:
            if record[0] != 'year':
                year = int(record[0])
                value = float(record[1])
                results.append([year, value])
        return results

latveria = annual_mean_temp('LTV')
print('number of records for Latveria:', len(latveria))
~~~
~~~ {.output}
url used is http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/LTV.csv
response code: 200
length of data: 0
number of records for Latveria: 0
~~~

In other words,
the World Bank is always saying,
"I was able to answer your query,"
even when it actually can't.
After a bit more experimenting, we discover that the site *always* returns a 200 status code.
The only way to tell if there's real data or not is to check if `response.text` is empty.
Here's the updated function:

~~~ {.python}
def annual_mean_temp(country):
    '''
    Get the annual mean temperature for a country given its 3-letter ISO code (such as "CAN").
    Returns an empty list if the country code is invalid.
    '''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/' + country + '.csv'
    response = requests.get(url)
    results = []
    if len(response.text) > 0:
        wrapper = csv.reader(response.text.strip().split('\n'))
        for record in wrapper:
            if record[0] != 'year':
                year = int(record[0])
                value = float(record[1])
                results.append([year, value])
    return results

print('number of records for Canada:', len(annual_mean_temp('CAN')))
print('number of records for Latveria:', len(annual_mean_temp('LTV')))
~~~
~~~ {.output}
number of records for Canada: 109
number of records for Latveria: 0
~~~

Now that we can get surface temperatures for different countries,
we can write a function to compare those values.
(We'll jump straight into writing a function because by now it's clear that's what we're eventually going to do anyway.)
Here's our first attempt:

~~~ {.python}
def diff_records(left, right):
    '''Given lists of [year, value] pairs, return list of [year, difference] pairs.'''
    num_years = len(left)
    results = []
    for i in range(num_years):
        left_year, left_value = left[i]
        right_year, right_value = right[i]
        difference = left_value - right_value
        results.append([left_year, difference])
    return results
~~~

Here, we're using the number of entries in `left` (which we find with `len(left)`) to control our loop.
The expression:

~~~ {.python}
for i in range(num_years):
~~~

runs `i` from 0 to `num_years-1`, which corresponds exactly to the legal indices of `left`.
Inside the loop we unpack the left and right years and values from the list entries,
then append a pair containing a year and a difference to `results`,
which we return at the end.

To see if this function works, we can run a couple of tests on made-up data:

~~~ {.python}
print('one record:', diff_records([[1900, 1.0]],
                                  [[1900, 2.0]]))
print('two records:', diff_records([[1900, 1.0], [1901, 10.0]],
                                   [[1900, 2.0], [1901, 20.0]]))
~~~
~~~ {.output}
one record: [[1900, -1.0]]
two records: [[1900, -1.0], [1901, -10.0]]
~~~

That looks pretty good—but what about these cases?

~~~ {.python}
print('mis-matched years:', diff_records([[1900, 1.0]],
                                         [[1999, 2.0]]))
print('left is shorter', diff_records([[1900, 1.0]],
                                      [[1900, 10.0], [1901, 20.0]]))
print('right is shorter', diff_records([[1900, 1.0], [1901, 2.0]],
                                       [[1900, 10.0]]))
~~~
~~~ {.error}
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-15-7582f56db8bf> in <module>()
      4                                       [[1900, 10.0], [1901, 20.0]])
      5 print('right is shorter', diff_records([[1900, 1.0], [1901, 2.0]],
----> 6                                        [[1900, 10.0]]))

<ipython-input-13-67464343fd99> in diff_records(left, right)
      5     for i in range(num_years):
      6         left_year, left_value = left[i]
----> 7         right_year, right_value = right[i]
      8         difference = left_value - right_value
      9         results.append([left_year, difference])

IndexError: list index out of rangemis-matched years: [[1900, -1.0]]
left is shorter [[1900, -9.0]]
right is shorter
~~~

The first test gives us an answer even though the years didn't match:
we get a result, but it's meaningless.
The second case gives us a partial result,
again without telling us there's a problem,
while the third crashes because we're using `left` to determine the number of records,
but `right` doesn't have that many.

The first two problems are actually worse than the third
because they are [silent failures](reference.html#silent-failure):
the function does the wrong thing, but doesn't indicate that in any way.
Let's fix that:

~~~ {.python}
def diff_records(left, right):
    '''
    Given lists of [year, value] pairs, return list of [year, difference] pairs.
    Fails if the inputs are not for exactly corresponding years.
    '''
    assert len(left) == len(right), \
           'Inputs have different lengths.'
    num_years = len(left)
    results = []
    for i in range(num_years):
        left_year, left_value = left[i]
        right_year, right_value = right[i]
        assert left_year == right_year, \
               'Record {0} is for different years: {1} vs {2}'.format(i, left_year, right_year)
        difference = left_value - right_value
        results.append([left_year, difference])
    return results
~~~

Do our "good" tests pass?

~~~ {.python}
print('one record:', diff_records([[1900, 1.0]],
                                  [[1900, 2.0]]))
print('two records:', diff_records([[1900, 1.0], [1901, 10.0]],
                                   [[1900, 2.0], [1901, 20.0]]))
~~~
~~~ {.output}
one record: [[1900, -1.0]]
two records: [[1900, -1.0], [1901, -10.0]]
~~~

What about our the three tests that we now expect to fail?

~~~ {.python}
print('mis-matched years:', diff_records([[1900, 1.0]],
                                         [[1999, 2.0]]))
~~~
~~~ {.error}
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-18-c101917a748e> in <module>()
      1 print('mis-matched years:', diff_records([[1900, 1.0]],
----> 2                                          [[1999, 2.0]]))

<ipython-input-16-d41327791c15> in diff_records(left, right)
     10         left_year, left_value = left[i]
     11         right_year, right_value = right[i]
---> 12         assert left_year == right_year,                'Record {0} is for different years: {1} vs {2}'.format(i, left_year, right_year)
     13         difference = left_value - right_value
     14         results.append([left_year, difference])

AssertionError: Record 0 is for different years: 1900 vs 1999mis-matched years:
~~~

~~~ {.python}
print('left is shorter', diff_records([[1900, 1.0]],
                                      [[1900, 10.0], [1901, 20.0]]))
~~~
~~~ {.error}
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-19-682d448d921e> in <module>()
      1 print('left is shorter', diff_records([[1900, 1.0]],
----> 2                                       [[1900, 10.0], [1901, 20.0]]))

<ipython-input-16-d41327791c15> in diff_records(left, right)
      4     Fails if the inputs are not for exactly corresponding years.
      5     '''
----> 6     assert len(left) == len(right),            'Inputs have different lengths.'
      7     num_years = len(left)
      8     results = []

AssertionError: Inputs have different lengths. left is shorter
~~~
~~~ {.python}
print('right is shorter', diff_records([[1900, 1.0], [1901, 2.0]],
                                       [[1900, 10.0]]))
~~~
~~~ {.error}
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-20-a475e608dd70> in <module>()
      1 print('right is shorter', diff_records([[1900, 1.0], [1901, 2.0]],
----> 2                                        [[1900, 10.0]]))

<ipython-input-16-d41327791c15> in diff_records(left, right)
      4     Fails if the inputs are not for exactly corresponding years.
      5     '''
----> 6     assert len(left) == len(right),            'Inputs have different lengths.'
      7     num_years = len(left)
      8     results = []

AssertionError: Inputs have different lengths. right is shorter
~~~

Excellent: the assertions we've added will now alert us if we try to work with badly-formatted or inconsistent data.

>## Error Handling {.challenge}
>
> Python scripts should have error handling code because:
>
> 1.  Python is an inherently unreliable language.
> 2.  Functions can return errors.
> 3.  One should never trust the data provided is what is expected.
> 4.  A python script would stop on an error, so the task wouldn't be accomplished.

> ## When to Complain? {.challenge}
>
> We have actually just committed the same mistake as the World Bank:
> if someone gives `annual_mean_temp` an invalid country identifier,
> it doesn't report an error,
> but instead returns an empty list,
> so the caller has to somehow know to look for that.
> Should it use an assertion to fail if it doesn't get data?
> Why or why not?

> ## Enumerating {.challenge}
>
> Python includes a function called `enumerate` that's often used in `for` loops.
> This loop:
>
> ~~~ {.python}
> for (i, c) in enumerate('abc'):
>     print(i, '=', c)
> ~~~
>
> prints:
>
> ~~~ {.output}
> 0 = a
> 1 = b
> 2 = c
> ~~~
>
> Rewrite `diff_records` to use `enumerate`.

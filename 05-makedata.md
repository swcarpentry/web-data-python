---
layout: page
title: Working With Data on the Web
subtitle: Publishing Data
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Write Python programs that share static data sets.

In our [previous lesson](01-getdata.html),
we built functions called `get_annual_mean_temp_by_country` and `diff_records`
to download temperature data for different countries and find annual differences.
The next step is to share our findings with the world by making publishing the data sets we generate.
To do this, we have to answer three questions:

*   How are we going to store the data?
*   How are people going to download it?
*   How are people going to find it?

The first question is the easiest to answer:
`diff_records` returns a list of (year, difference) pairs that we can write out as a CSV file:

~~~ {.python}
import csv

def save_records(filename, records):
    '''Save a list of [year, temp] pairs as CSV.'''
    with open(filename, 'w') as raw:
        writer = csv.writer(raw)
        writer.writerows(records)
~~~

Let's test it:

~~~ {.python}
save_records('temp.csv', [[1, 2], [3, 4]])
~~~

If we then look in the file `temp.csv`, we find:

~~~
1,2
3,4
~~~

as desired.

Now, where should this file go?
The answer is clearly "a server",
since data on our laptop is only accessible when we're online
(and probably not even then, since most people don't run a web server on their laptop).
But where on the server, and what should we call it?

The answer to those questions depends on how the server is set up.
On many multi-user Linux machines,
users can create a directory called something like `public_html` under their home directory,
and the web server will search in those directories.
For example,
if Nelle has a file called `thesis.pdf` in her `public_html` directory,
the web server will find it when it gets the URL `http://the.server.name/u/nelle/thesis.pdf`.
The specifics differ from one machine to the next, but the mechanism stays the same.

As for what we should call it, here we return to the key idea in REST:
every data set should be identified by a "guessable" URL.
In our case we'll use the name `left-right.csv`,
where `left` and `right` are the three-letter codes of the countries whose mean annual temperatures we are differencing.
We can then tell people that if they want to compare Australia and Brazil,
they should look for `http://the.server.name/u/nelle/AUS-BRA.csv`.
(We use upper case to be consistent with the World Bank's API.)

But what's to prevent someone from creating a badly-named (and therefore unfindable) file?
Someone could, for example, call `save_records('aus+bra.csv', records)`.
To prevent this (or at least reduce the risk), let's modify `save_records` as follows:

~~~ {.python}
import csv

def save_records(left, right, records):
    '''Save a list of [year, temp] pairs as CSV.'''
    filename = left + '-' + right + '.csv'
    with open(filename, 'w') as raw:
        writer = csv.writer(raw)
        writer.writerows(records)
~~~

We can now call it like this:

~~~ {.python}
save_records('AUS', 'BRA', [[1, 2], [3, 4]])
~~~

and then check that the right output file has been created.
Since we are bound to have the country codes anyway (having used them to look up our data), this is as little extra work as possible.

> ## Testing Output {.challenge}
>
> Modify `save_records` so that it can be tested using `cStringIO`.

> ## Deciding What to Check {.challenge}
>
> Should `save_records` check that every record in its input is the same length?
> Why or why not?

> ## Setting Up Locally {.challenge}
>
> Find out how to publish a file on your department's server.

>## Published Data Consistency {.challenge}
>
> It is important for the file names of published data to be consistent because;
>a) Some operating systems (e.g. Windows) treat spaces differently
>b) You may not have access to your department's server to rename them
>c) The cStringIO and csv libraries require it.
>d) the files and data can be processed programmatically.
>

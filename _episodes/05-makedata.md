---
title: "Publishing Data"
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Write Python programs that share static data sets.

We now have functions to download temperature data for different countries and find annual differences.
The next step is to share our findings with the world by publishing the data sets we generate.
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

> ## Lessons Learned {.callout}
>
> We use the `csv` library to write data
> for the same reason we use it to read:
> it correctly handles special cases (such as text containing commas).

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
users can create a directory called like `public_html` under their home directory,
and the web server will automatically search in those directories.
For example,
if Nelle has a file called `thesis.pdf` in her `public_html` directory,
the web server will find it when it gets the URL `http://the.server.name/~nelle/thesis.pdf`.
(The tilde `~` in front of Nelle's name is what tells the web server
to look in Nelle's `public_html` directory.)
The specifics differ from one machine to the next,
but the basic idea stays the same.

As for what we should call it, here we return to the key idea in REST:
every data set should be identified by a "guessable" URL.
In our case we'll use a name  like `left-right.csv`,
where `left` and `right` are the three-letter codes of the countries whose temperatures we are differencing.
We can then tell people that if they want to compare Australia and Brazil,
they should look for `http://the.server.name/~nelle/AUS-BRA.csv`.
(We use upper case to be consistent with the World Bank's API.)

But what's to prevent someone from creating a badly-named (and therefore unfindable) file?
Someone could, for example, call `save_records('aus+bra.csv', records)`.
To reduce the odds of this happening,
let's modify `save_records` to take country identifiers as parameters:

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
We are bound to have the country codes anyway (having used them to look up our data),
so this should seem natural to our users.

> ## Deciding What to Check {.challenge}
>
> Should `save_records` check that every record in its input has exactly two fields?
> Why or why not?
> What about country codes -
> should it contain a list of those that match actual countries
> and check that `left` and `right` are in that list?

> ## Setting Up Locally {.challenge}
>
> Find out how to publish a file on your department's server.

> ## Published Data Consistency {.challenge}
>
> It is important for the file names of published data to be consistent because:
>
> 1.  Some operating systems (e.g. Windows) treat spaces differently.
> 2.  You may not have access to your department's server to rename them.
> 3.  The `csv` library requires it.
> 4.  Programs can only process files and data correctly when they are.

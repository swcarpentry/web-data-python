---
layout: page
title: Working With Data on the Web
subtitle: Publishing Data
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Write Python programs that share data in a findable way.

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

The final step in this lesson is to make the data we generate findable.
It's not enough to tell people what the rule is for creating filenames,
since that doesn't tell them what data sets we've actually generated.
Instead, we need to create an [index](reference.html#index) to tell them what files exist.
For reasons we will see in a moment,
that index should also tell them when each data set was generated.

Here's the format we will use:

~~~
2014-05-26,FRA,TCD,FRA-TCD.csv
2014-05-27,AUS,BRA,AUS-BRA.csv
2014-05-27,AUS,CAN,AUS-CAN.csv
2014-05-28,BRA,CAN,BRA-CAN.csv
~~~

The four columns in this file are self-explanatory, but why do we bother to include the filename?
After all, we can re-generate it easily given the two country codes.
The answer is that while *we* know the rule for generating filenames,
other people's programs shouldn't have to.
Explicit is better than implicit.

Here's a function that updates the index file every time we generate a new data file:

~~~ {.python}
import time

def update_index(index_filename, left, right):
    '''Append a record to the index.'''

    # Read existing data.
    with open(index_filename, 'r') as raw:
        reader = csv.reader(raw)
        records = []
        for r in reader:
            records.append(r)
    
    # Create new record.
    timestamp = time.strftime('%Y-%m-%d')
    data_filename = left + '-' + right + '.csv'
    new_record = (timestamp, left, right, data_filename)
    
    # Save.
    records.append(new_record)
    with open(index_filename, 'w') as raw:
        writer = csv.writer(raw)
        writer.writerows(records)
~~~

Let's test it.
If our index file contains:

~~~
2014-05-26,FRA,TCD,FRA-TCD.csv
2014-05-27,AUS,BRA,AUS-BRA.csv
2014-05-27,AUS,CAN,AUS-CAN.csv
2014-05-28,BRA,CAN,BRA-CAN.csv
~~~

and we run:

~~~ {.python}
update_index('data/index.csv', 'TCD', 'CAN')
~~~

then our index file now contains:

~~~
2014-05-26,FRA,TCD,FRA-TCD.csv
2014-05-27,AUS,BRA,AUS-BRA.csv
2014-05-27,AUS,CAN,AUS-CAN.csv
2014-05-28,BRA,CAN,BRA-CAN.csv
2014-05-29,TCD,CAN,TCD-CAN.csv
~~~

Now that all of this is in place,
it's easy for us—and other people—to do new and exciting things with our data.
For example,
we can easily write a small program that tells us what data sets include information about a particular country
*and* have been published since we last checked:

~~~ {.python}
def what_is_available(index_file, country, after):
    '''What data files include a country and have been published since 'after'?'''
    with open(index_file, 'r') as raw:
        reader = csv.reader(raw)
        filenames = []
        for record in reader:
            if (record[0] <= after) and (record[1] == country or record[2] == country):
                filenames.append(record[3])
    return filenames

print what_is_available('data/index.csv', 'BRA', '2014-05-27')
~~~
~~~ {.output}
['AUS-BRA.csv', 'BRA-CAN.csv']
~~~

This may not seem like a breakthrough,
but it is actually an example of how the web helps researchers do new kinds of science.
With a little bit more work,
we could create a file on *our* machine to record when we last ran `what_is_available` for each of several different sites that are producing data.
Each time we run it, our program would:

*   read our local "what to check" file;
*   ask each data source whether it had any new data for us;
*   download and process that data; and
*   present us with a summary of the results.

This is exactly how blogs work.
Every blog reader keeps a list of blog URLs that it's supposed to check.
When it is run, it goes to each of those sites and asks them for their index file (which is typically called something like `feed.xml`).
It then checks the articles listed in that index against its local record of what has already been seen,
then downloads any articles that are new.

By automating this process, blogging tools help us focus attention on things that are actually worth looking at.

> ## Testing Output {.challenge}
>
Modify `save_records` so that it can be tested using `cStringIO`.

> ## Deciding What to Check {.challenge}
>
Should `save_records` check that every record in its input is the same length?
> Why or why not?

> ## Setting Up Locally {.challenge}
>
> Find out how to publish a file on your department's server.

> ## To Automate or Not {.challenge}
>
> Should `update_index` be called inside `save_records` so that the index is automatically updated every time a new data set is generated?
> Why or why not?

> ## Removing Redundant Redundancy {.challenge}
>
> `update_index` and `save_records` both construct the name of the data file.
> Refactor them to remove this redundancy.

> ## Generating a Local Index (Large) {.challenge}
>
> Generate a local index file to show what data sets were created when.

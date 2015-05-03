---
layout: page
title: Working With Data on the Web
subtitle: Making Data Findable
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Make data sets more useful by providing metadata.

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
            if (after <= record[0]) and (record[1] == country or record[2] == country):
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

>## Indexing {.challenge}
>
> Index's are important for generated data because: 
>a) They can be checked in an automated way for changes
>b) The web server will not display the directory without an index
>c) REST API's require an index to function
>d) its too complicated for a program to calculate itself.
>

---
layout: page
title: Working With Data on the Web
subtitle: Reference
---
## [Getting Data](01-getdata.html)

*   Many sites make data available for download via URLs that are formatted in specific ways.
*   Use the `requests` library to download data in Python programs.

## [Handling CSV Data](02-csv.html)

*   Use the `io` library to treat text as input or output files.
*   Use the `csv` library to read comma-separated values.

## [Generalizing and Handling Errors](03-generalize.html)

*   Write tests.

## [Visualization](04-visualize.html)

*   Use the `pyplot` library from `matplotlib` for simple visualizations.
*   Viewing data is often the first step toward understanding it.

## [Publishing Data](05-makedata.html)

*   Publish data by putting files with predictable names in a publicly-accessible location.

## [Making Data Findable](06-findable.html)

*   Create a machine-readable index to explicitly tell people what data sets are available.

## Glossary

Application Programming Interface (API):
:   A set of functions through which programs can use a service.

comma-separated values (CSV):
:   A common textual representation for tables
    in which the values in each row are separated by commas.

escape sequence:
:   A sequence of characters used to represent another character.
    For example,
    the two-letter escape sequence `\n` represents a newline character in Python,
    while the multi-letter escape sequence `&amp;` respresents an ampersand in HTML.

index:
:   A document or data set that contains information about,
    and pointers to,
    actual data sets.
    An index contains the metadata that makes actual data findable.

Representational State Transfer (REST):
:   a set of patterns for sharing data on the web.

silent failure:
:   Failing without producing any warning messages.
    Silent failures are hard to detect and debug.

status code:
:   A numerical value that indicates whether a function or other procedure succeeded,
    or if it failed, why.

unit testing tool:
:   A software library and associated tool or tools
    that helps programmers write short tests for their code
    and run them systematically.

wrapper:
:   A function that is "wrapped around" something
    to process that thing's output in some way.

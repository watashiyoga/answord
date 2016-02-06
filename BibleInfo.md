#contains information about how bibles are setup, how to obtain bibles,

# Bible Setup #

Bibles that are used with answord are nothing more than a sqlite database. I did this because sqlite comes with android and makes looking up verses and such very simple.

In order for a bible to work with Answord its schema should be setup as the following
Answord Sqlite Bible Schema:
```
TABLE bible
id INTEGER PRIMARY KEY
book VARCHAR(50)
chapter INTEGER
verse INTEGER
scripture VARCHAR(500)
```

  * There should be a record in the table that defines the name of the bible. For this the book column should be called **version** and the actual name of the bible should be in the scripture column

  * There should be a record in the table that defines a note for the bible. For this the book column should be called **note** and the actual note should be in the scripture column

## Bible Format Plans ##

The format at the moment is very spartan. It is just intend to get the basic of viewing a bible down but once the bible application is in better shape I plan on possibly changing the schema to allow for more elaborate features. Some features are
  * Titles
  * Notes
  * Cross References
  * Quotes
Pretty much features that are referenced in the OSIS format.

## What Bibles will come with Answord ##
I plan on making the World English Bible the basic bible to come with Answord. I chose this because its public domain and a bit easier to read than King James Version. I plan on having more public domain bibles available for download.
## How do I get ESV or other sword bibles to work with Answord ##
ESV is not public domain so I can't have it in as download. Instead the way to get this working is to use the mod2osis tool in libsword library. Once you have an osis file you can then convert that to sqlite database with osisparse.py A tutorial for this will be created once the bible is in version 1 and the demand for this becomes higher.
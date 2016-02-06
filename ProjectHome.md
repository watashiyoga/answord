Answord is a project with the aim to make a responsive feature-filled bible application for the android mobile platform. Rather than using online bibles as its source, it will use bibles stored on the device.
## Features planned for the project ##
  * Full Text Search
  * On the fly downloading of bibles
  * Multiple Bibles
## Overall Goals of the project ##
  * responsiveness
  * ease of use
## Current Phase ##
1/28 I am trying to find the best way to load bibles into the app. The problem is that the Android Platform has no distinct way to have a preloaded database in the apk. I have been researching this for awhile now and its been driving me crazy. But I have a plan that may work that I came across while reading some mailing lists I could have a downloadable sql file that I would download and run. and since the insert statements can be separated the database can be populated incrementally. There are other things to consider but I think this could be a good direction.
~~I am working on a osis to sqlite converter. Its in python because it seemed the easiest to do this in.~~
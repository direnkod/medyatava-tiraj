medyatava-tiraj
===============

\#direngezi  
\#occupygezi

parser.py
----------

This script reads newspaper statistics from medyatava.com/tiraj and generates a JSON file called `tiraj.json` from that data.  
You can adjust the oldest date to fetch using `OLDEST` variable in the script.

json-to-tsv.py
--------------

This script converts `tiraj.json` to a tab-separated-values (.tsv) file that can be used with several visualization libraries.

simple-stats.py
---------------

This is probably an invalid and meaningless way to analyze pressrun(tiraj) of mainstream and opposite news papers using `tiraj.json`.

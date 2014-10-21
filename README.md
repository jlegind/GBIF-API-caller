GBIF_API_caller
===============

This Python class **SearchAPI** can make API calls from a list of values and will parse the JSON response which is then outputted to a **flat text file** (tab separated).
It presupposes that the call is made to the GBIF Portal API http://www.gbif.org/developer/summary
Only the Species API and the Occurrence API have been tested.

Here is a usage example:

>my_api = SearchAPI('http://api.gbif.org/v1/species/match?name=', 
'D:/test/species.txt', 'D:/test/GBIFinterpreted_names.txt')

>my_api.take_parameters("usageKey", "scientificName", "canonicalName", "rank")

The first argument is the search url, in this case it must contain everything except the variable that comes from text file in the second argument. The third argument is the output file.

See the exeSearch file for more examples.

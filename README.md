GBIF_API_caller
===============

This Python class can make API calls from a list of values and will parse the JSON response which is then outputted to a text file.
It presupposes that the call is made to the GBIF Portal API http://www.gbif.org/developer/summary
Only the Species API and the Occurrence API have been tested.

Here is a usage example:

>my_api = SearchAPI('http://api.gbif.org/v1/species/match?', 'D:/test/species_names.txt', 'D:/test/GBIF_names.txt')
>my_api.take_parameters("usageKey", "scientificName", "canonicalName", "rank")


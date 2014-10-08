GBIF_API_caller
===============

The class can make API calls from a list of values and parses the JSON response which is outputted to a text file.

Here is an example:

**my_api = SearchAPI('http://api.gbif.org/v1/species/match?', 'D:/test/species_names.txt', 'D:/test/GBIF_names.txt')**
**my_api.take_parameters("usageKey", "scientificName", "canonicalName", "rank")**


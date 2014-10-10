__author__ = 'jlegind'

from searchAPI import SearchAPI

# my_api = SearchAPI('http://api.gbif.org/v1/species/',
#                    'G:/test/GISDnubtaxonomy_unique.txt',
#                    'G:/test/no_param_test.txt', suffix="/distributions?")
# my_api.take_parameters("locationId", "locality", "country", "status",
#                        "establishmentMeans", "sourceTaxonKey")

# my_api = SearchAPI('http://api.gbif.org/v1/species/match?', 'G:/test/taxon.txt', 'G:/test/GISDnubtaxonomy_test.txt')
# my_api.take_parameters("usageKey", "species", "scientificName", "canonicalName", "rank",
# name=3, kingdom=4)
#
# my_api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/test/GISDnubtaxonomy_unique.txt', 'G:/test/GISDnubtaxonomy_full_test.txt')
# my_api.take_parameters("key", "nubKey", "taxonID", "kingdom", "phylum", "order", "family", "genus",
#                        "species", "kingdomKey", "phylumKey", "classKey", "orderKey", "familyKey",
#                        "genusKey", "speciesKey", "datasetKey", "parentKey", "parent", "acceptedKey",
#                        "accepted", "scientificName", "canonicalName", "authorship", "nameType",
#                        "rank", "origin", "taxonomicStatus", "nomenclaturalStatus", "accordingTo",
#                        "numDescendants", "synonym", "class", "publishedIn", "references")
#
# my_api = SearchAPI('http://api.gbif.org/v1/species/',
#                    'G:/test/GISDnubtaxonomy_unique.txt',
#                    'G:/test/no_param_test2.txt')
# my_api.take_parameters("order", "family", "genus", "species")

# my_api = SearchAPI('http://api.gbif.org/v1/occurrence/search?scientificName=', 'G:/test/occ.txt', 'G:/test/occurrence_test.txt')
# my_api.take_parameters("order", "species", "country")

api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/test/GISDnubtaxonomy_unique.txt',
                'G:/test/vernacular_mk2.txt', suffix="/vernacularNames?")
api.take_parameters('vernacularName', 'language', 'sourceTaxonKey', 'preferred')

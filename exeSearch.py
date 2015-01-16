__author__ = 'jlegind'

from searchAPI import SearchAPI

# my_api = SearchAPI('http://api.gbif.org/v1/species/',
#                    'G:/test/GISDnubtaxonomy_unique.txt',
#                    'G:/test/no_param_test.txt', suffix="/distributions")
# my_api.take_parameters("locationId", "locality", "country", "status",
#                        "establishmentMeans", "sourceTaxonKey")

#my_api = SearchAPI('http://api.gbif.org/v1/species/match?', 'G:/test/taxon.txt', 'G:/test/GISDnubtaxonomy_test.txt')
#my_api.take_parameters("usageKey", "species", "scientificName", "canonicalName", "rank",
#name=3, kingdom=4)

# my_api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/test/GISDnubtaxonomy_unique.txt', 'G:/test/GISDnubtaxonomy_full_test.txt')
# my_api.take_parameters("key", "nubKey", "taxonID", "kingdom", "phylum", "order", "family", "genus",
#                        "species", "kingdomKey", "phylumKey", "classKey", "orderKey", "familyKey",
#                        "genusKey", "speciesKey", "datasetKey", "parentKey", "parent", "acceptedKey",
#                        "accepted", "scientificName", "canonicalName", "authorship", "nameType",
#                        "rank", "origin", "taxonomicStatus", "nomenclaturalStatus", "accordingTo",
#                        "numDescendants", "synonym", "class", "publishedIn", "references")

# my_api = SearchAPI('http://api.gbif.org/v1/species/',
#                    'G:/test/GISDnubtaxonomy_unique.txt',
#                    'G:/test/no_param_test2.txt')
# my_api.take_parameters("order", "family", "genus", "species")

my_api = SearchAPI('http://api.gbif.org/v1/species/match?kingdom=plantae&name=', 'G:/Custom exports/IUCN/species_search.txt', 'G:/test/IUCN_tax.txt')
my_api.take_parameters("usageKey", "species", "scientificName", "canonicalName", "rank")

# api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/test/GISDnubtaxonomy_unique.txt',
#                 'G:/test/vernacular_mk2.txt', suffix="/vernacularNames")
# api.take_parameters('vernacularName', 'language', 'sourceTaxonKey', 'preferred')
#
# api = SearchAPI('http://api.gbif.org/v1/occurrence/download/dataset/', 'G:/test/downloads.txt', 'G:/test/download_stats.txt')
# api.take_parameters('numberRecords', 'download')

#my_api = SearchAPI('http://api.gbif.org/v1/species/match?name=', 'G:/sweden_invasives/species.txt', 'G:/sweden_invasives/invasives_taxonomy.txt')
#my_api.take_parameters("usageKey", "kingdom", "family", "scientificName")

#my_api = SearchAPI('http://api.gbif.org/v1/organization/', 'G:/To publishers/arthro.txt', 'G:/To publishers/arthro_out.txt')
#my_api.take_parameters("title")
#ALA API call --------------------
# my_api = SearchAPI('http://collections.ala.org.au/ws/dataResource/', 'G:/ALA/api.txt', 'G:/ALA/lic.txt')
# my_api.take_parameters("name", "licenseType")
#---------------------------------


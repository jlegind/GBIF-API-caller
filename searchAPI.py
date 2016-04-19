__author__ = 'jlegind'

from urllib import parse, request
import json
import collections


class SearchAPI(object):
    def __init__(self, url, read_path, write_path, suffix='', separator='\t'):
        """
        :param url: JSON api url
        :param read_path: File that contains the search params
        :param write_path: Output file
        :param suffix: If the url has a suffix like /verbatim after the params this can be tagged on
        """
        self.wp = write_path
        self.file = open(read_path, mode='r', encoding='utf-8')
        self.write_file = open(write_path, mode='w', encoding='utf-8')
        self.url = url
        self.suffix = suffix
        self.appended = ''
        self.separator = separator

    def take_parameters(self, *args, **kwargs):
        """
        :param args: The JSON values you want returned
        :param kwargs: The API search term[key] in the API call,
                        and position[value] in the read_file (tab separated columns)
        """
        line = self.file.readline()
        while line:
            new_url = self.url
            to_paging_params = []
            split_line = line.split(self.separator)

            if kwargs:
                for k in kwargs:
                        kw = split_line[kwargs[k]].strip()
                        new_url += k+'='+parse.quote_plus(kw)+'&'
                        to_paging_params.append(kw)
            else:
                vl = split_line[0].strip()
                new_url += vl
                print(vl+" prrr---")
                self.appended = vl
                to_paging_params.append(vl)
            self.pagination(new_url.strip('&')+self.suffix, to_paging_params, args)
            line = self.file.readline()

    def pagination(self, url, terms, keys, offset=None, appended=''):
        """
        :param url: Takes the url with the search term and value added
        :param terms: A list of search values
        :param keys: A list of JSON keys that you want the value for
        :param offset: Used to increment paging
        """
        #print(url)
        if not terms or offset == None:
            print('Absolute no_param')
            new_url = url
        else:
            new_url = url+'&offset='+str(offset)+'&limit=100'
        print(new_url)
        try:
            response = request.urlopen(new_url)
            r = response.read()
            decoded_json = json.loads(r.decode('utf-8'))
            print('debug1')
            end_of_records = None
            try:
                results = decoded_json['results']
                end_of_records = decoded_json['endOfRecords']
            except KeyError:
                print('keyError !!!!!!!')
                results = decoded_json
                #print(results)

            if end_of_records is False:
                print('False')
                for j in results:
                    self.parse_json(j, keys, terms)
                offset += 100
                self.pagination(url, terms, keys, offset=offset)
            else:
                print('debug2')
                try:
                    for j in results:
                        #print('debug3')
                        self.parse_json(j, keys, terms)
                except:
                    #print('8888debuggg')
                    self.parse_json(results, keys, terms)
        except Exception as err:
            print(err, 'err')
            print(type(err))
            #Below is NOT TESTED outside a plain non-JSON result (like the count API call)
            self.write_output(decoded_json)

    def write_output(self, input_to_file):
        #print('debug5')
        if isinstance(input_to_file, collections.Iterable):
            output = '\t'.join(str(e) for e in input_to_file)
        else:
            output = input_to_file
        #output string is created from the input_to_file list. Integers are cast to str
        #print(output)
        self.write_file.write(str(output)+'\t'+self.appended+'\n')

    def parse_json(self, json_element, keys, terms):
        list_output = []
        #print('debug4')
        for k in keys:
            try:
                list_output.append(json_element[k])
            except KeyError:
                #print('keyerror---')
                list_output.append('NULL')
        #print('debug3', terms)
        [list_output.append(i) for i in terms]
        #print('debug4', list_output)
        self.write_output(list_output)


def main():
    #my_api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/GIASIP/export/nubkeys.txt', 'G:/GIASIP/export/GISDnubtaxonomy_test.txt')
    """my_api.take_parameters("key", "nubKey", "taxonID", "kingdom", "phylum", "order", "family", "genus",
                           "species", "kingdomKey", "phylumKey", "classKey", "orderKey", "familyKey",
                           "genusKey", "speciesKey", "datasetKey", "parentKey", "parent", "acceptedKey",
                           "accepted", "scientificName", "canonicalName", "authorship", "nameType",
                           "rank", "origin", "taxonomicStatus", "nomenclaturalStatus", "accordingTo",
                           "numDescendants", "synonym", "class", "publishedIn", "references",
                           no_param=0)
    """
    # my_api = SearchAPI('http://api.gbif.org/v1/species/', 'G:/GIASIP/export/GISDnubtaxonomy_unique.txt', 'G:/GIASIP/export/no_param_test.txt', suffix="/distributions?")
    # my_api.take_parameters("locationId", "locality", "country", "status", "establishmentMeans", "sourceTaxonKey")

    # my_api = SearchAPI('http://api.gbif.org/v1/species/', 'C:/Users/jlegind/Dropbox/GIASIP/taxon_keys.txt', 'C:/Users/jlegind/Dropbox/GIASIP/export/GISDvernacularnames2.txt', suffix="/vernacularNames?")
    # my_api.take_parameters("vernacularName", "language", "sourceTaxonKey", "preferred")
    #
    # my_api = SearchAPI('http://api.gbif.org/v1/species/match?kingdom=Animalia&', 'G:/Custom exports/Imanol/names.txt', 'G:/Custom exports/Imanol/interpreted_names.txt', separator=';')
    # my_api.take_parameters("usageKey",
    #                          "scientificName", "rank",
    #                        name=0)


    # my_api = SearchAPI('http://api.gbif.org/v1/species/match?', 'G:/nub/toLookup.txt', 'G:/Custom exports/interpreted_names_oldNub.txt', separator=';')
    # my_api.take_parameters("usageKey",
    #                          "scientificName", "kingdom", "phylum", "class", "order", "family", "genus", "rank", "status", "confidence",
    #                        name=0)

    # my_api = SearchAPI('http://api.gbif.org/v1/dataset/', 'G:/Custom exports/dataset_list.csv', 'G:/Custom exports/lic_datasets.txt')
    # my_api.take_parameters("key", "title", "type")
    # my_api.take_parameters("key", "title", identifier=0)

    my_api = SearchAPI('http://api.gbif.org/v1/occurrence/count?datasetKey=', 'G:/Deletion/deleted_datasets/datasetkeys.csv', 'G:/Custom exports/del_counts.txt')
    my_api.take_parameters(None)
    # UGLY HACK line 49 offset=None , must be 0

if __name__ == '__main__':
    main()
__author__ = 'jlegind'

from urllib import parse, request
import json


class SearchAPI(object):
    def __init__(self, url, read_path, write_path, suffix=''):
        """
        :param url: JSON api url
        :param read_path: File that contains the search parameter values
        :param write_path: Output file
        :param suffix: If the url has a suffix like /verbatim after the params; this can be tagged on
        """
        self.wp = write_path
        self.file = open(read_path, mode='r', encoding='utf-8')
        self.write_file = open(write_path, mode='w', encoding='utf-8')
        self.url = url
        self.suffix = suffix
        self.appended = ''

    def take_parameters(self, *args, **kwargs):
        """
        :param args: The JSON values you want returned
        :param kwargs: The API search term[key] in the API call,
                        and position[value] in the read_file (tab separated columns)
                        example: (...name=3, kingdom=4) where the int is the position
                        if there is one column only don't add any kwargs
        """
        line = self.file.readline()
        while line:
            new_url = self.url
            to_paging_params = []
            split_line = line.split('\t')

            if kwargs:
                for k in kwargs:
                        kw = split_line[kwargs[k]].strip()
                        new_url += k+'='+parse.quote_plus(kw)+'&'
                        to_paging_params.append(kw)
            else:
                val = split_line[0].strip()
                new_url += val
                self.appended = val
                to_paging_params.append(val)
            self.pagination(new_url.strip('&')+self.suffix, to_paging_params, args)
            line = self.file.readline()

    def pagination(self, url, terms, keys, offset=0):
        """
        :param url: Takes the url with the search term and value added
        :param terms: A list of search values
        :param keys: A list of JSON keys that you want the value for
        :param offset: Used to increment paging
        """
        limit = 20
        print(url)
        new_url = url

        try:
            response = request.urlopen(new_url)
            r = response.read()
            decoded_json = json.loads(r.decode('utf-8'))
            end_of_records = None
            try:
                #Tests for the existence of the list results[]
                results = decoded_json['results']
                end_of_records = decoded_json['endOfRecords']
            except KeyError:
                print('harmless keyError ! continue ...')
                results = decoded_json

            if end_of_records is False:
                print('False')
                for j in results:
                    self.parse_json(j, keys, terms)
                offset += limit
                new_url = url+'&offset='+str(offset)+'&limit='+str(limit)
                self.pagination(new_url, terms, keys, offset=offset)
            else:
                try:
                    #Tests if results is a list
                    for j in results:
                        self.parse_json(j, keys, terms)
                except:
                    self.parse_json(results, keys, terms)
        except Exception as err:
            print(err, 'err')
            print(type(err))

    def write_output(self, input_to_file):
        output = '\t'.join(str(e) for e in input_to_file)
        #output string is created from the input_to_file list. Integers are cast to str
        self.write_file.write(str(output+'\n'))

    def parse_json(self, json_element, keys, terms):
        list_output = []
        for k in keys:
            try:
                list_output.append(json_element[k])
            except KeyError:
                list_output.append('NULL')
        [list_output.append(i) for i in terms]
        self.write_output(list_output)

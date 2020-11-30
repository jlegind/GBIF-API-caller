import requests
import csv


class SearchAPI(object):
    def __init__(self, url, read_path, write_path, suffix='', separator='\t'):
        """
        :param url: JSON api url
        :param read_path: File that contains the search params
        :param write_path: Output file
        :param suffix: If the url has a suffix like /verbatim after the params this can be tagged on
        """
        self.wp = write_path
        self.file = open(read_path, mode='r', encoding='utf-8-sig')
        self.write_file = open(write_path, mode='w', encoding='utf-8')
        self.url = url
        self.suffix = suffix
        self.appended = ''
        self.separator = separator

    def make_search_name(self, positions):
        '''
        assumes multiple columns and composes a name from these in order of positions
        param: positions = a LIST of column positions in a csv/text file
        '''
        line = self.file.readline()
        while line:
            rowlist = line.split(self.separator)
            # res = [name for name in rowlist]
            name = [rowlist[e] for e in positions]
            stripped_name = [j.rstrip() for j in name]
            stripped_name = ' '.join(stripped_name)
            print('stripped name: ', stripped_name)
            line = self.file.readline()
            search_url = self.url+stripped_name
            yield search_url


    def searching_gbif_api(self, url, offset=0):
        '''
        Just get the GBIF api search result with paging if necessary. Modeled on the recursive extract_values function.
        url: example ... http://api.gbif.org/v1/species/match?kingdom=Animalia&PLACEHOLDER FOR BINOMIAL OR TRINOMIAL
        '''
        res = []
        print('gained url = ',type(url), url)

        def paging(url, res, offset):
            nurl = '{}&offset={}'.format(url, offset)
            print(nurl)
            rson = requests.get(nurl)
            rson = rson.json()
            if not isinstance(rson, list):
                return rson
            print('trying1')
            _result = rson['results']
            print(len(_result), _result)

            if rson['endOfRecords'] == True:
                print('!the END!')
                res.append(_result)
                print('res now = ', _result)
            else:
                offset = offset + 200
                res.append(_result)
                paging(url, res, offset)
            return res

        final = paging(url, res, offset)
        return final


    def filter_api_response(self, response, fields):
        '''
        response = json response from api
        fields = A list of fields to parse for
        Returns a dict to be made into a row. 1 dict == 1 row
        '''
        try:
            resp_dict = dict.fromkeys(fields)
            for j in fields:
                resp_dict[j] = response[j]
            return resp_dict
        except Exception as e:
            #These names have no acceptedUsageKey because they are ACCEPTED names!
            print('errrror', e)
            copyfields = fields.copy()
            copyfields.remove('acceptedUsageKey')
            #removes the term 'acceptedUsageKey' from the dictionary
            accepted_dict = dict.fromkeys(copyfields)
            print('after syndict')
            print('syn dict -- ', accepted_dict)
            for item in copyfields:
                accepted_dict[item] = response[item]

            return accepted_dict


myapi = SearchAPI('http://api.gbif.org/v1/species/match?kingdom=Animalia&name=', 'H:/into_api/atomized_fish_list.txt', 'H:/output_api/interpreted_names_fish.txt')
res = myapi.make_search_name([0,1,2])
#The name file has the search name atomized and the list contains the name parts by index number

out_directory = 'H:/output_api/'
read_file = 'H:/into_api/atomized_fish_list.txt' 'H:/output_api/interpreted_names_fish.txt'

with open('H:/output_api/interpreted_names_fish.txt', 'w+', newline='', encoding='utf-8') as wfile:
    field_list = ["usageKey", "acceptedUsageKey", "scientificName", "kingdom", "phylum", "class", "order", "family",
                  "genus", "rank", "status", "confidence"]
    writer = csv.DictWriter(wfile, fieldnames=field_list, delimiter='\t')
    writer.writeheader()

    for j in res:
        rsp = requests.get(j)
        rsp = rsp.json()
        reply = myapi.searching_gbif_api(j)
        try:
            res = myapi.filter_api_response(reply, field_list)
            writer.writerow(res)
        except Exception as e:
            print('ERROR', e)
            print(res)


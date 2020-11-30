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
        Just get the GBIF api search result
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
                offset = offset + 20
                print('not end yet... ', len(_result), _result)
                res.append(_result)
                paging(url, res, offset)
            return res

        final = paging(url, res, offset)
        return final


    def filter_api_response(self, response, fields):
        '''
        response = json response from api
        fields = A list of fields to parse for
        '''
        try:
            resp_dict = dict.fromkeys(fields)
            for j in fields:
                resp_dict[j] = response[j]
            return resp_dict
        except Exception as e:
            print('errrror', e)
        # else:
            copyfields = fields.copy()
            print('fields scope: ', copyfields)
            copyfields.remove('acceptedUsageKey')
            print('copy ', copyfields)
            print('QQQ', response)
            synonym_dict = dict.fromkeys(copyfields)
            print('after syndict')
            print('syn dict -- ', synonym_dict)
            for item in copyfields:
                synonym_dict[item] = response[item]
                print(response[item])
            print('accepted dict!!! ', synonym_dict)
            return synonym_dict


myapi = SearchAPI('http://api.gbif.org/v1/species/match?kingdom=Animalia&name=', 'H:/into_api/atomized_fish_list.txt', 'H:/output_api/interpreted_names_fish.txt')
res = myapi.make_search_name([0,1,2])
#The name file has the search name atomized and the list contains the name parts by index number

out_directory = 'H:/output_api/'
read_file = 'H:/into_api/atomized_fish_list.txt' 'H:/output_api/interpreted_names_fish.txt'
error_file = open(out_directory+'taxon_fail.csv', mode='w', encoding='utf-8', newline='')
error_writer = csv.writer(error_file, delimiter='\t')

with open('H:/output_api/interpreted_names_fish.txt', 'w+', newline='') as wfile:
    field_list = ["usageKey", "acceptedUsageKey", "scientificName", "kingdom", "phylum", "class", "order", "family",
                  "genus", "rank", "status", "confidence"]
    writer = csv.DictWriter(wfile, fieldnames=field_list, delimiter='\t')
    writer.writeheader()

    for j in res:
        print('name url == ', j, type(j))
        rsp = requests.get(j)
        rsp = rsp.json()
        # print(rsp['usageKey'])
        reply = myapi.searching_gbif_api(j)
        try:
            res = myapi.filter_api_response(reply, field_list)
            print('return dict === ', res)
            writer.writerow(res)
        except Exception as e:
            print('ERROR', e)
            print(res)
            # message = 'The {} lookup failed. No match found in the GBIF taxon backbone.'.format(j)
            print()
            # error_writer.writerow({'error': message})
            # continue
            # break
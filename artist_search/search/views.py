from django.shortcuts import render
from django.http import HttpResponse
import json

def read_data(fn):
    with open(fn, 'r') as f:
        data = f.read()
    return data

def import_data(fn):
    data = read_data(fn)
    return json.loads(data)

def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')


def api_page(request, data=None):
    if data == None:
        raw_data = import_data('search/data.json')
        data = raw_data['artists']
    searcher = SearchEngine(data=data)
    results = searcher.search(**request.GET.dict())
    return HttpResponse(json.dumps(results),
                        content_type='application/json'
                        )

def set_bias(artist_dict,median_age):
    artist_dict['bias'] = abs(artist_dict['age'] - median_age)
    return artist_dict


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def bestfit(self,data):
        """
        given a dataset order by middle of age range
        :param data: list of dicts {age:int, uuid = ID}
        :return: sorted data biased to middle of age range
        """
        try:
            ages = [i['age'] for i in data]
            max_age, min_age = max(ages),min(ages)
            median_age = ((max_age - min_age) / 2.0) + min_age
            decorated_data= [set_bias(i, median_age) for i in data]
            return sorted(decorated_data,key=lambda artist : artist['bias'])
        except ValueError:
            return data


    def search(self, min=None, max=None, **kwargs):
        r = self.data
        if max:
            r = [i for i in r if i['age'] <= int(max)]
        if min:
            r = [i for i in r if i['age'] > int(min)]
        return self.bestfit(r)

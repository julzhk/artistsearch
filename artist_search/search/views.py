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


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def search(self, min=None, max=None, **kwargs):
        r = self.data
        if max:
            r = [i for i in r if i['age'] < int(max)]
        if min:
            r = [i for i in r if i['age'] > int(min)]
        return r

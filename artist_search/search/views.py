from django.shortcuts import render
from django.http import HttpResponse
import json

def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')


def api_page(request, data=None):
    searcher = SearchEngine(data=data)
    min = request.GET.get('min',None)
    max = request.GET.get('max',None)
    results = searcher.search(min=min, max=max)
    return HttpResponse(json.dumps(results),
                        content_type='application/json'
                        )


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def search(self, min=None, max=None, **kwargs):
        r = self.data
        if max:
            r = [i for i in r if i['age'] < max]
        if min:
            r = [i for i in r if i['age'] > int(min)]
        return r

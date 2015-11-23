from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')


def api_page(request):
    return HttpResponse(content_type='application/json')


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def search(self, min=None, max=None, **kwargs):
        r = self.data
        if max:
            r = [i for i in r if i['age'] < max]
        if min:
            r = [i for i in r if i['age'] > min]
        return r

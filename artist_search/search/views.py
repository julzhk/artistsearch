from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')


def api_page(request):
    pass


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def search(self, min=None, max=None, **kwargs):
        min_age = min
        max_age = max
        r = self.data
        if max_age:
            r = [i for i in r if i['age']< max_age]
        if min_age:
            r = [i for i in r if i['age']> min_age]
        return r

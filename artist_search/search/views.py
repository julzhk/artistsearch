from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')


def api_page(request):
    pass


class SearchEngine(object):
    def __init__(self, data):
        self.data = data

    def search(self, *args, **kwargs):
        min_age = kwargs.get('min',0)
        max_age = kwargs.get('max',900)
        r = [i for i in self.data if i['age']< max_age]
        return r

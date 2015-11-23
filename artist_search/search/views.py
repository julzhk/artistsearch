from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse('<html><title>Artist Search API</title></html>')

def api_page(request):
    pass


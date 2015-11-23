from django.core.urlresolvers import resolve
from django.test import TestCase
from search.views import home_page, api_page
from django.http import HttpRequest

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Artist Search API</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

class APITest(TestCase):

    def test_root_url_resolves_to_api_view(self):
        found = resolve('/api')
        self.assertEqual(found.func, api_page)

    def test_root_url_with_trailing_slash_resolves_to_api_view(self):
        found = resolve('/api/')
        self.assertEqual(found.func, api_page)

class DataSearch(TestCase):
    def test_simple_search(self):
        data = [{"age": 10, "uuid": "id1"},
                {"age": 20, "uuid": "id2"},
                {"age": 30, "uuid": "id3"}
                ]
        searcher = SearchEngine(data)
        result = searcher.search(max=11)
        self.assertEqual(len(result), 1)

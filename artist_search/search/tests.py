from django.core.urlresolvers import resolve
from django.test import TestCase
from search.views import home_page, api_page, SearchEngine
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


class SimpleAPITest(TestCase):
    def test_root_url_resolves_to_api_view(self):
        found = resolve('/api')
        self.assertEqual(found.func, api_page)

    def test_root_url_with_trailing_slash_resolves_to_api_view(self):
        found = resolve('/api/')
        self.assertEqual(found.func, api_page)

    def test_root_url_resolves_to_api_view_with_min_age_parameter(self):
        found = resolve('/api?min=0')
        self.assertEqual(found.func, api_page)

    def test_root_url_resolves_to_api_view_with_max_age_parameter(self):
        found = resolve('/api?max=100')
        self.assertEqual(found.func, api_page)

    def test_root_url_resolves_to_api_view_with_max_min_age_parameter(self):
        found = resolve('/api?min=0&max=100')
        self.assertEqual(found.func, api_page)


class DataSearch(TestCase):

    def setUp(self):
        self.data = [
                {"age": 10, "uuid": "id1"},
                {"age": 20, "uuid": "id2"},
                {"age": 30, "uuid": "id3"}
                ]
        self.searcher = SearchEngine(self.data)

    def test_simple_search(self):
        result = self.searcher.search(max=11)
        self.assertEqual(len(result), 1)

    def test_simple_search_results(self):
        result = self.searcher.search(max=11)
        result = result[0]
        self.assertEqual(result['age'], 10)

    def test_simple_search_results_multiple_results(self):
        result = self.searcher.search(max=21)
        self.assertEqual(len(result), 2)

    def test_simple_search_no_params_results_shows_all(self):
        result = self.searcher.search()
        self.assertEqual(len(result), 3)

    def test_max_age_search_has_correct_ids(self):
        result = self.searcher.search(max=21)
        ids = [i['uuid'] for i in result]
        self.assertTrue('id1' in ids)
        self.assertTrue('id2' in ids)
        self.assertTrue('id3' not in ids)

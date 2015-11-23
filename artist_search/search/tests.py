from django.core.urlresolvers import resolve
from django.test import TestCase
from search.views import home_page, api_page, SearchEngine
from django.http import HttpRequest
import json

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

    def test_max_and_min_search_count(self):
        result = self.searcher.search(max=21, min=11)
        self.assertEqual(len(result), 1)

    def test_max_and_min_search_id(self):
        result = self.searcher.search(max=21, min=11)
        self.assertEqual(result[0]['uuid'], 'id2')

class APIJSONTest(TestCase):

    def setUp(self):
        self.data = [
            {"age": 10, "uuid": "id1"},
            {"age": 20, "uuid": "id2"},
            {"age": 30, "uuid": "id3"}
        ]

    def test_api_returns_json(self):
        request = HttpRequest()
        response = api_page(request)
        self.assertTrue(response.status_code,200)
        self.assertTrue('json' in response['Content-Type'])

    def test_api_with_mock_data_returns_json(self):
        request = HttpRequest()
        response = api_page(request, data=self.data)
        self.assertTrue(response.status_code,200)
        self.assertTrue('json' in response['Content-Type'])

    def test_api_with_mock_data_returns_data_convert_from_json(self):
        request = HttpRequest()
        response = api_page(request, data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),3)

    def test_api_with_mock_data_returns_correct_data_from_json(self):
        request = HttpRequest()
        response = api_page(request, data=self.data)
        json_data = json.loads(response.content)
        ids = [i['uuid'] for i in json_data]
        self.assertTrue('id1' in ids)
        self.assertTrue('id2' in ids)
        self.assertTrue('id3' in ids)

class APIJSONFilterTest(TestCase):

    def setUp(self):
        self.data = [
            {"age": 10, "uuid": "id1"},
            {"age": 20, "uuid": "id2"},
            {"age": 30, "uuid": "id3"}
        ]


    def test_api_with_mock_data_with_no_filter_json_count(self):
        request = HttpRequest()
        found = resolve('/api')
        response = found.func(request,data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),3)

    def test_api_with_mock_data_with_one_filter_json_count(self):
        request = HttpRequest()
        request.GET = {'min':'11'}
        found = resolve('/api')
        response = found.func(request,data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),2)


    def test_api_with_mock_data_with_two_filters_json_count(self):
        request = HttpRequest()
        request.GET = {'min':'11','max':21}
        found = resolve('/api')
        response = found.func(request,data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),1)

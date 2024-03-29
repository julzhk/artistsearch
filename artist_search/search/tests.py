from django.core.urlresolvers import resolve
from django.test import TestCase
from search.views import home_page, api_page, SearchEngine, read_data, import_data
from django.http import HttpRequest, QueryDict
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

class DataSearchBestFit(TestCase):
    def setUp(self):
        self.data = [
            {"age": 10, "uuid": "id1"},
            {"age": 20, "uuid": "id2"},
            {"age": 30, "uuid": "id3"},
            {"age": 40, "uuid": "id4"},
            {"age": 50, "uuid": "id5"}
        ]
        self.searcher = SearchEngine(self.data)

    def test_search_function(self):
        result = self.searcher.bestfit(data=self.data)
        ages = [i['age'] for i in result]
        self.assertEqual(ages[0],30)
        self.assertTrue(ages[1] == 20 or ages[1] == 40)
        self.assertEqual(ages[-1],50)

    def test_search_order(self):
        result = self.searcher.search(min=0,max=60)
        ages = [i['age'] for i in result]
        self.assertEqual(ages[0],30)
        self.assertTrue(ages[1] == 20 or ages[1] == 40)
        self.assertEqual(ages[-1],50)


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
        request.GET = QueryDict('min=11')
        found = resolve('/api')
        response = found.func(request,data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),2)


    def test_api_with_mock_data_with_two_filters_json_count(self):
        request = HttpRequest()
        request.GET = QueryDict('min=11&max=21')
        found = resolve('/api')
        response = found.func(request,data=self.data)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),1)


class ReadDataFile(TestCase):
    def test_read_file(self):
        data = read_data('search/data.json')
        self.assertTrue(len(data)>0)

    def test_import_data(self):
        data = import_data('search/data.json')
        self.assertTrue('artists' in data)

class RealAPI(TestCase):

    def test_get_list_from_real_request(self):
        request = HttpRequest()
        response = api_page(request)
        json_data = json.loads(response.content)
        self.assertTrue(len(json_data)>0)

    def test_get_list_from_real_request_with_min_filter(self):
        request = HttpRequest()
        request.GET = QueryDict('min=11')
        response = api_page(request)
        json_data = json.loads(response.content)
        self.assertTrue(len(json_data)>0)

    def test_get_list_from_real_request_with_max_filter(self):
        request = HttpRequest()
        request.GET = QueryDict('max=21')
        response = api_page(request)
        json_data = json.loads(response.content)
        self.assertTrue(len(json_data)>0)

    def test_get_list_from_real_request_with_min_max_filter(self):
        request = HttpRequest()
        request.GET = QueryDict('min=31&max=21')
        response = api_page(request)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data),0)

    def test_get_list_from_real_request_with_min_max_one_age_filter(self):
        request = HttpRequest()
        request.GET = QueryDict('max=21&min=20')
        response = api_page(request)
        json_data = json.loads(response.content)
        self.assertTrue(len(json_data)>0)

import json

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from task.views import create_category, edit_category, delete_category, get_tasks
from tests.endpoint_helper import default_category, post_category_url, get_categories_url, put_category_url, \
    delete_category_url


class GetCategoryTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None):
        if category_data is None:
            category_data = default_category
        self.create_category(category_data)

    def create_category(self, category_data, expected_http_status=201):
        category_request = self.factory.post(post_category_url, category_data)
        category_response = create_category(category_request)

        self.assertEqual(category_response.status_code, expected_http_status)

    def test_get_tasks(self, expected_http_status=200):
        request = self.factory.get(get_categories_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_http_status)
        json_data = json.loads(response.content.decode())
        self.assertEqual(1, len(json_data))
        self.assertEqual(default_category['name'], json_data[0]['name'])


class PostCategoryTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def get_tasks(self, category_name, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertContains(response, category_name, 1)

    def test_post_tasks(self):
        self.create_category(default_category)
        self.get_tasks(default_category.get('name'))

    def test_post_categories_empty_name(self):
        self.create_category({'name': ''}, 400)

    def test_post_categories_whitespace_character(self):
        self.create_category({'name': '\t'}, 400)

    def test_post_categories_special_character(self):
        self.create_category({'name': '​'}, 400)

    def test_post_categories_missing_name_property(self):
        self.create_category({'NaN': 'totally_legit_name'}, 400)


class PutCategoryTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_category(default_category)

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def modify_category(self, category_id, new_name_data, expected_status_code=200):
        request = self.factory.put(f'{put_category_url}/{category_id}', new_name_data, content_type='application/json')
        response = edit_category(request, category_id)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

    def get_tasks(self, category_name, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertContains(response, category_name.get('name'), 1)

    def test_put_tasks(self):
        new_category_name = {'name': 'modified_name'}
        self.modify_category(1, new_category_name)
        self.get_tasks(new_category_name)

    def test_put_categories_empty_name(self):
        self.create_category({'name': ''}, 400)

    def test_put_categories_whitespace_character(self):
        self.create_category({'name': '\t'}, 400)

    def test_put_categories_special_character(self):
        self.create_category({'name': '​'}, 400)

    def test_put_categories_missing_name_property(self):
        self.create_category({'NaN': 'totally_legit_name'}, 400)


class DeleteCategoryTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_category(default_category)

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def delete_category(self, category_id, expected_status_code=200):
        request = self.factory.delete(f'{delete_category_url}/{category_id}')
        response = delete_category(request, category_id)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

    def get_tasks(self, expected_status_code=404):
        request = self.factory.get(get_categories_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

    def test_delete_tasks(self):
        self.delete_category(1)
        self.get_tasks()

    def test_delete_nonexistent_category_id(self):
        self.delete_category(9999, 404)

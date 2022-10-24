import json

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from .views import get_categories, create_category, create_task

default_category = {'name': 'test_category'}
default_task = {'name': 'test_task'}

get_categories_url = '/api/categories/'
post_category_url = '/api/categories/create/'
put_category_url = '/api/categories/edit/'
delete_category_url = '/api/categories/delete/'

get_tasks_url = '/api/tasks/'
post_tasks_url = '/api/tasks/create/'
put_tasks_url = '/api/tasks/edit/'
delete_tasks_url = '/api/tasks/delete/'


class GetCategoryTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None):
        if category_data is None:
            category_data = default_category
        self.create_category(category_data)

    def create_category(self, category_data):
        category_request = self.factory.post(post_category_url, category_data)
        category_response = create_category(category_request)

        self.assertEqual(category_response.status_code, 201)

    def test_get_categories(self):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, 200)
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

    def create_task(self, task_data, expected_http_status=201):
        task_request = self.factory.post(post_tasks_url, task_data)
        task_response = create_task(task_request)

        self.assertEqual(task_response.status_code, expected_http_status)

    def get_categories(self, category_name, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertContains(response, category_name, 1)

    def test_post_categories(self):
        self.create_category(default_category)
        self.get_categories(default_category.get('name'))

    def test_post_categories_empty_name(self):
        self.create_category({'name': ''}, 400)

    def test_post_categories_whitespace_character(self):
        self.create_category({'name': '\t'}, 400)

    def test_post_categories_special_character(self):
        self.create_category({'name': '​'}, 400)

    def test_post_categories_missing_name_property(self):
        self.create_category({'NaN': 'totally_legit_name'}, 400)

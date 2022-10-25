import json

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from task.views import get_categories, create_category, create_task, get_tasks, edit_task, delete_task
from tests.endpoint_helper import default_category, post_category_url, get_categories_url, post_tasks_url, \
    get_tasks_url, put_tasks_url, delete_tasks_url

default_task_create = {
    'name': 'test_task',
    'category': 1,
    'deadline': '2022-10-25',
    'description': 'test description',
    'title': 'test_title'
}

default_task = {
    'id': 1,
    'category': {
        'id': 1,
        'name': default_category.get('name')
    },
    'deadline': default_task_create.get('deadline'),
    'description': default_task_create.get('description'),
    'title': default_task_create.get('title')
}


class GetTaskTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None, task_data=None):
        if category_data is None:
            category_data = default_category
        if task_data is None:
            task_data = default_task_create
        self.create_category(category_data)
        self.create_task(task_data)

    def get_categories(self, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

        return json.loads(response.content.decode())

    def create_task(self, task_data, expected_http_status=201):
        task_request = self.factory.post(post_tasks_url, task_data)
        task_response = create_task(task_request)

        self.assertEqual(task_response.status_code, expected_http_status)

    def create_category(self, category_data, expected_http_status=201):
        category_request = self.factory.post(post_category_url, category_data)
        category_response = create_category(category_request)

        self.assertEqual(category_response.status_code, expected_http_status)

    def test_get_tasks(self):
        request = self.factory.get(get_tasks_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content.decode())[0]

        self.assertJSONEqual(json.dumps(default_task), json.dumps(json_data))


class PostTaskTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None):
        if category_data is None:
            category_data = default_category
        self.create_category(category_data)

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def get_categories(self, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

        return json.loads(response.content.decode())

    def get_tasks(self, expected_status_code=200):
        request = self.factory.get(get_tasks_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        return json.loads(response.content.decode())[0]

    def create_task(self, task_data, expected_http_status=201):
        task_request = self.factory.post(post_tasks_url, task_data)
        task_response = create_task(task_request)

        self.assertEqual(task_response.status_code, expected_http_status)

    def test_post_tasks(self):
        self.create_task(default_task_create)
        self.get_tasks()

    def test_post_tasks_empty(self):
        self.create_category({}, 400)

    def test_post_tasks_nonexistent_id(self):
        self.create_category({
            'name': 'test_task',
            'category': 9999,
            'deadline': '2022-10-25',
            'description': 'test description',
            'title': 'test_title'
        }, 400)

    def test_post_tasks_special_character(self):
        self.create_category({
            'name': '​',
            'category': 9999,
            'deadline': '2022-10-25',
            'description': 'test description',
            'title': 'test_title'
        }, 400)

    def test_post_tasks_missing_name_property(self):
        self.create_category({
            'category': 1,
            'deadline': '2022-10-25',
            'description': 'test description',
            'title': 'test_title'
        }, 400)


class PutTaskTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None):
        if category_data is None:
            category_data = default_category
        self.create_category(category_data)

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def get_categories(self, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

        return json.loads(response.content.decode())

    def get_tasks(self, expected_status_code=200):
        request = self.factory.get(get_tasks_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        return json.loads(response.content.decode())[0]

    def create_task(self, task_data, expected_http_status=201):
        task_request = self.factory.post(post_tasks_url, task_data)
        task_response = create_task(task_request)

        self.assertEqual(task_response.status_code, expected_http_status)

    def modify_task(self, task_data, expected_http_status=200):
        task_request = self.factory.put(f'{put_tasks_url}/{task_data.get("id")}', task_data, content_type='application/json')
        task_response = edit_task(task_request, task_data.get('id'))
        task_response.render()

        self.assertEqual(task_response.status_code, expected_http_status)

    def test_put_task(self):
        self.create_task(default_task_create)
        self.get_tasks()

        modified_task = {
            'id': 1,
            'name': 'test_task_modified',
            'category': 1,
            'deadline': '2022-10-26',
            'description': 'test description modified',
            'title': 'test_title_new'
        }

        expected_task = {
            'id': 1,
            'category': {
                'id': 1,
                'name': default_category.get('name')
            },
            'deadline': modified_task.get('deadline'),
            'description': modified_task.get('description'),
            'title': modified_task.get('title')
        }

        self.modify_task(modified_task)
        remote_task = self.get_tasks()

        self.assertJSONEqual(json.dumps(expected_task), json.dumps(remote_task))

    def test_put_task_empty_name(self):
        self.create_task(default_task_create)
        self.get_tasks()

        modified_task = {
            'id': 1,
            'name': '',
            'category': 1,
            'deadline': '2022-10-26',
            'description': 'test description modified',
            'title': 'test_title_new'
        }
        self.modify_task(modified_task, 400)


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        self.create_environment()

    def create_environment(self, category_data=None, task_data=None):
        if category_data is None:
            category_data = default_category
        if task_data is None:
            task_data = default_task_create
        self.create_category(category_data)
        self.create_task(task_data)

    def create_category(self, category_data, expected_http_status=201):
        categories_request = self.factory.post(post_category_url, category_data)
        categories_response = create_category(categories_request)

        self.assertEqual(categories_response.status_code, expected_http_status)

    def get_categories(self, expected_status_code=200):
        request = self.factory.get(get_categories_url)
        response = get_categories(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

        return json.loads(response.content.decode())

    def get_tasks(self, expected_status_code=200):
        request = self.factory.get(get_tasks_url)
        response = get_tasks(request)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)
        return json.loads(response.content.decode())[0]

    def create_task(self, task_data, expected_http_status=201):
        task_request = self.factory.post(post_tasks_url, task_data)
        task_response = create_task(task_request)

        self.assertEqual(task_response.status_code, expected_http_status)

    def delete_task(self, task_id, expected_status_code=200):
        request = self.factory.delete(f'{delete_tasks_url}/{task_id}')
        response = delete_task(request, task_id)
        response.render()

        self.assertEqual(response.status_code, expected_status_code)

    def test_delete_task(self):
        self.delete_task(1)
        self.get_tasks(expected_status_code=404)

    def test_delete_nonexistent_category_id(self):
        self.delete_task(9999, 404)

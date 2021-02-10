import json
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status


class UserTest(TestCase):
    """ Test module for Register User API """

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"name": "test", "username": "test", "password": "test", "is_editor": 'false'}
        self.user_data_is_editor = {"name": "test", "username": "test1", "password": "test", "is_editor": 'true'}

    def test_register_user_for_editor_false(self):
        url = reverse('register-user')
        self.response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_register_user_for_editor_true(self):
        url = reverse('register-user')
        self.response = self.client.post(url, self.user_data_is_editor, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_login_user_correct_credential(self):
        register_url = reverse('register-user')
        register = self.client.post(register_url, json.dumps(self.user_data), content_type="application/json")
        login_url = reverse('token_obtain_pair')
        payload = json.dumps({"username": self.user_data['username'], "password": self.user_data['password']})
        login = self.client.post(login_url, payload, content_type="application/json")
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertEqual(login.status_code, status.HTTP_200_OK)


class ArticleTest(TestCase):
    """ Test module for Article User API """

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"name": "test", "username": "test", "password": "test", "is_editor": 'false'}
        self.user_data_is_editor = {"name": "test", "username": "test1", "password": "test", "is_editor": 'true'}
        self.client.post(reverse('register-user'), json.dumps(self.user_data), content_type="application/json")
        payload = json.dumps({"username": self.user_data['username'], "password": self.user_data['password']})
        self.token = self.client.post(reverse('token_obtain_pair'), payload, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def api_authentication(self, token=None):
        token = self.token if (token is None) else token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_article(self):
        # url = '/api/v1/article/'
        url = reverse('article-list')
        data = json.dumps({"title": "Demo", "content": "test"})
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_update_article(self):
        url = reverse('article-list')
        data = json.dumps({"title": "Demo", "content": "test"})
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.article = self.client.post(url, data, content_type="application/json")
        update_data = json.dumps({"title": "Demo1", "content": "test1"})
        update_url = url + str(self.article.data['id']) + '/'
        self.update_article = self.client.patch(update_url, update_data, content_type="application/json")
        self.assertEqual(self.article.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.update_article.status_code, status.HTTP_200_OK)

    def test_article_list(self):
        create_url = reverse('article-list')
        get_url = reverse('writer-list')
        data = json.dumps({"title": "Demo", "content": "test"})
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.article = self.client.post(create_url, data, content_type="application/json")
        self.response = self.client.get(get_url, content_type="application/json")
        self.assertEqual(self.article.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


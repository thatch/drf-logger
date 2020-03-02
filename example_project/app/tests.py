from rest_framework.test import APITestCase
from rest_framework import status


class HelloAPITests(APITestCase):

    url = '/app/hello/'
    fixtures = ['db.yaml']

    def test_simple(self):
        # To output user_id.
        self.client.login(username='drf-user', password='password')

        r = self.client.get(self.url)
        self.assertTrue(status.is_success(r.status_code))


class PersonViewSetTests(APITestCase):

    url = '/app/person/'

    def test_list(self):
        r = self.client.get(self.url)
        self.assertTrue(status.is_success(r.status_code))

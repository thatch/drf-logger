from rest_framework.test import APITestCase
from rest_framework import status


class HelloAPITests(APITestCase):

    url = '/app/hello/'

    def test_simple(self):
        r = self.client.get(self.url)
        self.assertTrue(status.is_success(r.status_code))


class PersonViewSetTests(APITestCase):

    url = '/app/person/'

    def test_list(self):
        r = self.client.get(self.url)
        self.assertTrue(status.is_success(r.status_code))

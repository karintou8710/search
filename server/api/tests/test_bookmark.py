import json

from rest_framework import status
from rest_framework.test import APITestCase


class BookMarkTest(APITestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        response = self.client.post('/api/bookmark/', {'bookMarkID': 1})
        if response.status_code != status.HTTP_201_CREATED:
            raise Exception("setUp() failure")

    def test_get_bookmarks(self):
        response = self.client.get('/api/bookmark/')
        json_content = json.loads(response.content)
        self.assertEqual(json_content[0]['id'], 1)

    def test_post_invalid_string_bookMarkID(self):
        data = {
            'bookMarkID': "abc",
        }
        response = self.client.post('/api/bookmark/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [1])

    def test_post_invalid_none_bookMarkID(self):
        data = {}
        response = self.client.post('/api/bookmark/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [1])

    def test_post_valid_bookMarkID(self):
        data = {
            'bookMarkID': "2",
        }
        response = self.client.post('/api/bookmark/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [1, 2])

    def test_post_same_bookMarkID(self):
        data = {
            'bookMarkID': 1,
        }
        response = self.client.post('/api/bookmark/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [1])

    def test_all_delete_bookMarkIDs(self):
        response = self.client.delete('/api/bookmark/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [])

    def test_delete_bookMarkID(self):
        response = self.client.delete('/api/bookmark/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [])

    def test_delete_not_exist_bookMarkID(self):
        response = self.client.delete('/api/bookmark/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.session.get("bookMarkIDs"), [1])

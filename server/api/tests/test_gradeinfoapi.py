from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import GradeInfo
from api.paginations import SizePagination


class GradeInfoAPITest(APITestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        self.dataSize = len(GradeInfo.objects.all())
        self.data = {
            "subject": "プログラミング入門",
            "lecture": "テストの必要性",
            "group": "1-53組",
            "teacher": "手巣戸　大事",
            "year": "2200",
            "semester": "2学期",
            "faculty": "総合教育部",
            "numOfStudents": 1000,
            "ap": 0,
            "a": 0,
            "am": 0,
            "bp": 0,
            "b": 0,
            "bm": 0,
            "cp": 0,
            "c": 0,
            "d": 0,
            "dm": 0,
            "f": 1000,
            "gpa": 0,
        }
        self.user = User.objects.create_user(
            username='testuser', email='jaco@test.jp', password='top_secret'
        )
        self.admin = User.objects.create_superuser(
            username='supertestuser', email='jacob@test.com', password='top_secret'
        )

    def test_get(self):
        response = self.client.get('/api/gradeinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.dataSize)

    def test_post_by_anonymousUser(self):
        response = self.client.post('/api/gradeinfo/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeInfo.objects.count(), self.dataSize)

    def test_post_by_user(self):
        self.client.login(username=self.user.username, password="top_secret")
        response = self.client.post('/api/gradeinfo/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeInfo.objects.count(), self.dataSize)

    def test_post_by_admin(self):
        self.client.login(username=self.admin.username, password="top_secret")
        response = self.client.post('/api/gradeinfo/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(GradeInfo.objects.all()), self.dataSize + 1)

    def test_retrieve(self):
        response = self.client.get('/api/gradeinfo/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_put_by_anonymousUser(self):
        response = self.client.put('/api/gradeinfo/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeInfo.objects.get(pk=1).subject, "test")

    def test_put_by_user(self):
        self.client.login(username=self.user.username, password="top_secret")
        response = self.client.put('/api/gradeinfo/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeInfo.objects.get(pk=1).subject, "test")

    def test_put_by_admin(self):
        self.client.login(username=self.admin.username, password="top_secret")
        response = self.client.put('/api/gradeinfo/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GradeInfo.objects.get(pk=1).subject, "プログラミング入門")

    def test_delete_by_anonymousUser(self):
        response = self.client.delete('/api/gradeinfo/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        qs = GradeInfo.objects.filter(pk=1)
        self.assertTrue(qs.exists())

    def test_delete_by_user(self):
        self.client.login(username=self.user.username, password="top_secret")
        response = self.client.delete('/api/gradeinfo/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        qs = GradeInfo.objects.filter(pk=1)
        self.assertTrue(qs.exists())

    def test_delete_by_admin(self):
        self.client.login(username=self.admin.username, password="top_secret")
        response = self.client.delete('/api/gradeinfo/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        qs = GradeInfo.objects.filter(pk=1)
        self.assertFalse(qs.exists())

    def test_calc_num_page(self):
        inputs = [100, 101, 99]
        if settings.REST_FRAMEWORK['PAGE_SIZE'] != 10:
            raise Exception("ページサイズが変更されました。テストコードを見直す必要があります。")
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        ans = [10, 11, 10]
        res = [SizePagination.get_num_page(inp, page_size) for inp in inputs]
        self.assertEqual(res, ans)

from io import StringIO

from django.core.management import call_command
from django.test import Client, TestCase
from jsonschema.exceptions import ValidationError

from api.models import GradeInfo
from scraping.errors import SumOfStudentError

# TODO: 本番データのテストの方法


class CommandTest(TestCase):

    def setUp(self):
        self.client = Client()

    # 全てのデータが正しく読み込まれているか
    def test_loadalldata(self):
        expected = 6
        out = StringIO()  # stdoutに出力しない
        testDirPath = "scraping/testdata/normal/"
        call_command('loadalldata', stdout=out, testdir=testDirPath)
        actual = GradeInfo.objects.count()
        self.assertEqual(actual, expected)

    # 既にデータが入った状態で再度実行すると、ブックマークがリセットされないか
    # TODO: IDが変わっていないかまで調べる必要あり
    def test_not_clean_bookmark_by_loadalldata(self):
        # 一度データ登録
        out = StringIO()  # stdoutに出力しない
        testDirPath = "scraping/testdata/normal/"
        call_command('loadalldata', stdout=out, testdir=testDirPath)
        first = GradeInfo.objects.first()
        bookmarkID = str(first.id)
        data = {
            'bookMarkID': bookmarkID,
        }
        response = self.client.post("/api/bookmark/", data)
        response = self.client.get("/api/bookmark/")
        actual = len(response.json())
        expected = 1
        self.assertEqual(actual, expected)
        # もう一度呼ぶ
        testDirPath = "scraping/testdata/normal/"
        call_command('loadalldata', stdout=out, testdir=testDirPath)
        response = self.client.get("/api/bookmark/")
        actual = len(response.json())
        expected = 1
        self.assertEqual(actual, expected)

    # 誤った型のjsonフォーマットでエラーがでるか
    def test_json_validation_error(self):
        out = StringIO()  # stdoutに出力しない
        testDirPathList = [
            "scraping/testdata/json_validation_error/test1/",
            "scraping/testdata/json_validation_error/test2/",
            "scraping/testdata/json_validation_error/test3/",
            "scraping/testdata/json_validation_error/test4/",
        ]
        for testDirPath in testDirPathList:
            with self.assertRaises(ValidationError):
                call_command('loadalldata', stdout=out, testdir=testDirPath)

    # 誤った人数のデータでエラーがでるか
    def test_not_equal_number_of_people(self):
        out = StringIO()
        testDirPath = "scraping/testdata/not_equal_number_of_people/"
        with self.assertRaises(SumOfStudentError):
            call_command('loadalldata', stdout=out, testdir=testDirPath)

    # 指定したテストディレクトリが存在しなかった場合
    def test_testdir_not_found(self):
        out = StringIO()
        testDirPath = "scraping/testdata/filenotfound_test/"
        with self.assertRaises(FileNotFoundError):
            call_command('loadalldata', stdout=out, testdir=testDirPath)

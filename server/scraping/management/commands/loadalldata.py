import json
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from jsonschema import validate

from api.models import GradeInfo
from scraping.errors import SumOfStudentError
from scraping.schema.gradeSchema import gradeJsonSchema


class Command(BaseCommand):
    """スクレイピングした成績をDBに保存するコマンド
    """

    help = 'JSONファイルから保存していないデータをDBに登録します'

    def add_arguments(self, parser):
        parser.add_argument('--testdir', default="scraping/data/")  # テストディレクトリのパス

    def handle(self, *args, **options):
        dataDir = options.get("testdir")
        # 入力されたディレクトリのバリデーション
        if not os.path.isdir(dataDir):
            raise FileNotFoundError(f"{dataDir}はディレクトリへのパスではありません")

        for curDir, _, files in os.walk(dataDir):
            for filename in files:
                # 成績データが保存されたjsonファイルへのパス
                filePath = os.path.join(curDir, filename)
                self.stdout.write(f"loading {filePath}...")

                with open(filePath, 'r') as f:
                    data = json.load(f)
                    # jsonファイルが正しいフォーマットかチェックする
                    validate(instance=data, schema=gradeJsonSchema)

                    # 合計の人数と各成績の人数の和が等しいことの確認
                    self.__validate_number_of_people(data)

                    # トランザクションでアトミックな処理にする
                    with transaction.atomic():
                        self.__save_recodes_if_not_exist(data)

    def __save_recodes_if_not_exist(self, data):
        """DBに存在しない成績データを保存する

        DBのデータの重複をしないようにする。
        毎度DBのデータを削除して入れ直す案は毎回IDが異なるので却下

        Args:
            data: __validate_number_of_peopleメソッドを通った成績データ

        Returns:
            None
        """
        newGradeList = []

        # DBに接続できない、テーブルがないなどでエラーがでる可能性がある
        savedGradeData = GradeInfo.objects.all()
        for d in data:
            record = d['fields']

            if not savedGradeData.filter(**record).exists():
                newGradeList.append(GradeInfo(**record))

        GradeInfo.objects.bulk_create(newGradeList)

    def __validate_number_of_people(self, data):
        """合計の人数と各成績の人数の和が等しいことの確認

        間違いのデータが含まれていたら例外を発生する。

        Args:
            data: 規定のjsonフォーマットの成績データ

        Returns:
            None
        """
        for d in data:
            r = d['fields']
            expected = r['numOfStudents']
            actual = (
                r['ap'] + r['a'] + r['am'] + r['bp'] + r['b'] + r['bm'] +
                r['cp'] + r['c'] + r['d'] + r['dm'] + r['f']
            )
            if expected != actual:
                errorMessage = f"numOfStudents-{expected} : sum-{actual}, 合計の人数と各成績の人数の和が異なります。 {r}"
                raise SumOfStudentError(errorMessage)

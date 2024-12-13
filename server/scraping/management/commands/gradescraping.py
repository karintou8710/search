import os

import jsonstreams
from django.core.management.base import BaseCommand

from scraping import table
from scraping.encoder import EnsureAsciiFalseEncoder
from scraping.tool import GradeScraping

MODEL_NAME = 'api.gradeinfo'


class Command(BaseCommand):

    help = 'search hokudai grade and save data as json.'

    def add_arguments(self, parser):
        facultyIDs = list(table.facultyID2name.keys())
        facultyIDs.append('all')
        parser.add_argument('termID', type=str,
                            choices=table.termID2year.keys())
        parser.add_argument('facultyID', type=str, choices=facultyIDs)

    def handle(self, *args, **options):
        termID = options['termID']
        if options['facultyID'] == 'all':
            facultyIDs = table.facultyID2name.keys()
        else:
            facultyIDs = [options['facultyID']]

        for facultyID in facultyIDs:
            faculty = table.facultyID2name[facultyID]
            self.stdout.write(f'{faculty} のデータを取得します')
            self._gradeScraping(termID, facultyID)

    def _gradeScraping(self, termID, facultyID):
        dirPath = f'scraping/data/{termID}'

        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        filename = f'scraping/data/{termID}/{facultyID}.json'

        if os.path.exists(filename):
            if input('既にファイルがあります。上書きしますか？[y/n] : ') != 'y':
                return

        gs = GradeScraping(termID, facultyID)
        self.stdout.write('結果ページに接続しています...')
        gs.toResultPage()

        with jsonstreams.Stream(jsonstreams.Type.ARRAY, filename=filename,
                                indent=4, encoder=EnsureAsciiFalseEncoder) as s:
            for item in gs.getItems():
                res = {
                    'model': MODEL_NAME,
                    'fields': item,
                }

                s.write(res)

        self.stdout.write(f"error count: {len(gs.errors)}")
        gs.close()

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tqdm import tqdm

from scraping import table

# 旧GPAは未対応

HOME_URL = "https://educate.academic.hokudai.ac.jp/seiseki/GradeDistSerch.aspx"
RESULT_URL = "https://educate.academic.hokudai.ac.jp/seiseki/GradeDistResult11.aspx"


class GradeScraping:

    def __init__(self, termID, facultyID):
        options = Options()
        options.add_argument("--headless")
        options.browser_version = "stable"
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)  # seconds

        self.termID = termID
        self.facultyID = facultyID
        self.errors = []

    def toResultPage(self):
        # 00 -> 全学教育
        self.driver.get(HOME_URL)
        time.sleep(1)

        # 期間 学士課程 学部 授業科目・担当教員別
        idList = ["ddlTerm", "ddlDiv", "ddlFac", "ddlDataKind"]
        valueList = [self.termID, "02", self.facultyID, "1"]

        for selectID, value in zip(idList, valueList):
            dropdown = self.driver.find_element(By.ID, selectID)
            select = Select(dropdown)
            select.select_by_value(value)
            time.sleep(1)

        btn = self.driver.find_element(By.ID, "btnSerch")
        btn.click()  # submit
        time.sleep(1)

        # 表示件数を全てにする
        dropdown = self.driver.find_element(By.ID, "ddlLine_ddl")
        select = Select(dropdown)
        select.select_by_index(0)
        time.sleep(1)

    def getItems(self):
        if self.driver.current_url != RESULT_URL:
            raise Exception("結果ページに移動してください。")

        trs = self.driver.find_elements(By.XPATH, '//*[@id="gvResult"]/tbody/tr')
        trs = trs[2:]  # ヘッダーの余分な情報を捨てる

        def isValidRow(tr):
            tds = tr.find_elements(By.TAG_NAME, "td")
            # 空行ではない新GPAの行
            if len(tds) != 18:
                return False

            # 統計データは取得しない
            if tds[2].text in ["合計", "統計", "総計"]:
                return False

            return True

        trs = list(filter(isValidRow, trs))

        grades = ["ap", "a", "am", "bp", "b", "bm", "cp", "c", "d", "dm", "f"]
        totalSize = int(self.driver.find_element(By.ID, "lblResultCnt").text)

        # 行数が指定のものと同じかチェック2
        try:
            assert totalSize == len(trs)
        except AssertionError:
            raise ValueError(
                f"実際の成績数とカウントされた成績数が異なります: expectedSize={totalSize}, actualSize={len(trs)}"
            )

        for tr in tqdm(trs):
            item = dict()
            tds = tr.find_elements(By.TAG_NAME, "td")

            item["subject"] = tds[1].text
            item["lecture"] = tds[2].text
            item["group"] = tds[3].text
            item["teacher"] = tds[4].text.replace("　", "")
            item["year"] = table.termID2year[self.termID][0]
            item["semester"] = table.termID2year[self.termID][1] + "学期"
            item["faculty"] = table.facultyID2name[self.facultyID]
            numOfStudents = tds[5].text
            # NOTE: 正常なデータだが成績がないデータもある(２重登録？)
            if numOfStudents == " ":
                continue
            item["numOfStudents"] = int(numOfStudents)

            sumNum = 0
            try:
                for idx in range(len(grades)):
                    percent = float(tds[6 + idx].text)
                    item[grades[idx]] = round(percent * item["numOfStudents"] / 100)
                    sumNum += item[grades[idx]]
            except ValueError:  # 旧GPAはスキップ
                continue

            # 履修者数と合計が合うか確認
            try:
                assert sumNum == item["numOfStudents"]
            except AssertionError:
                self.errors.append(tr)
                continue
            item["gpa"] = float(tds[6 + len(grades)].text)
            yield item

    def close(self):
        # ブラウザーを終了
        self.driver.close()

# スクレイピングをする時の引数は下の辞書のキーを入力

# gradescrapingコマンドの引数選択に使用
termID2year = {
    '20252': ('2025', '2'),  # 2025年度 2学期
    '20251': ('2025', '1'),  # 2025年度 1学期
    '20242': ('2024', '2'),  # 2024年度 2学期
    '20241': ('2024', '1'),  # 2024年度 1学期
    '20232': ('2023', '2'),  # 2023年度 2学期
    '20231': ('2023', '1'),  # 2023年度 1学期
    '20222': ('2022', '2'),  # 2022年度 2学期
    '20221': ('2022', '1'),  # 2022年度 1学期
    '20212': ('2021', '2'),  # 2021年度 2学期
    '20211': ('2021', '1'),  # 2021年度 1学期
    '20202': ('2020', '2'),  # 2020年度 2学期
    '20201': ('2020', '1'),
    '20192': ('2019', '2'),
    '20191': ('2019', '1'),
    '20182': ('2018', '2'),
    '20181': ('2018', '1'),
    '20172': ('2017', '2'),
    '20171': ('2017', '1'),
    '20162': ('2016', '2'),
    '20161': ('2016', '1'),
}

# 公式サイトで学部に付けられているID
facultyID2name = {
    '00': '全学教育',
    '02': '総合教育部',
    '05': '文学部',
    '07': '教育学部',
    '11': '現代日本学プログラム課程',
    '15': '法学部',
    '17': '経済学部',
    '22': '理学部',
    '25': '工学部',
    '34': '農学部',
    '36': '獣医学部',
    '38': '水産学部',
    '42': '医学部',
    '43': '歯学部',
    '44': '薬学部',
}

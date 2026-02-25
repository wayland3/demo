'''
mongodb 中的数组对象转换为数组字符串
'''
import json
from pymongo import MongoClient


url = 'mongodb://michong:michong@10.0.0.36:27017/'
db_name = 'game_test'


table_pre = 'week_data_'

target_table = 'week_data'

weeks = [
    '2023_1',
    '2023_2',
    '2023_3',
    '2023_4',
    '2023_5',
    '2023_6',
    '2023_7',
    '2023_8',
    '2023_9',
    '2023_10',
    '2023_11',
    '2023_12',
    '2023_13',
    '2023_14',
    '2023_15',
    '2023_16',
    '2023_17',
    '2023_18',
    '2023_19',
    '2023_20',
    '2023_21',
    '2023_22',
    '2023_23',
    '2023_24',
    '2023_25',
    '2023_26',
    '2023_27',
    '2023_28',
    '2023_29',
    '2023_30',
    '2023_31',
    '2023_32',
    '2023_33',
    '2023_34',
    '2023_35',
    '2023_36',
    '2023_37',
    '2023_38',
    '2023_39',
    '2023_40',
    '2023_41',
    '2023_42',
    '2023_43',
    '2023_44',
    '2023_45',
    '2023_46',
    '2023_47',
    '2023_48',
    '2023_49',
    '2023_50',
    '2023_51',
    '2023_52',
    '2024_1',
    '2024_2',
    '2024_3',
    '2024_4',
    '2024_5',
    '2024_6',
    '2024_7',
    '2024_8',
    '2024_9',
    '2024_10',
    '2024_11',
    '2024_12',
    '2024_13',
    '2024_14',
    '2024_15',
    '2024_16',
    '2024_17',
]


with MongoClient(url) as client:
    # 选择数据库和集合
    db = client[db_name]

    target_collection = db[target_table]

    for i in weeks:
        collection = db[table_pre + i]

        to_insert = []
        data = collection.find()
        for d in data:
            data = {
                'playerID': d['_id'],
                'week': i,
                'upFavor': d['upFavor'],
                'rank1p3': d['rank1p3'],
                'rank1p4': d['rank1p4'],
                'yiman': d['yiManAmount'],
            }
            to_insert.append(data)

        if not to_insert:
            continue

        target_collection.insert_many(to_insert)

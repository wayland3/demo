'''
mongodb 中的数组对象转换为数组字符串
'''
import json
from pymongo import MongoClient


# url = 'mongodb://michong:michong@10.0.0.36:27017/'
url = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
db_name = 'game_test'
# db_name = 'game_pre_release'
collection_name = 'playersummaries'


def conv():
    # 创建MongoDB连接
    with MongoClient(url) as client:
        # 选择数据库和集合
        db = client[db_name]
        collection = db[collection_name]

        # 查询所有数据，每次从服务器获取100个文档
        documents = collection.find().batch_size(1000)
        for doc in documents:
            actors = doc.get('actors')

            if actors == '':
                print(doc['_id'], 'eeeeeeeeee')

            if not actors:
                continue

            if isinstance(actors[0], str):
                print(actors)


if __name__ == '__main__':
    conv()

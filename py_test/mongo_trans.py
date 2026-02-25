'''
mongodb 中的数组对象转换为数组字符串
'''
import json
from pymongo import MongoClient


url = 'mongodb://michong:michong@10.0.0.36:27017/'
url = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
db_name = 'game_test'
db_name = 'game_pre_release'
collection_name = 'playersummaries'


convert_field = ['avatars', 'emojis', 'images', 'ornaments', 'voices']


# 将数组对象转换为数组字符串
def array_object_to_array_str(v):
    if not v:
        return None

    if len(v) == 0:
        return None

    vv = v[0]
    if isinstance(vv, str):
        return None

    result = []
    for item in v:
        s = json.dumps(item)
        result.append(s)

    return result


def convert(doc):
    updated = False
    for field in convert_field:
        v = doc.get(field)
        vv = array_object_to_array_str(v)
        if vv:
            doc[field] = vv
            updated = True
    return updated


def update(docs):
    to_update = []

    # 遍历所有数据
    for doc in docs:
        if convert(doc):
            to_update.append(doc)
    return to_update


def conv():
    # 创建MongoDB连接
    with MongoClient(url) as client:
        # 选择数据库和集合
        db = client[db_name]
        collection = db[collection_name]

        # 查询所有数据，每次从服务器获取100个文档
        documents = collection.find().batch_size(1000)
        to_update = update(documents)
        # 更新数据
        for doc in to_update:
            _id = doc['_id']
            collection.update_one(
                {'_id': _id},  # 查询条件
                # 更新操作
                {'$set': {
                    'avatars': doc.get('avatars'),
                    'emojis': doc.get('emojis'),
                    'images': doc.get('images'),
                    'ornaments': doc.get('ornaments'),
                    'voices': doc.get('voices')
                }
                }
            )


if __name__ == '__main__':
    conv()

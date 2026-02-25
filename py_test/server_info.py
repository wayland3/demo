'''
mongodb 中的数组对象转换为数组字符串
'''
import json
from pymongo import MongoClient
from bson import ObjectId


url = 'mongodb://root:root@10.0.0.181:27017/'
db_name = 'zinnor'
collection_name = 'server_status'


l = ['golang-test',
     'golang-qa',
     'go-dev',
     'go预发布',
     '策划_1',
     '策划_2',
     '日本正式服',
     '日本提审服',
     'yanghao',
     'wanglei',
     'wyz',
     'sdc',
     '开发服',
     '测试服',
     'QA 服',
     '预发布环境']

s = '660bd6b6d63803028cb4b0a4'


def conv():
    # 创建MongoDB连接
    with MongoClient(url) as client:
        # 选择数据库和集合
        db = client[db_name]
        collection = db[collection_name]

        # 查询所有数据，每次从服务器获取100个文档
        documents = collection.find().batch_size(1000)

        m = {}
        for doc in documents:
            m[doc.get('name')] = doc

        for name in l:
            d = m[name]
            oid = ObjectId()
            d['_id'] = oid
            collection.insert_one(d)


if __name__ == '__main__':
    conv()

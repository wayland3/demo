<<<<<<< HEAD
'''
把活动从一个mongo库转移到另一个mongo库
'''

import json

from pymongo import MongoClient

GO_DEV = 'mongodb://michong:michong@10.0.0.36:27017/'
GO_TEST_INT_PRE = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
JAVA_DEV_TEST = 'mongodb://root:root@10.0.0.181/'

GO_GAME_TEST = 'game_test'
GO_GAME_INTERNAL = 'game_internal_test'
GO_GAME_PRE = 'game_pre_release'
JAVA_GAME_DEV = 'game_dev'
JAVA_GAME_TEST = 'game_test'


SRC_URL = JAVA_DEV_TEST
SRC_DB_NAME = JAVA_GAME_DEV
TGT_URL = GO_TEST_INT_PRE
TGT_DB_NAME = GO_GAME_INTERNAL
COLLECTION_NAME = 'activity_data'


def conv():
    src = None
    with MongoClient(SRC_URL) as client:
        # 选择数据库和集合
        db = client[SRC_DB_NAME]
        collection = db[COLLECTION_NAME]

        src = collection.find_one({'_id': 171})

    if src is None:
        print('no such activity')
        return

    with MongoClient(TGT_URL) as client:
        db = client[TGT_DB_NAME]
        collection = db[COLLECTION_NAME]

        # src['_id'] = 5
        collection.insert_one(src)


if __name__ == '__main__':
    conv()
=======
'''
把活动从一个mongo库转移到另一个mongo库
'''

from pymongo import MongoClient

GO_DEV = 'mongodb://michong:michong@10.0.0.36:27017/'
GO_TEST_INT_PRE = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
JAVA_DEV_TEST = 'mongodb://root:root@10.0.0.181/'
SYNC = 'mongodb://admin:Mahjong2021@172.31.11.159/'

GO_GAME_TEST_DB = 'game_test'
GO_GAME_INTERNAL_DB = 'game_qa'
GO_GAME_PRE_DB = 'game_pre_release'
SYNC_DB = 'game'
JAVA_GAME_DEV_DB = 'game_dev'
JAVA_GAME_TEST_DB = 'game_test'


SRC_URL = GO_TEST_INT_PRE
SRC_DB_NAME = GO_GAME_INTERNAL_DB
TGT_URL = GO_DEV
TGT_DB_NAME = GO_GAME_TEST_DB
COLLECTION_NAME = 'activity_data'


def conv():
    src = None
    with MongoClient(SRC_URL) as client:
        # 选择数据库和集合
        db = client[SRC_DB_NAME]
        collection = db[COLLECTION_NAME]

        src = collection.find_one({'_id': 187})

    if src is None:
        print('no such activity')
        return

    with MongoClient(TGT_URL) as client:
        db = client[TGT_DB_NAME]
        collection = db[COLLECTION_NAME]

        src['_id'] = 187
        collection.insert_one(src)


def conv_all():
    src = None
    with MongoClient(SRC_URL) as client:
        # 选择数据库和集合
        db = client[SRC_DB_NAME]
        collection = db[COLLECTION_NAME]

        src = list(collection.find())

    if src is None:
        print('no such activity')
        return

    with MongoClient(TGT_URL) as client:
        db = client[TGT_DB_NAME]
        collection = db[COLLECTION_NAME]

        collection.insert_many(src)


if __name__ == '__main__':
    conv()
>>>>>>> 7f4cda1c81984a42ed067bc57052f4b85c8af826

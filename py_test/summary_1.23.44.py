import json
from multiprocessing import Pool
# from concurrent.futures import ThreadPoolExecutor
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField

from pymongo import MongoClient

GO_DEV = 'mongodb://mahjong:Mahjong#2021@10.0.1.54:27017/'
GO_GAME_TEST = 'game_internal_test'
COLLECTION_NAME = 'playersummaries'
BOT_COLLECTION_NAME = 'botSummaries'

HOST = '10.0.1.50'
USER = 'mahjong'
PASSWORD = 'Mahjong#2021'
DB = 'game_internal_test'
CHARSET = 'utf8mb4'

# HOST = '10.0.1.50'
# USER = 'mahjong'
# PASSWORD = 'Mahjong#2021'
# DB = 'game_dev'
# CHARSET = 'utf8mb4'


# 定义数据库连接
db = MySQLDatabase(DB, user=USER,
                   password=PASSWORD, host=HOST, port=3306)


# 定义模型
class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    database_id = PrimaryKeyField()
    inventory = CharField()


client = MongoClient(GO_DEV)
db = client[GO_GAME_TEST]
collection = db[COLLECTION_NAME]
bot_collection = db[BOT_COLLECTION_NAME]


def update_data(item):
    try:
        print(f"Starting update for item {item.database_id}")
        im = json.loads(item.inventory)
        title = im.get('11')
        if not title:
            return

        ts = []
        for t in title:
            if not t:
                continue
            m = {}
            if t.get('1') == '':
                continue

            m['1'] = t.get('1')
            if t.get('2'):
                m['2'] = t.get('2')
            else:
                m['2'] = 1

            if t.get('5'):
                m['5'] = t.get('5')

            s = json.dumps(m)
            ts.append(s)

    except Exception as e:
        print('parse: ', e)

    try:
        collection.update_one({'_id': item.database_id}, {
            '$set': {'appellations': ts}
        })
        bot_collection.update_one({'playerID': item.database_id}, {
            '$set': {'appellations': ts}
        })
    except Exception as e:
        print('save: ', e)
    print(f"Finished update for item {item.database_id}")


# 创建线程池
with Pool(processes=1) as pool:
    start_id = 0
    page_size = 2000
    query_times = 1

    while True:
        # 使用 paginate 方法来分页查询数据
        query = Character.select().where(Character.database_id > start_id).order_by(
            Character.database_id).limit(page_size)

        i = 0
        for q in query:
            i += 1
            start_id = q.database_id

            if not q.inventory:
                continue
            pool.apply_async(update_data, (q,))

        print(f'第{query_times}次查询到 {i} 条\n')
        query_times += 1
        if i < page_size:
            break

print("summary update finish")
collection.update_many({'appellations': {'$exists': False}}, {'$set': {'appellations': []}})
print("summary [] update finish")
bot_collection.update_many({'appellations': {'$exists': False}}, {'$set': {'appellations': []}})
print("bot summary update finish")

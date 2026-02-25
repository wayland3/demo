import json
from multiprocessing import Pool
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField

from pymongo import MongoClient

GO_DEV = 'mongodb://michong:michong@10.0.0.36:27017/'
GO_GAME_TEST = 'game_test'
COLLECTION_NAME = 'playersummaries'

HOST = '10.0.0.241'
USER = 'michong'
PASSWORD = 'michong'
DB = 'mahjong_game_test'
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
    misc = CharField()


client = MongoClient(GO_DEV)
db = client[GO_GAME_TEST]
collection = db[COLLECTION_NAME]


def update_data(item):
    try:
        m = json.loads(item.inventory)
        title = m.get('11')
        if not title:
            return

        ts = []
        for t in title:
            if not t:
                continue
            if t.get('1') == '':
                continue
            if t.get('2'):
                ts.append(f'{t.get('1')},{t.get('2')}')
            else:
                ts.append(f'{t.get('1')},1')

    except Exception as e:
        print('parse: ', e)

    try:
        collection.update_one({'_id': item.database_id}, {
            '$set': {'appellations': ts}
        })
    except Exception as e:
        print('save: ', e)


def trans():
    # 批量查询所有数据
    query = Character.select()
    pool = Pool(processes=3)

    start_id = 0
    page_size = 2000

    query_times = 1
    while True:
        # 使用 paginate 方法来分页查询数据
        query = Character.select().where(Character.database_id > start_id).order_by(
            Character.database_id).limit(page_size)

        i = 0
        for item in query:
            i += 1
            start_id = item.database_id

            if not item.inventory:
                continue
            pool.apply_async(update_data, (item,))

        print(f'第{query_times}次查询到 {i} 条\n')
        query_times += 1
        if i < page_size:
            break

    pool.close()
    pool.join()


if __name__ == '__main__':
    trans()

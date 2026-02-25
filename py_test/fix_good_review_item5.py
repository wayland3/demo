import json
import pandas as pd
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, TimeField, IntegerField

from pymongo import MongoClient
import redis


HOST = '10.0.0.241'
USER = 'michong'
PASSWORD = 'michong'
DB = 'mahjong_game_test'
CHARSET = 'utf8mb4'


REDIS_HOST = '10.0.0.32'  # redis的ip
CLUSTER = 61


# HOST = '10.0.1.50'
# USER = 'mahjong'
# PASSWORD = 'Mahjong#2021'
# DB = 'game_pre_release'
# CHARSET = 'utf8mb4'


change = {2682731: 1372, 9159929: 1782, 8190427: 669, 10152058: 150, 9488303: 6, 11159664: 653, 9775795: 34,
          618378: 148, 3532786: 97, 3235219: 52, 7458364: 61, 3134607: 2, 8479688: 27, 8346733: 21, 3431120: 5, 7104110: 4}


# 定义数据库连接
db = MySQLDatabase(DB, user=USER,
                   password=PASSWORD, host=HOST, port=3306)


# 定义模型
class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    database_id = PrimaryKeyField()
    last_login = TimeField()
    last_logout = TimeField()
    inventory = CharField()


r = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def update_data(item):
    try:
        m = json.loads(item.inventory)
        items = m.get('1', [])

        i = -1
        remove = False
        for v in items:
            i += 1
            if v.get('1', '') != 'lottery':
                continue
            count = v.get('2', 1)
            count -= change[item.database_id]
            count = max(count, 0)
            if count == 0:
                remove = True
            v['2'] = count
            break

        if remove:
            items.pop(i)
        m['1'] = items

        Character.update(inventory=json.dumps(m)).where(Character.database_id == item.database_id).execute()

        r.delete(f'character:{CLUSTER}:{item.database_id}')

    except Exception as e:
        print('parse: ', e)


def trans():
    ids = list(change.keys())
    query = Character.select().where(Character.database_id.in_(ids)).execute()

    updated = []
    for item in query:
        if item.last_login < item.last_logout:
            updated.append(item)

    for item in updated:
        print(f'updated: {item.database_id}')
        update_data(item)

    for item in updated:
        change.pop(item.database_id)
    print('left: ', list(change.keys()))


if __name__ == '__main__':
    trans()

    # result = {}
    # df = pd.read_excel('11.xlsx', header=None,)
    # for index, row in df.iterrows():
    #     item = {}
    #     pid = int(df.iloc[index, 0])
    #     lottery = int(df.iloc[index, 7])
    #     if lottery == 0:
    #         continue
    #     result[pid] = lottery
    # print(result, len(result))

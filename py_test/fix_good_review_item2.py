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


HOST = '10.0.1.50'
USER = 'mahjong'
PASSWORD = 'Mahjong#2021'
DB = 'game_pre_release'
CHARSET = 'utf8mb4'


# change = {
#     10178: {'cloth': 1782, 'token': 9694},
#     853478: {'cloth': 669, 'token': 21531}
# }

change = {2682731: 33278, 9159929: 35756, 8190427: 17889, 10152058: 12904, 9488303: 8510, 9775795: 9135, 384552: 8030, 7458364: 1910, 3047809: 625, 10754799: 1521, 2833045: 20,
          5997368: 92, 7061586: 359, 6246563: 730, 6542445: -1549, 4717061: 130, 3431120: 150, 4779587: -370, 11910049: -1703, 6003835: 119, 7104110: 90, 4557722: 60, 2699296: 24}

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
    token = IntegerField()


r = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def update_data(item):
    try:
        token = item.token-change[item.database_id]
        token = max(token, 0)

        m = json.loads(item.inventory)
        m['8'] = token

        Character.update(inventory=json.dumps(m), token=token).where(Character.database_id == item.database_id).execute()

        r.delete(f'character:{CLUSTER}:{item.database_id}')

    except Exception as e:
        print('parse: ', e)


def trans():
    ids = list(change.keys())

    print(ids)

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
    # df = pd.read_excel('22.xlsx', header=None,)
    # for index, row in df.iterrows():
    #     item = {}
    #     pid = int(df.iloc[index, 0])
    #     token = int(df.iloc[index, 12])
    #     if token == 0:
    #         continue
    #     result[pid] = token
    # print(result, len(result))

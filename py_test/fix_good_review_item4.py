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


ids = [2833045, 3134607, 3235219, 4779587, 9159929, 9180719, 9488303, 9775795]

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
    cloth = IntegerField()
    # token = IntegerField()


r = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def update_data(item):
    try:
        m = json.loads(item.inventory)
        m['10'] = item.cloth

        Character.update(inventory=json.dumps(m)).where(Character.database_id == item.database_id).execute()

        r.delete(f'character:{CLUSTER}:{item.database_id}')

    except Exception as e:
        print('parse: ', e)


def trans():

    query = Character.select().where(Character.database_id.in_(ids)).execute()

    updated = []
    for item in query:
        if item.last_login < item.last_logout:
            updated.append(item)

    for item in updated:
        print(f'updated: {item.database_id}')
        update_data(item)


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

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

change = {2682731: {'cloth': 1372, 'token': 12232}, 9159929: {'cloth': 1782, 'token': 9694}, 8190427: {'cloth': 669, 'token': 21531}, 10152058: {'cloth': 150, 'token': 12026}, 9488303: {'cloth': 6, 'token': 10660}, 11159664: {'cloth': 653, 'token': 17216}, 9775795: {'cloth': 34, 'token': 7785}, 384552: {'cloth': 0, 'token': 5290}, 618378: {'cloth': 148, 'token': 6761}, 3532786: {'cloth': 97, 'token': 4515}, 10574933: {'cloth': 0, 'token': 3246}, 9180719: {'cloth': 0, 'token': 64}, 3235219: {'cloth': 52, 'token': 3039}, 11964170: {'cloth': 0, 'token': 99}, 7458364: {'cloth': 61, 'token': 490}, 5131074: {'cloth': 0, 'token': 415}, 3134607: {
    'cloth': 2, 'token': 290}, 3047809: {'cloth': 0, 'token': 1325}, 10754799: {'cloth': 0, 'token': 159}, 8479688: {'cloth': 27, 'token': 890}, 2833045: {'cloth': 0, 'token': 1210}, 5997368: {'cloth': 0, 'token': 1108}, 7061586: {'cloth': 0, 'token': 511}, 6246563: {'cloth': 0, 'token': 80}, 6542445: {'cloth': 0, 'token': 2179}, 8346733: {'cloth': 21, 'token': 130}, 4717061: {'cloth': 0, 'token': 260}, 3431120: {'cloth': 5, 'token': 120}, 4779587: {'cloth': 0, 'token': 580}, 11910049: {'cloth': 0, 'token': 1853}, 6003835: {'cloth': 0, 'token': 31}, 7104110: {'cloth': 4, 'token': 30}, 4557722: {'cloth': 0, 'token': 30}, 2699296: {'cloth': 0, 'token': 66}}

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
        token = item.token-change[item.database_id]['token']
        token = max(token, 0)

        m = json.loads(item.inventory)
        m['8'] = token

        exists_cloth = m.get('10')
        if exists_cloth:
            cloth = exists_cloth-change[item.database_id]['cloth']
            cloth = max(cloth, 0)
            m['10'] = cloth

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
    # df = pd.read_excel('11.xlsx', header=None,)
    # for index, row in df.iterrows():
    #     item = {}
    #     pid = int(df.iloc[index, 0])
    #     cloth = int(df.iloc[index, 7])
    #     token = int(df.iloc[index, 11])
    #     result[pid] = {'cloth': cloth, 'token': token}
    # print(result)

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


HOST = '172.31.11.159'
USER = 'wanglei'
PASSWORD = 'z($Zp4568n3'
DB = 'game'
CHARSET = 'utf8mb4'


ids = [2682731, 9159929, 8190427, 10152058, 9488303, 11159664, 9775795, 384552, 618378, 3532786, 10574933, 9180719, 3235219, 11964170, 7458364, 5131074, 3134607,
       3047809, 10754799, 8479688, 2833045, 5997368, 7061586, 6246563, 6542445, 8346733, 4717061, 3431120, 4779587, 11910049, 6003835, 7104110, 4557722, 2699296]

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


def trans():

    query = Character.select().where(Character.database_id.in_(ids)).execute()

    data = {}
    for item in query:
        m = json.loads(item.inventory)
        clo = m.get('10', 0)
        if clo > 0:
            data[item.database_id] = clo

    print(data)


[2833045, 3134607, 3235219, 4779587, 9159929, 9180719, 9488303, 9775795]


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

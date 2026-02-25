import json
import pandas as pd
from multiprocessing import Pool
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, TimeField, IntegerField

from pymongo import MongoClient
import redis
import time


HOST = '10.0.0.241'
USER = 'michong'
PASSWORD = 'michong'
DB = 'mahjong_game_test'
CHARSET = 'utf8mb4'


HOST = '10.0.1.50'
USER = 'mahjong'
PASSWORD = 'Mahjong#2021'
DB = 'game_pre_release'
CHARSET = 'utf8mb4'


# 定义数据库连接
db = MySQLDatabase(DB, user=USER,
                   password=PASSWORD, host=HOST, port=3306)


# ts = int(time.time())*1000
ts = 1709524800000


# 定义模型


class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    database_id = PrimaryKeyField()
    misc = CharField()


def update_data(item):
    try:
        m = json.loads(item.misc)
        activity = m.get('21')
        if not activity:
            return

        activities = activity.get('1')
        if not activities:
            return

        for a in activities:
            if not a:
                continue
            if a.get('0') != 'discordActivity':
                continue
            join_time = a.get('10')
            if not join_time:
                continue

            if join_time > ts and a.get('11'):
                print(item.database_id, join_time)

    except Exception as e:
        print('parse: ', e)


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

            if not item.misc:
                continue
            pool.apply_async(update_data, (item,))

        # print(f'第{query_times}次查询到 {i} 条\n')
        query_times += 1
        if i < page_size:
            break

    pool.close()
    pool.join()
    print('done')


if __name__ == '__main__':
    trans()

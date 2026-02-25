import time
from datetime import datetime
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, BigIntegerField, IntegerField, DoubleField, TimestampField, DateTimeField
from multiprocessing import Pool
import json
import redis

r_host = 'mahjong-java-dev-slb.redis'
cluster = 60

# host = '172.16.1.35'
# cluster = 1

host = '10.0.1.50'
user = 'mahjong'
password = 'Mahjong#2021'
db = 'game_test'
charset = 'utf8mb4'

# host = '172.16.1.208'
# user = 'mahjong'
# password = 'Mahjong2022'
# db = 'game'
# charset = 'utf8mb4'


# 创建 Redis 连接
r = redis.Redis(host=r_host, port=6379, db=0)

prefix = f'character:{cluster}:'

# 定义数据库连接
database = MySQLDatabase(db, user=user, password=password, host=host, port=3306)


# 定义模型
class BaseModel(Model):
    class Meta:
        database = database
# 定义模型


class Actor(BaseModel):
    database_id = PrimaryKeyField()
    appearance = CharField()

    class Meta:
        db_table = 'actor'


l = [
    (461101, 9367286),
    (762865, 5808472),
    (806619, 5808472),
    (829073, 5740250),
    (829170, 5405641),
    (829209, 4217513),
    (829401, 9105149),
    (833769, 10312214),
    (833896, 10312214),
]


def fix():
    for d in l:
        a = Actor.get_or_none(Actor.database_id == d[0])
        if not a:
            print(f"未找到 database_id={d[0]} 的数据")
            continue

        appearance = json.loads(a.appearance)
        two = appearance.get("2", {})
        if not two:
            print(f"未找到 appearance 中的 '2' 键，database_id={d}[0]")
            continue

        new_two = {}
        for pf, state in two.items():
            pf = pf[2:]
            state = state[2:]

            if pf in state:
                new_two[pf] = state

        appearance["2"] = new_two
        a.appearance = json.dumps(appearance)
        try:
            a.save()
        except Exception as e:
            print(f"保存数据失败: {e}")
            continue

        key = f'{prefix}{d[1]}'
        r.delete(key)

    time.sleep(300)  # 300秒 = 5分钟
    completed = []
    for d in l:
        key = f'{prefix}{d[1]}'
        if not r.exists(key):
            completed.append(d)

    for c in completed:
        l.remove(c)


if __name__ == '__main__':
    while len(l) > 0:
        fix()
        print("remain", l)
    print("所有数据已处理完成")

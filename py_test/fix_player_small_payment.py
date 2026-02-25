import time
from datetime import datetime
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, BigIntegerField, IntegerField, DoubleField, TimestampField, DateTimeField
from multiprocessing import Pool
import json
import redis

# r_host = 'mahjong-java-dev-slb.redis'
# cluster = 60

r_host = '172.16.1.35'
cluster = 1

# host = '10.0.1.50'
# user = 'mahjong'
# password = 'Mahjong#2021'
# db = 'game_test'
# charset = 'utf8mb4'

host = '172.16.1.208'
user = 'mahjong'
password = 'Mahjong2022'
db = 'game'
charset = 'utf8mb4'


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


class Character(BaseModel):
    database_id = PrimaryKeyField()
    misc = CharField()
    last_login = DateTimeField()

    class Meta:
        db_table = 'character'


ts77 = 1751868000000

l = [
    493730,
    2222283,
    2604871,
    2651192,
    2872771,
    3056566,
    3470017,
    3852935,
    4223758,
    4940192,
    5093742,
    5671370,
    5736662,
    5838127,
    6220241,
    7580194,
    7957000,
    7962300,
    8131919,
    8363332,
    8743927,
    9243737,
    9284648,
    9821612,
    9887010,
    10058026,
    10312296,
    10419912,
    11080316,
    11548019,
    11603066,
    11703996,
]


def get_misc(misc):
    try:
        m = json.loads(misc)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

    misc14 = m.get("14", {})
    if misc14:
        misc14['productIDs'] = []
        misc14['firstChargeFlag'] = False
        m[14] = misc14

    misc21 = m.get("21", {})
    if misc21:
        activity = misc21.get("1", [])
        for item in activity:
            if item.get("0") == "small_payment_model_519":
                shop = item.get("2", {})
                new_shop = {}
                for k, v in shop.items():
                    v['count'] = 0
                    new_shop[k] = v
                item["2"] = new_shop
                break

    m["21"] = {"1": activity}
    return json.dumps(m)


def fix():
    completed = []
    for v in l:
        c = Character.get_or_none(Character.database_id == v)
        if not c:
            print(f"未找到 database_id={v} 的数据")
            continue

        if c.last_login.timestamp() == ts77 / 1000:
            completed.append(v)
            continue

        misc = get_misc(c.misc)

        if misc:
            c.misc = misc
        c.last_login = datetime.fromtimestamp(ts77 / 1000)  # ts77 为毫秒级时间戳

        try:
            c.save()
        except Exception as e:
            print(f"保存新角色数据失败: {e}")
            continue

        key = f'{prefix}{v}'
        r.delete(key)

    for v in completed:
        l.remove(v)


if __name__ == '__main__':
    while True:
        fix()
        print("remain", l)
        if len(l) == 0:
            print("所有数据已处理完成")
            break

        time.sleep(300)  # 300秒 = 5分钟

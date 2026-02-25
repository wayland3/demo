import time
from datetime import datetime
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, BigIntegerField, IntegerField, DoubleField, TimestampField, DateTimeField
from multiprocessing import Pool
import json
import redis

# host = 'mahjong-java-dev-slb.redis'
# cluster = 60

host = '172.16.1.35'
cluster = 1

o_host = '172.31.11.159'
o_user = 'root'
o_password = 'Mahjong2021'
o_db = 'game_sync'
o_charset = 'utf8mb4'

n_host = '172.16.1.208'
n_user = 'mahjong'
n_password = 'Mahjong2022'
n_db = 'game'
n_charset = 'utf8mb4'
# n_host = '172.31.11.159'
# n_user = 'root'
# n_password = 'Mahjong2021'
# n_db = 'game_sync'
# n_charset = 'utf8mb4'

# 创建 Redis 连接
r = redis.Redis(host=host, port=6379, db=0)

prefix = f'character:{cluster}:'

# 定义数据库连接
old_db = MySQLDatabase(o_db, user=o_user,
                       password=o_password, host=o_host, port=3306)

new_db = MySQLDatabase(n_db, user=n_user,
                       password=n_password, host=n_host, port=3306)


# 定义模型
class OldBaseModel(Model):
    class Meta:
        database = old_db
# 定义模型


class NewBaseModel(Model):
    class Meta:
        database = new_db


class OldCharacter(OldBaseModel):
    database_id = PrimaryKeyField()
    actor = IntegerField()
    head = CharField()
    avatar = CharField()
    cumulative_recharge = DoubleField()
    coin = IntegerField()
    diamond = IntegerField()
    token = IntegerField()
    inventory = CharField()
    mailbox = CharField()
    misc = CharField()
    gossip = CharField()
    cloth = IntegerField()
    achievements = CharField()
    title_level = IntegerField()

    class Meta:
        db_table = 'character_source'


class NewCharacter(NewBaseModel):
    database_id = PrimaryKeyField()
    actor = IntegerField()
    head = CharField()
    avatar = CharField()
    cumulative_recharge = DoubleField()
    coin = IntegerField()
    diamond = IntegerField()
    token = IntegerField()
    inventory = CharField()
    mailbox = CharField()
    misc = CharField()
    gossip = CharField()
    cloth = IntegerField()
    achievements = CharField()
    title_level = IntegerField()
    last_login = DateTimeField()

    class Meta:
        db_table = 'character'


class NewActor(NewBaseModel):
    database_id = PrimaryKeyField()
    parent_id = BigIntegerField()
    created = BigIntegerField()
    avatar = CharField()
    favor = IntegerField()
    favor_level = IntegerField()
    enable_favor_ex = IntegerField()
    story = CharField()
    appearance = CharField()
    read_story = CharField()
    sms = CharField()
    enable_favor_time = BigIntegerField()

    class Meta:
        db_table = 'actor'


class OldActor(OldBaseModel):
    database_id = PrimaryKeyField()
    parent_id = BigIntegerField()
    created = BigIntegerField()
    avatar = CharField()
    favor = IntegerField()
    favor_level = IntegerField()
    enable_favor_ex = IntegerField()
    story = CharField()
    appearance = CharField()
    read_story = CharField()
    sms = CharField()
    enable_favor_time = BigIntegerField()

    class Meta:
        db_table = 'actor_source'


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


def get_misc(nc_misc, oc_misc):
    try:
        nc = json.loads(nc_misc)
        oc = json.loads(oc_misc)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None
    misc10 = nc.get("10", None)
    misc11 = nc.get("11", None)
    misc20 = nc.get("20", None)
    misc30 = nc.get("30", None)

    if misc10:
        oc["10"] = misc10
    if misc11:
        oc["11"] = misc11
    if misc20:
        oc["20"] = misc20
    if misc30:
        oc["30"] = misc30

    recharge = ''
    monthly = ''
    rookies = ''
    lottery = ''
    limit493 = ''
    limit471 = ''
    limit84 = ''

    o_misc21 = oc.get("21", {})
    if o_misc21:
        activity = o_misc21.get("1", [])
        for item in activity:
            if item.get("0") == "recharge_model_499":
                recharge = item
            if item.get("0") == "MonthlyCardActivities":
                monthly = item
            if item.get("0") == "rookiesMonthlyActivities":
                rookies = item
            if item.get("0") == "lottery_avatar_model_492":
                lottery = item
            if item.get("0") == "limitRecharge_model_493":
                limit493 = item
            if item.get("0") == "limitAvatar_model_471":
                limit471 = item
            if item.get("0") == "limitAvatar_model_84":
                limit84 = item

    activity_list = []
    n_misc21 = nc.get("21", {})
    if n_misc21:
        n_activity = n_misc21.get("1", [])
        remove_index = []

        for i, item in enumerate(n_activity):
            if item.get("0") == "recharge_model_499" and recharge:
                remove_index.append(i)
            if item.get("0") == "MonthlyCardActivities" and monthly:
                remove_index.append(i)
            if item.get("0") == "rookiesMonthlyActivities" and rookies:
                remove_index.append(i)
            if item.get("0") == "lottery_avatar_model_492" and lottery:
                remove_index.append(i)
            if item.get("0") == "limitRecharge_model_493" and limit493:
                remove_index.append(i)
            if item.get("0") == "limitAvatar_model_471" and limit471:
                remove_index.append(i)
            if item.get("0") == "limitAvatar_model_84" and limit84:
                remove_index.append(i)

        for v in sorted(remove_index, reverse=True):
            n_activity.pop(v)

        if recharge:
            n_activity.append(recharge)
        if monthly:
            n_activity.append(monthly)
        if rookies:
            n_activity.append(rookies)
        if lottery:
            n_activity.append(lottery)
        if limit493:
            n_activity.append(limit493)
        if limit471:
            n_activity.append(limit471)
        if limit84:
            n_activity.append(limit84)
        activity_list = n_activity

    if activity_list:
        oc["21"] = {"1": activity_list}
    return json.dumps(oc)


def fix():
    completed = []
    for v in l:
        nc = NewCharacter.get_or_none(NewCharacter.database_id == v)
        if not nc:
            print(f"未找到 database_id={v} 的数据")
            continue

        if nc.last_login.timestamp() == ts77 / 1000:
            completed.append(v)
            continue

        oc = OldCharacter.get_or_none(OldCharacter.database_id == v)
        if not oc:
            print(f"未找到旧数据 database_id={v} 的数据")
            continue

        misc = get_misc(nc.misc, oc.misc)

        if misc:
            nc.misc = misc
        nc.actor = oc.actor
        nc.head = oc.head
        nc.avatar = oc.avatar
        nc.cumulative_recharge = oc.cumulative_recharge
        nc.coin = oc.coin
        nc.diamond = oc.diamond
        nc.token = oc.token
        nc.inventory = oc.inventory
        nc.mailbox = oc.mailbox
        nc.cloth = oc.cloth
        nc.achievements = oc.achievements
        nc.title_level = oc.title_level
        nc.last_login = datetime.fromtimestamp(ts77 / 1000)  # ts77 为毫秒级时间戳

        try:
            nc.save()
        except Exception as e:
            print(f"保存新角色数据失败: {e}")
            continue

        NewActor.delete().where(
            (NewActor.parent_id == v) & (NewActor.created > ts77)
        ).execute()

        n_a_query = list(NewActor.select().where(NewActor.parent_id == v))
        o_a_query = list(OldActor.select().where(OldActor.parent_id == v))

        for na in n_a_query:
            for oa in o_a_query:
                if na.database_id == oa.database_id:
                    na.avatar = oa.avatar
                    na.favor = oa.favor
                    na.favor_level = oa.favor_level
                    na.enable_favor_ex = oa.enable_favor_ex
                    na.story = oa.story
                    na.appearance = oa.appearance
                    na.read_story = oa.read_story
                    na.sms = oa.sms
                    na.enable_favor_time = oa.enable_favor_time

                    try:
                        na.save()
                    except Exception as e:
                        print(f"保存新演员数据失败: {e}")
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

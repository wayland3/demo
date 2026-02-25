from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField
from typing import Iterable
import json

checkList = [
    9885498,
    6549392,
    11223923,
    4348042,
    7612900,
    9367286,
    9821612,
    11080316,
    5509252,
    2604871,
    6020056,
    6885967,
    3105982,
    11376880,
    5808472,
    4573240,
    8147966,
    7186189,
    4587379,
    4140303,
    7193306,
    2941977,
    2922984,
    10020674,
    5105603,
    7765239,
    9180351,
    9651109,
    5825889,
    7569834,
    2598096,
    7293376,
    10390257,
    10761272,
    10367092,
    5938656,
    7433048,
    3138556,
    5923074,
    4566627,
    10389156,
    7326407,
    11045603,
    5876253,
]

checkList = [
    11201448,
    2359712,
    11045603,
    11436797,
    10367092,
    4348042,
    7876306,
    5923074,

]

checkList = [
    11436797,
    11045603,
    9752265,
    4348042,
    9575146,
    5923074,
    7451182,
    10471831,
    10390257,
    9715291,
    10367092,

]

checkList = [
    11045603,
    11436797,
    4348042,
    9651109,
    10367092,
    5923074,
    9575146,
    10390257,
    7451182,
    10471831,
    9759281,
    9752265,
    9715291,
    2604871,
]

checkList = [
    7661722,
    3255948,
    5856485,
    4223758,
    11703996,
    8570932,
    5970935,

]

checkList = [
    2999652,
    7661722,
    8570932,
    11703996,
    9284648,
    9651109,
    3255948,
    5856485,
    4223758,
    5970935,
]

checkList = [
    2722296,
    9651109,
    9651109,
    9284648,
    10144449,
    11703996,
    11703996,
    11703996,
    11703996,
    8093362,
    8093362,
    2722296,
    5997271,
    4160670,
    11045603,
    3722461,

]

checkList = [
    3722461,
    2722296,
    5997271,
    4160670,
    2651192,
    2651192,
    2651192,
    2651192,
    2651192,
    5211135,
    10144449,
    7790887,
    5473766,

]
checkList = [
    4035741,
    4035741,
    2222283,
    9243737,
    5718764,
    2222283,
    5808472,
    10390257,
    3892321,
    8013093,
    10494305,
    7175574,
    7175574,
    7557612,
    2722296,
    5473766,
    10312214,
    10312214,
    7790887,
    8115872,
    11546043,
    11546043,
    11546043,
    11201448,
    2872771,
    2872771,
    2872771,
    2872771,
    10312214,
    10312214,
    10312214,
    10312214,
    11823216,
]

checkList = [
    4035741,
    8724585,
    7569834,
    3892321,
    7175574,
    7254327,
    2722296,
    5473766,
    2758517,
    8115872,
    8146925,
    11546043,
    9105149,
    9367286,
    4573986,
    11823216,
    7290137,
    7652612,
    5407068,
    10291125,
    7539235,
    10534007,
    5923074,
    2066099,
    2872771,
    8795091,
    3056566,
    3722461,
    7790887,
    9306818,
    9887010,
    4999457,
    6247915,
    9035815,
    4896772,
    5247720,
    4816417,
    9002181,
    3987503,
    11502404,
    8743927,
]

# checkList = [
#     8758427,
#     3039161,
#     9860554,
# ]

# checkList = [
#     4332745,
#     6247915,
#     9542636,
#     6117784,

# ]

# checkList = [
#     4350778,
#     5187878,
#     3892321,
#     10276980,
#     4573986,
#     10362761,
#     5572062,
#     4979722,
#     5997271,
#     5671370,
# ]

host = '10.0.0.241'
user = 'michong'
password = 'michong'
db = 'mahjong_game_test'
charset = 'utf8mb4'

host = '172.31.11.159'
user = 'root'
password = 'Mahjong2021'
db = 'game'
charset = 'utf8mb4'


# 定义数据库连接
db = MySQLDatabase(db, user=user,
                   password=password, host=host, port=3306)


# 定义模型
class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    database_id = PrimaryKeyField()
    inventory = CharField()


check_items = ('pb00061', 'lztx00053', 'jdt00048', 'lzb00019', 'dtbj010', 'cg_0_10')


def check_one(c):
    if not c.inventory:
        return
    found = True
    for item in check_items:
        if c.inventory.find(item) == -1:
            found = False
            break
    if found:
        print(f"Character ID: {c.database_id}")


def check():
    query: Iterable[Character] = Character.select().where(Character.database_id.in_(checkList))

    for c in query:
        check_one(c)


if __name__ == '__main__':
    check()

# select DISTINCT role_id
# FROM log.event_log el
# where event_name = 'GetOrnament'
#   and event_arg1 in ('pb00061', 'lztx00053', 'jdt00048', 'lzb00019', 'dtbj010', 'cg_0_10')
#   and event_time > '2025-06-27 15:00:00'
#   and event_time < '2025-07-01 02:14:31';


# select *
# FROM log.event_log el
# where event_name = 'NewMail'
#   and event_arg1 = 'dressDraw01ActivityRewardMail'
#   and event_time > '2025-06-27 23:00:00'
#   and event_time < '2025-06-30 23:30:00'
# ORDER by event_time ASC


# select DISTINCT role_id
# FROM log.event_log el
# where event_name = 'GetOrnament'
#   and event_arg1 in ('pb00061', 'lztx00053', 'jdt00048', 'lzb00019', 'dtbj010', 'cg_0_10')
#   and event_time >= '2025-07-01 02:14:31'
#   and event_time < '2025-07-01 14:59:59';


# select *
# FROM log.event_log el
# where event_name = 'NewMail'
#   and event_arg1 = 'dressDraw01ActivityRewardMail'
#   and event_time > '2025-06-27 23:00:00'
#   and event_time < '2025-07-02 23:30:00'
# ORDER by event_time ASC;

# select *
# FROM log.event_log el
#   where event_time > '2025-06-01 23:00:00'
#   and event_args != ''
# ORDER by event_time ASC


# select DISTINCT role_id
# FROM log.event_log el
# where event_name = 'GetOrnament'
#   and event_arg1 in ('pb00061', 'lztx00053', 'jdt00048', 'lzb00019', 'dtbj010', 'cg_0_10')
#   and event_time >= '2025-07-05 14:59:59'
#   and event_time < '2025-07-08 14:59:59';


# select *
# FROM log.event_log el
# where event_name = 'NewMail'
#   and event_arg1 = 'dressDraw01ActivityRewardMail'
#   and event_time > '2025-06-27 23:00:00'
#   and event_time < '2025-07-02 23:30:00'
# ORDER by event_time ASC;


# select  *
# FROM log.event_log el
# where event_name = 'GetOrnament'
# --   where role_id=6220241
# --   and role_id=6220241
#   and event_arg1 in ('pb00061', 'lztx00053', 'jdt00048', 'lzb00019', 'dtbj010', 'cg_0_10')
#   and event_time >= '2025-07-07 12:40:00'
#   and event_time < '2025-07-10 12:45:59';


# select *
# from maque.app_v1
# where logTime > '2025-07-07 20:40:45'
#   and logTime < '2025-07-07 20:40:48'
#   and context like '%4255408%'
#   and message = 'handle event';

# select *
# from maque.app_v1
# where logTime > '2025-07-08 14:40:45'
#   and logTime < '2025-07-08 15:10:48'
#   and context like '%6220241%'
#   and message = 'handle event';

# select *
# from maque.app_v1
# where logTime > '2025-07-08 16:52:15'
#   and logTime < '2025-07-08 16:53:17'
#   and context like '%4488207%'
# order by logTime asc;
# --   and message = 'handle event';


# select *
# from maque.app_v1
# where logTime > '2025-07-08 08:00:15'
#   and logTime < '2025-07-08 08:53:17'
#   and message!='client cmd'
#   and message!='activity is show'
#   and message!='handle message request'
# --   and context like '%4488207%'
# and context like '%500%'
# and context like '%http%'
# and context not like '%activity%'
# --   and message = 'handle event';

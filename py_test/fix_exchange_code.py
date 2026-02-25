from peewee import Model, MySQLDatabase, PrimaryKeyField, IntegerField
import numpy as np


host = '10.0.0.241'
user = 'michong'
password = 'michong'
db = 'mahjong_game_test'
charset = 'utf8mb4'

# host = '172.31.11.159'
# user = 'root'
# password = 'Mahjong2021'
# db = 'game'
# charset = 'utf8mb4'


# 定义数据库连接
db = MySQLDatabase(db, user=user,
                   password=password, host=host, port=3306)


class ExchangeCode(Model):
    class Meta:
        database = db
        db_table = 'exchange_code'

    code = PrimaryKeyField()
    batch = IntegerField()


class UsedExchangeCode(Model):
    class Meta:
        database = db
        db_table = 'consumed_exchange_code'

    code = PrimaryKeyField()
    batch = IntegerField()


def update_exchange_code(codes):
    for code in codes:
        UsedExchangeCode.update(batch=code.batch).where(UsedExchangeCode.code == code.code).execute()


def get_exchange_code(codes):
    query = ExchangeCode.select().where(ExchangeCode.code.in_(codes)).execute()

    result = []
    for code in query:
        result.append(code)
    return result


def get_used_exchange_code():
    query = UsedExchangeCode.select().where(UsedExchangeCode.batch == 0).execute()

    codes = []
    for code in query:
        codes.append(code.code)
    return codes


def fix():
    try:
        to_fix = get_used_exchange_code()
        src = get_exchange_code(to_fix)

        l = np.array_split(src, 10)
        for i in l:
            update_exchange_code(i)
    except Exception as e:
        print('fix error: ', e)


if __name__ == '__main__':
    fix()

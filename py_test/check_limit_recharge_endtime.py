from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField
from multiprocessing import Pool
import json


# host = '10.0.0.241'
# user = 'michong'
# password = 'michong'
# db = 'mahjong_game_test'
# charset = 'utf8mb4'

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
    misc = CharField()


def check_activity(c):
    try:
        misc = json.loads(c.misc)
        activity = misc.get('21')
        if not activity:
            return None
        al = activity.get('1')
        if not al:
            return None
        for item in al:
            if not item:
                continue
            if item.get('-1') != 84:
                continue

            end_time = item.get('1')
            if not end_time:
                continue
            if end_time >= 1712502000000 and end_time <= 1712502600000:
                print(f'检测到异常数据: {c.database_id}, {end_time} \n')
        return None
    except Exception as e:
        print('check_activity: ', e)


def check():
    # 批量查询所有数据
    query = Character.select()
    pool = Pool(processes=6)

    start_id = 0
    page_size = 2000

    # while True:
    #     # 使用 paginate 方法来分页查询数据
    #     query = Character.select().where(Character.database_id > start_id).order_by(
    #         Character.database_id).limit(page_size)

    #     i = 0
    #     for item in query:
    #         i += 1
    #         start_id = item.database_id

    #         if not item.misc:
    #             continue
    #         pool.apply_async(check_activity, (item,))

    #     print(f'查询到 {i} 条\n')
    #     if i < page_size:
    #         break

    query = Character.select().where(Character.database_id == 3235219)
    item = query.get()
    pool.apply_async(check_activity, (item,))

    pool.close()
    pool.join()


if __name__ == '__main__':
    check()

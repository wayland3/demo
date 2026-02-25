from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField
from multiprocessing import Pool
import json


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


# 定义模型
class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    database_id = PrimaryKeyField()
    inventory = CharField()


def update_activity(activity):
    try:
        if not activity:
            return None
        al = activity.get('1')
        if not al:
            return None
        for item in al:
            if not item:
                continue
            if item.get('0') != 'discordActivity':
                continue

            k1 = item.get('1')
            if not k1:
                continue
            if k1 == 'true':
                item['1'] = True
                return activity
            if k1 == 'false':
                item['1'] = False
                return activity
        return None
    except Exception as e:
        print('update_activity: ', e)


def update_challenge(challenge):
    if not challenge:
        return None

    otk = challenge.get('12')
    if not otk:
        return None

    update = False
    result = []
    for item in otk:
        if not item:
            update = True
            continue

        item_id = item.get('id')
        if item_id:
            new_item = {'1': item_id, '2': item.get('count')}
            result.append(new_item)
            update = True

        else:
            result.append(item)

    if update:
        challenge['12'] = result
        return challenge
    return None


def update_misc(c):
    m = json.loads(c.misc)
    update = False

    activity = update_activity(m.get('21'))
    if activity:
        m['21'] = activity
        update = True

    challenge = update_challenge(m.get('10'))
    if challenge:
        m['10'] = challenge
        update = True

    if update:
        return json.dumps(m)
    return None


def update_data(character):
    try:
        misc = update_misc(character)
    except Exception as e:
        print('update: ', e)

    if not misc:
        return
    character.misc = misc

    try:
        character.save()
    except Exception as e:
        print('save: ', e)


def find():
    # 批量查询所有数据
    query = Character.select()
    pool = Pool(processes=3)

    start_id = 0
    page_size = 2000

    while True:
        # 使用 paginate 方法来分页查询数据
        query = Character.select().where(Character.database_id > start_id).order_by(
            Character.database_id).limit(page_size)

        i = 0
        for item in query:
            i += 1
            start_id = item.database_id

            if not item.inventory:
                continue
            pool.apply_async(update_data, (item,))

        print(f'查询到 {i} 条\n')
        if i < page_size:
            break

    pool.close()
    pool.join()


if __name__ == '__main__':
    find()

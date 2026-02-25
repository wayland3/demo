from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField
from multiprocessing import Pool
import json


o_host = '10.0.1.50'
o_user = 'michong'
o_password = 'Mahjong2021'
o_db = 'game_dev'
o_charset = 'utf8mb4'

n_host = '10.0.1.50'
n_user = 'michong'
n_password = 'Mahjong2021'
n_db = 'game_test'
n_charset = 'utf8mb4'


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
    misc = CharField()


class NewCharacter(OldBaseModel):
    database_id = PrimaryKeyField()
    misc = CharField()


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


def trans():
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

            if not item.misc:
                continue
            pool.apply_async(update_data, (item,))

        print(f'查询到 {i} 条\n')
        if i < page_size:
            break

    pool.close()
    pool.join()


if __name__ == '__main__':
    trans()

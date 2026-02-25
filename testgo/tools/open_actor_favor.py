# 把数据库中的雀士好感羁绊开启

import redis
import pymysql

config = {
    'user': 'mahjong',
    'password': 'Mahjong#2021',
    'host': '10.0.1.50',
    'database': 'game_internal_test'
}

redis_config = {
    'host': 'mahjong-java-dev-slb.redis'
}

prefix = 'character:50'

def remove_redis_key():
    pool = redis.ConnectionPool(**redis_config)
    r = redis.Redis(connection_pool=pool)
    keys = r.keys(f'{prefix}:*')
    if keys:
        r.delete(*keys)

def update_actor_favor_ex():
    connection = pymysql.connect(**config)
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE actor SET enable_favor_ex = 1"
            cursor.execute(sql)
            connection.commit()
            return cursor.rowcount
    
if __name__ == '__main__':
    remove_redis_key()
    result =update_actor_favor_ex()
    print('update rows: %d' % result)

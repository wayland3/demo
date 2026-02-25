import json
import time
import redis

HOST = '10.0.0.32'
PREFIX = 'character:61:*'

# 创建一个redis连接
r = redis.Redis(host=HOST, port=6379, db=0)


def check_user_name():
    for key in r.scan_iter(PREFIX, 100):
        v = r.get(key)
        time.sleep(0.1)
        if v is None:
            continue
        vv = json.loads(v.decode())
        database_id = vv.get('databaseID')
        created = vv.get('created')

        if created.startswith('1970-01-01'):
            print(f'key: {key}, database_id: {database_id}, created: {created}\n')


if __name__ == '__main__':
    check_user_name()

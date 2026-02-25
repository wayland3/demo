'''
修复 三人一位 四人一位 排行榜数据
'''

import time
import redis
from pymongo import MongoClient

base_timestamp = 2051193600


def gen_rank_score(score, timestamp):
    score = score << 30  # 将score左移30位，占据22位
    timestamp = base_timestamp - timestamp  # 基准时间戳减去传入的时间戳
    rank_score = score | timestamp  # 将timestamp写入到rankScore的低30位
    return rank_score


def parse_rank_score(rank_score):
    score = rank_score >> 30  # 通过右移操作获取得分
    timestamp = rank_score & (1 << 30 - 1)  # 通过与操作获取时间戳
    timestamp = base_timestamp - timestamp  # 还原时间戳
    return score, timestamp


def add_score(rdb_key, player_id, score, timestamp):
    rank_score = gen_rank_score(score, timestamp)
    r.zadd(rdb_key, {player_id: rank_score})


# redis
RDB_HOST = 'mahjong-java-dev-slb.redis'  # redis的ip
r = redis.Redis(host=RDB_HOST, port=6379, db=0)

REDIS_KEY_P3R1 = 'weekly:rank:p3r1:{}:65'
REDIS_KEY_P4R1 = 'weekly:rank:p4r1:{}:65'

# mongo
url = 'mongodb://admin:Mahjong2021@172.31.11.159/'
db_name = 'game'
# url = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
# db_name = 'game_pre_release'

client = MongoClient(url)
db = client[db_name]
collection = db['replaysummaries']
collection_player_summary = db['playersummaries']


def get_replay(start, end):
    pipeline = [
        {
            '$match': {
                'replayTime': {'$gt': start, '$lte': end},
                'type': {'$in': [200, 201]}
            }
        },
        # {
        #     '$group': {
        #         '_id': '$replayID',
        #         'mode': {'$first': '$mode'},
        #         'player1': {'$first': '$player1'},
        #         # 'playerID': {'$first': '$playerID'}
        #     }
        # },
        {
            '$project': {
                '_id': 1,
                'replayID': 1,
                'player1': 1,
                'mode': 1,
                'playerID': '$player1'
            }
        }
    ]
    records = list(collection.aggregate(pipeline))
    return records


def get_player():
    pipeline = [
        {
            '$project': {
                '_id': 1,
                'aiLevel': 1,
            }
        }
    ]
    records = list(collection_player_summary.aggregate(pipeline))
    return records


def get_last_week():
    start = 1719154800
    end = 1719759600
    return get_replay(start, end)


def get_this_week():
    start = 1719759600
    end = int(time.time())
    return get_replay(start, end)


def rank1(records):
    result = {}  # {'playerID':{'p3':xx, 'p4':xx}}
    for record in records:
        player_id = record['player1']
        mode = record['mode']
        rank = result.get(player_id, {'p3': 0, 'p4': 0})
        if mode in (3, 4):
            rank['p3'] += 1
        else:
            rank['p4'] += 1
        result[player_id] = rank
    return result


def add_last_week_to_redis(ranks):
    week = 26
    key_p3 = REDIS_KEY_P3R1.format(week)
    key_p4 = REDIS_KEY_P4R1.format(week)

    for player_id, rank in ranks.items():
        add_score(key_p3, player_id, rank['p3'], 1719759600)
        add_score(key_p4, player_id, rank['p4'], 1719759600)


def del_last_week():
    week = 26
    key_p3 = REDIS_KEY_P3R1.format(week)
    key_p4 = REDIS_KEY_P4R1.format(week)
    r.delete(key_p3)
    r.delete(key_p4)


def del_this_week():
    week = 27
    key_p3 = REDIS_KEY_P3R1.format(week)
    key_p4 = REDIS_KEY_P4R1.format(week)
    r.delete(key_p3)
    r.delete(key_p4)


def add_this_week_to_redis(ranks):
    week = 27
    key_p3 = REDIS_KEY_P3R1.format(week)
    key_p4 = REDIS_KEY_P4R1.format(week)

    for player_id, rank in ranks.items():
        add_score(key_p3, player_id, rank['p3'], int(time.time()))
        add_score(key_p4, player_id, rank['p4'], int(time.time()))


if __name__ == '__main__':
    players = get_player()
    player_ids = {b['_id'] for b in players if b.get('aiLevel', 0) == 0}

    rs = get_last_week()
    seen = set()
    rs = [x for x in rs if not (x['replayID'] in seen or seen.add(x['replayID']))]
    rs = [r for r in rs if r.get('playerID', -1) == r['player1'] and r['player1'] in player_ids]

    ranks = rank1(rs)

    del_last_week()
    add_last_week_to_redis(ranks)
    # l = [(k, v) for k, v in ranks.items()]
    # p3_rank = sorted(l, key=lambda x: x[1]['p3'], reverse=True)
    # p4_rank = sorted(l, key=lambda x: x[1]['p4'], reverse=True)

    # print('last week p3 rank:')
    # for i in range(100):
    #     print(p3_rank[i])
    # print('last week p4 rank:')
    # for i in range(100):
    #     print(p4_rank[i])

    rs = get_this_week()
    rs = [x for x in rs if not (x['replayID'] in seen or seen.add(x['replayID']))]
    rs = [r for r in rs if r.get('playerID', -1) == r['player1']]
    rs = [r for r in rs if r.get('playerID', -1) == r['player1'] and r['player1'] in player_ids]
    ranks = rank1(rs)

    del_this_week()
    add_this_week_to_redis(ranks)
    # l = [(k, v) for k, v in ranks.items()]
    # p3_rank = sorted(l, key=lambda x: x[1]['p3'], reverse=True)
    # p4_rank = sorted(l, key=lambda x: x[1]['p4'], reverse=True)

    # print('this week p3 rank:')
    # for i in range(100):
    #     print(p3_rank[i])
    # print('this week p4 rank:')
    # for i in range(100):
    #     print(p4_rank[i])

    # print('done')

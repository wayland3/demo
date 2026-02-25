'''
用于把玩家的得分和时间戳合并成一个rank_score, 在redis中排序
这里提供了两个方法，一个是生成rank_score，一个是解析rank_score
修改输入的score和timestamp，可以生成不同的rank_score
修改输入的rank_score，可以解析出score和timestamp
'''

import time

base_timestamp = 2051193600


def gen_rank_score(score, timestamp):
    score = score << 30  # 将score左移30位，占据22位
    timestamp = base_timestamp - timestamp  # 基准时间戳减去传入的时间戳
    rank_score = score | timestamp  # 将timestamp写入到rankScore的低30位
    return rank_score


def parse_rank_score(rank_score):
    score = rank_score >> 30  # 通过右移操作获取得分
    timestamp = rank_score & ((1 << 30) - 1)  # 通过与操作获取时间戳
    timestamp = base_timestamp - timestamp  # 还原时间戳
    return score, timestamp


if __name__ == '__main__':
    # 这是当前时间的时间戳，也可以自定义时间戳
    default_ts = int(time.time())

    # 生成rankScore
    # 输入开始 输入得分和时间戳(秒)
    score = 1220
    timestamp = 0
    # 输入结束

    rank_score = gen_rank_score(score, timestamp)
    print("生成的rank_score: ", rank_score)

    # 解析rankScore
    # 输入开始 输入rank_score
    # rank_score = 37892445182
    rank_score = 37892400019
    # 输入结束

    score, ts = parse_rank_score(rank_score)
    print("解析的score: ", score)
    print("解析的timestamp: ", ts)

from webbrowser import get
from pymongo import MongoClient

old = {
    'host': '172.31.11.159',
    'port': 27017,
    'username': 'wanglei',
    'password': '$9nAVcP0',
    'db': 'zinnor',
}

new = {
    'host': '172.31.11.159',
    'port': 27017,
    'username': 'wanglei',
    'password': '$9nAVcP0',
    'db': 'zinnor_statistic',
}


def get_connection(config):
    """
    获取数据库连接
    """
    client = MongoClient(**config)
    return client


def get_docs(db, collection):
    """
    获取文档
    """
    query = {"field": "value"}
    docs = db[collection].find(query)
    return docs


old = get_connection(old)
new = get_connection(new)


def log_active_day():


tables = [
    'log_active_day',
    'log_active_month',
    'log_active_week',
    'log_challenge',
    'log_challenge_user',
    'log_coin_consume_day',
    'log_coin_consume_month',
    'log_commodity',
    'log_currency_day',
    'log_dan_match_finish',
    'log_currency_month',
    'log_dan',
    'log_dan_match_player',
    'log_dan_match_time',
    'log_diamond_consume_day',
    'log_diamond_consume_month',
    'log_first_purchase',
    'log_game',
    'log_online',
    'log_otk',
    'log_otk_match_time',
    'log_otk_user',
    'log_pay_day',
    'log_pay_month',
    'log_rank_diamond',
    'log_rank_diamond_user',
    'log_register',
    'log_retention',
    'log_robot',
    'log_user_cost',
    'log_user_pay',
]

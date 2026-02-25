# import sys
# sys.path.append('/Users/wl/blog/data/demo/testgo')

import s
from sqlalchemy import create_engine
import pandas as pd

k ={
    'user': 'mahjong',
    'password': 'Mahjong#2021',
    'host': '10.0.1.50',
    'database': 'game_test'
}

j = {
    'user': 'root',
    'password': 'root',
    'host': '10.0.0.181',
    'database': 'game_test'
}


def get_character(config, id):
    engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (config['user'], config['password'], config['host'], config['database']))
    sql = "SELECT * FROM `character` WHERE `database_id`=%d" % id
    return pd.read_sql(sql, engine)

def get_actor(config,id):
    pass

def get_j_character(id):
    return get_character(j, id)

def get_k_character(id):
    return get_character(k, id)

def get_j_actor(id):
    return get_actor(j, id)

def get_k_actor(id):
    return get_actor(k, id)

id=6546574


def compare_character(id):
    diff = []

    jc = get_j_character(id)
    kc = get_k_character(id)
    # 不是1个
    if jc.shape[0] != kc.shape[0] or jc.shape[0]!=1:
        diff.append('character 行数不正确 java:%d go:%d' % (jc.shape[0], kc.shape[0]))
    j = jc.iloc[0]
    k = kc.iloc[0]
    
    if j['name']!=k['name']:
        diff.append("name java:%s go:%s" % (j['name'], k['name']))
    if j['sex'] !=k['sex']:
        diff.append('sex java:%d go:%d' %(j['name'], k['name']))
    if j['head'] !=k['head']:
        diff.append('head java:%d go:%d' %(j['head'], k['head']))
    if j['status'] !=k['status']:
        diff.append('status java:%d go:%d' %(j['status'], k['status']))
    if j['coin'] !=k['coin']:
        diff.append('coin java:%d go:%d' %(j['coin'], k['coin']))
    if j['diamond'] !=k['diamond']:
        diff.append('diamond java:%d go:%d' %(j['diamond'], k['diamond']))
    if j['token'] !=k['token']:
        diff.append('token java:%d go:%d' %(j['token'], k['token']))
    d= s.diff(j['inventory'], k['inventory'])
    if len(d)>0:
        diff.append({"inventory":d})
    d= s.diff(j['mailbox'], k['mailbox'])
    if len(d)>0:
        diff.append({"mailbox":d})
    d= s.diff(j['friend'], k['friend'])
    if len(d)>0:
        diff.append({"friend":d})
    d= s.diff(j['mailbox'], k['mailbox'])
    if len(d)>0:
        diff.append({"mailbox":d})
    d= s.diff(j['misc'], k['misc'])
    if len(d)>0:
        diff.append({"misc":d})
    d= s.diff(j['gossip'], k['gossip'])
    if len(d)>0:
        diff.append({"gossip":d})
    d= s.diff(j['achievements'], k['achievements'])
    if len(d)>0:
        diff.append({"achievements":d})
    return diff    
    


def compare_actor(id):
    diff = []
    ja = get_j_actor(id)
    ka = get_k_actor(id)
    # 0个 或者不相等
    if ja.shape[0] != ka.shape[0] or ja.shape[0]==0:
        diff.append('actor 行数不正确 java:%d go:%d' % (ja.shape[0], ka.shape[0]))
    pass
    




if __name__ == '__main__':
    diff=compare_character(id)
    print(diff)

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
    

    # connection = pymysql.connect(**config)
    
    # with connection:
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM `character` WHERE `database_id`=%d" % id
    #         df = pd.read_sql(sql, connection)
    #         print(df)
    #         cursor.execute(sql)
    #         result = cursor.fetchone()
    #         return pd.DataFrame(list(result), columns=[i[0] for i in cursor.description])



def get_j_character(id):
    return get_character(j, id)

def get_k_character(id):
    return get_character(k, id)



if __name__ == '__main__':
    # print(kops['host'])
    c=get_character(k, 6546574)
    print(c)
    # get_cursor(kops)

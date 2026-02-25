# Desc: mongo中的数据同步到另一个mongo中
from pymongo import MongoClient


source = {
    'host': '10.0.0.181',
    'port': 27017,
    'username': 'root',
    'password': 'root',
    'db': 'game_wyz',
}

target = {
    'host': '10.0.0.36',
    'port': 27017,
    'username': 'michong',
    'password': 'michong',
    'db': 'game_test',
}

collection = 'activity_data'


def get_connection(config):
    """
    获取数据库连接
    """
    client = MongoClient(**config)
    return client


def get_docs(db):
    """
    获取文档
    """
    query = {"field": "value"}
    docs = db[collection].find(query)
    return docs


def insert_docs(db, collection, docs):
    """
    插入文档
    """
    db[collection].insert_many(docs)


# 连接到源数据库
client = MongoClient()
source_db = client["source_db"]
source_collection = source_db["source_collection"]

# 查询需要导出的文档
query = {"field": "value"}
documents = source_collection.find(query)


# 连接到目标数据库
target_db = client["target_db"]
target_collection = target_db["target_collection"]

# 将查询到的文档导入到目标数据库中
for document in documents:
    target_collection.insert_one(document)

if __name__ == "__main__":
    pass

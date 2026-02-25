import redis

# 连接 Redis
r = redis.Redis(host='10.0.0.32', port=6379, db=0)

# 获取所有以 "char" 开头的 key
keys = r.keys("character*")

# 删除这些 key
for key in keys:
    r.delete(key)

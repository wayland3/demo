import pandas as pd
import clickhouse_connect
import openpyxl
from datetime import datetime, timedelta
import json


def generate_hourly_time_ranges(start_time, end_time):
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + timedelta(minutes=60)
        yield (current_time, next_time)
        current_time = next_time


# # 示例：生成从今天 00:00 到 23:59 的每小时时间段
# start_time = datetime.strptime("2025-03-28 00:00:00", "%Y-%m-%d %H:%M:%S")
# end_time = datetime.strptime("2025-03-30 23:59:59", "%Y-%m-%d %H:%M:%S")


# 创建 ClickHouse 客户端
client = clickhouse_connect.get_client(host='172.31.11.159', port=7123, username='mahjong', password='Mahjong2021')

# 执行查询并将结果加载到 Pandas DataFrame
# query = "SELECT * FROM `log_jp_sync`.event_log WHERE event_time > '2025-04-01 11:53:00' ORDER BY event_time DESC LIMIT 100"

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(['玩家id', '重连次数'])

# result = {}
# for start, end in generate_hourly_time_ranges(start_time, end_time):
#     # 格式化时间范围为字符串
#     start_str = start.strftime("%Y-%m-%d %H:%M:%S")
#     end_str = end.strftime("%Y-%m-%d %H:%M:%S")

#     # 执行查询并将结果加载到 Pandas DataFrame
#     query = f"select * from (select count(*) as c,role_id from log.event_log where event_time >= '{start_str}' and event_time< '{
#         end_str}' and event_name in ('PlayerOnline') group by role_id) order by c desc;"

#     df = client.query_df(query)

#     data = []
#     for i in range(len(df)):
#         if df.iloc[i]['c'] > 2:
#             data.append(df.iloc[i])

#     if len(data) == 0:
#         continue

#     start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
#     end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
#     start = start+timedelta(hours=8)
#     end = end+timedelta(hours=8)
#     start_str = start.strftime("%Y-%m-%d %H:%M:%S")
#     end_str = end.strftime("%Y-%m-%d %H:%M:%S")

#     for i in range(len(data)):
#         s = ''
#         if i == 0:
#             s = start_str
#         role_id = data[i]['role_id']
#         c = data[i]['c']
#         sheet.append([s, role_id, c])

# print(f'{start_str} - {end_str}')
# for v in data:
#     print(v['role_id'], v['c'])

# print('------------------------')

start_str = '2025-05-19 00:00:00'
end_str = '2025-05-19 23:59:59'

# query = f"select * from (select count(*) as c,role_id from log.event_log where event_time >= '{start_str}' and event_time< '{
#     end_str}' and event_name in ('PlayerOnline') group by role_id) order by c desc;"

query = f"select * from log.event_log where event_time >= '{start_str}' and event_time < '{end_str}' and event_name in ('PlayerOnline', 'PlayerOffline');"

df = client.query_df(query)

m = {}

for i, s in df.iterrows():
    c = m.get(s['role_id'], [])
    c.append(s)
    m[s['role_id']] = c

# 按时间排序
for k, v in m.items():
    m[k] = sorted(v, key=lambda x: x['event_time'])

result = {}

# offline 和 online 时间小于3分钟，记录一次
lastOffline = 0
for k, v in m.items():
    result[k] = 0
    for i in range(len(v)):
        if v[i]['event_name'] == 'PlayerOffline':
            lastOffline = v[i]['event_time']
            continue
        if v[i]['event_name'] == 'PlayerOnline':
            if lastOffline != 0:
                if (v[i]['event_time'] - lastOffline).total_seconds() < 3 * 60:
                    result[k] += 1

# 根据重连次数排序
result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

for k, v in result.items():
    sheet.append([k, v])

file_path = 'd0519.xls'
workbook.save(file_path)

# 关闭客户端
client.close()


def main():
    pass


if __name__ == '__main__':
    main()

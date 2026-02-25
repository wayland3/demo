"""
Author: wangl
Time: 2023/12/27 16:00
Description: 这个文件包含一些用于日期和时间转换的工具函数。
"""

import sys
import base64
import datetime
import hashlib
import json
import time
import pytz

default_icon = {
    'type': 'default', 'path': 'icon.png'
}


def create_item(title, subtitle, arg, icon=None):
    '创建alfred的item'
    return {
        'title': title,
        'subtitle': subtitle,
        'arg': arg,
        'icon': default_icon if icon is None else icon
    }


def now(s):
    '当前时间和时间戳'
    s = s.lower()
    if not s.startswith('now'):
        return None

    items = []

    # 时间戳
    local_date_time = datetime.datetime.now()
    timestamp = int(local_date_time.timestamp())
    item = create_item(str(timestamp), 'Timestamp', str(timestamp))
    items.append(item)

    # 本地时间
    formatted_local_date_time = local_date_time.strftime('%Y-%m-%d %H:%M:%S')
    item = create_item(formatted_local_date_time,
                       'Local time', formatted_local_date_time)
    items.append(item)

    # UTC时间
    utc_date_time = datetime.datetime.utcnow()
    formatted_utc_date_time = utc_date_time.strftime('%Y-%m-%d %H:%M:%S')
    item = create_item(formatted_utc_date_time,
                       'UTC time', formatted_utc_date_time)
    items.append(item)

    return items


def timestamp2datetime(s):
    '时间戳转时间只处理秒和毫秒'
    if not s.isdigit():
        return None

    if len(s) > 13:
        return None

    # 10位及以下的不处理，作为秒数处理
    # 10位以上到13位的除以1000，作为秒数处理
    ts = int(s)
    if len(s) > 10 and len(s) <= 13:
        ts = ts/1000

    items = []

    # 本地时间
    date_time = time.localtime(ts)
    formatted_date_time = time.strftime(
        '%Y-%m-%d %H:%M:%S', date_time)
    item = create_item(formatted_date_time, 'Local time', formatted_date_time)
    items.append(item)

    # UTC时间
    utc_date_time = time.gmtime(ts)
    formatted_utc_date_time = time.strftime(
        '%Y-%m-%d %H:%M:%S', utc_date_time)
    item = create_item(formatted_utc_date_time,
                       'UTC time', formatted_utc_date_time)
    items.append(item)

    return items


def datetime2timestamp(s):
    '''时间转时间戳
       处理格式包含:
       Y
       Y-m
       Y-m-d
       Y-m-d H
       Y-m-d H:M
       Y-m-d H:M:S
       Y-m-d H:M:S.ms
    '''

    formats = [
        '%Y',
        '%Y-%m',
        '%Y-%m-%d',
        '%Y-%m-%d %H',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f'
    ]

    s = s.strip()
    s = s.rstrip(':')
    s = s.rstrip('.')

    items = []
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(s, fmt)
            # 作为本地时间
            ts = dt.timestamp()
            item = create_item(
                str(int(ts)), 'As local to Timestamp', str(int(ts)))
            items.append(item)

            # 作为UTC时间
            dt = dt.replace(tzinfo=pytz.UTC)
            ts = dt.timestamp()
            item = create_item(
                str(int(ts)), 'As UTC to Timestamp', str(int(ts)))
            items.append(item)
            break
        except ValueError:
            continue
    return items


def md5(s):
    'md5加密'
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    s = m.hexdigest()
    item = create_item(s, 'md5', s)
    return [item]


def encode_base64(s):
    'base64编码'
    encoded = base64.b64encode(s.encode('utf-8'))
    s = encoded.decode('utf-8')
    item = create_item(s, 'base64编码', s)
    return [item]


def decode_base64(s):
    'base64解码'
    try:
        decoded = base64.b64decode(s).decode('utf-8')
    except Exception:
        return None
    item = create_item(decoded, 'base64解码', decoded)
    return [item]


func = [now, timestamp2datetime, datetime2timestamp,
        md5, encode_base64, decode_base64]


def trans(*args):
    '转换'
    if len(args) <= 1:
        return
    s = ' '.join(args[1:])
    s = s.strip()
    if not s:
        return

    total_items = []

    for f in func:
        items = f(s)
        if items:
            total_items.extend(items)
    result = {}
    result['items'] = total_items
    print(json.dumps(result))


def main():
    '入口'
    args = sys.argv
    trans(*args)


if __name__ == '__main__':
    main()

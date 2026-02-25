import json

import mysql.connector

host="10.0.0.135"
user="root"
password="root"
db1 = "mahjong_game_wl_1"
db2 = "mahjong_game_wl_2"


def get_db1():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db1
    )

def get_db2():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db2
    )

def get_db1_dict():
    db1 = get_db1()
    cursor = db1.cursor()
    cursor.execute("SELECT database_id, misc FROM `character` WHERE parent_id != 0 order by database_id desc limit 50000 offset 100000")
    results = cursor.fetchall()
    db1_dict = {}
    for i in results:
        if i is None:
            continue
        db1_dict[i[0]] = i[1]
    return db1_dict

def get_db2_dict():
    db2 = get_db2()
    cursor = db2.cursor()
    cursor.execute("SELECT database_id, misc FROM `character` WHERE parent_id != 0 order by database_id desc limit 50000 offset 100000")
    results = cursor.fetchall()
    db2_dict = {}
    for i in results:
        if i is None:
            continue
        db2_dict[i[0]] = i[1]
    return db2_dict



a = '''{"1": [], "2": [], "3": {"shopSnapshotMap": {}}, "4": [], "5": [], "10": {"1": 72, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": [{"1": 0, "2": 0}, {"1": 2, "2": 0}], "8": [{"1": 0, "2": 0}, {"1": 2, "2": 0}, {"1": 3, "2": 0}], "10": 0, "11": 1696086000, "14": 0}, "11": {"1": 2, "2": {"1": 1, "2": 0, "6": 0, "7": 0}, "3": {"1": 1, "2": 0, "6": 0, "7": 0}, "6": [{"1": "hb001", "2": 25000}]}, "12": {"guyi": 0, "mode": 1, "tips": 1, "fanfu": 1, "shiti": 0, "rounds": 1, "shiduan": 1, "thinks1": 60, "thinks2": 0, "zimosun": 1, "chibaopai": 2, "maxPlayers": 3, "initialPoints": 35000, "requirePoints": 40000, "showHandCards": 0}, "13": {"time": 1696086000228, "flashTime": 0, "shopDataList": [{"id": "1", "flag": [2], "item": {"id": "lw00010", "count": 1}, "name": "Item_lw00010", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "7", "flag": [2], "item": {"id": "hpk00002", "count": 1}, "name": "Item_hpk00002", "type": [], "price": 900000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "repeatBuy": 1, "sellPrice": 810000, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "2", "flag": [0], "item": {"id": "zb00005", "count": 1}, "name": "Item_zb00005", "type": [], "price": 900000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "repeatBuy": 1, "sellPrice": 900000, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "5", "flag": [0], "item": {"id": "lw00081", "count": 1}, "name": "Item_lw00081", "type": [], "price": 67500, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "sellPrice": 67500, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "4", "flag": [2], "item": {"id": "lw00050", "count": 1}, "name": "Item_lw00050", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "sellPrice": 4500, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "8", "flag": [2], "item": {"id": "lw00080", "count": 1}, "name": "Item_lw00080", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "sellPrice": 13500, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "3", "flag": [0], "item": {"id": "lw00070", "count": 1}, "name": "Item_lw00070", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "sellPrice": 15000, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}, {"id": "6", "flag": [0], "item": {"id": "lw00050", "count": 1}, "name": "Item_lw00050", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": "0001-01-01T00:00:00Z", "priceType": 1, "sellPrice": 15000, "showOrder": [0], "startTime": "0001-01-01T00:00:00Z", "freebiesStr": ""}], "shopSnapshotMap": {}}, "14": {"version": 1, "productIDs": [], "firstChargeFlag": false}, "15": {"flashTime": 1696086000166, "presentationMap": {}}, "17": {"15": "0"}, "20": {}, "21": {"1": [{"0": "transmitActivity", "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, {"0": "goodReviewActivity"}, {"0": "rookiesMonthlyActivities", "1": false, "2": 0, "3": [{"1": 1, "2": 0}, {"1": 2, "2": 0}, {"1": 3, "2": 0}, {"1": 4, "2": 0}, {"1": 5, "2": 0}, {"1": 6, "2": 0}, {"1": 7, "2": 0}, {"1": 8, "2": 0}, {"1": 9, "2": 0}, {"1": 10, "2": 0}, {"1": 11, "2": 0}, {"1": 12, "2": 0}, {"1": 13, "2": 0}, {"1": 14, "2": 0}, {"1": 15, "2": 0}, {"1": 16, "2": 0}, {"1": 17, "2": 0}, {"1": 18, "2": 0}, {"1": 19, "2": 0}, {"1": 20, "2": 0}, {"1": 21, "2": 0}, {"1": 22, "2": 0}, {"1": 23, "2": 0}, {"1": 24, "2": 0}, {"1": 25, "2": 0}, {"1": 26, "2": 0}, {"1": 27, "2": 0}, {"1": 28, "2": 0}, {"1": 29, "2": 0}, {"1": 30, "2": 0}], "4": false, "5": 0}, {"0": "goodReviewActivity_WINDOWS"}, {"0": "sign7Activities", "1": "true", "2": [{"1": -1, "2": 1692543600339, "3": 1, "4": 1, "5": 1}, {"1": -1, "2": 1692630000836, "3": 2, "4": 1, "5": 2}, {"1": 1, "2": 1696086000166, "3": 3, "4": 1, "5": 3}, {"1": 0, "2": 0, "3": 4, "4": 1, "5": 4}, {"1": 0, "2": 0, "3": 5, "4": 1, "5": 5}, {"1": 0, "2": 0, "3": 6, "4": 1, "5": 6}, {"1": 0, "2": 0, "3": 7, "4": 1, "5": 7}], "3": 1696086000166, "4": [{"1": 1, "2": 1696086000166, "3": 1, "4": 2, "5": 11}, {"1": 0, "2": 0, "3": 2, "4": 2, "5": 12}, {"1": 0, "2": 0, "3": 3, "4": 2, "5": 13}, {"1": 0, "2": 0, "3": 4, "4": 2, "5": 14}, {"1": 0, "2": 0, "3": 5, "4": 2, "5": 15}, {"1": 0, "2": 0, "3": 6, "4": 2, "5": 16}], "5": "1696172400166", "6": "1696086000166", "7": "false"}, {"0": "goodReviewActivity_ANDROID"}, {"0": "discordActivity"}, {"0": "MonthlyCardActivities", "1": "false", "2": "0", "3": "false", "4": 0, "5": "false"}, {"0": "noviceGiftActivity", "1": 1693126837863, "4": 1}, {"0": "recharge_model_56", "2": [{"1": 1, "2": 0, "3": 0, "4": "", "16": 0, "17": 200}, {"1": 2, "2": 0, "3": 0, "4": "", "16": 0, "17": 988}, {"1": 3, "2": 0, "3": 0, "4": "", "16": 0, "17": 1800}, {"1": 4, "2": 0, "3": 0, "4": "", "16": 0, "17": 4588}, {"1": 5, "2": 0, "3": 0, "4": "", "16": 0, "17": 6888}], "3": "false", "5": false, "-1": 56}, {"0": "goodReviewActivity_IOS"}, {"0": "questionnaireSurvey01Activity", "4": 4}, {"0": "jigsaw_model_57", "1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "2": [1, 2, 3, 4, 5, 6, 7], "3": 1696086000228, "4": {"1": 3, "2": 0, "3": 0, "4": "overRankOrder", "11": 0, "12": 1, "15": 2}, "5": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "7": 0, "8": 0, "-1": 57}, {"0": "practiceTaskActivities", "1": "false", "2": [{"1": 101, "2": 1, "3": 0, "4": "overRank", "11": 0, "12": 1}, {"1": 201, "2": 2, "3": 0, "4": "overChallenge", "11": 0, "12": 1}, {"1": 301, "2": 3, "3": 0, "4": "level", "11": 1, "12": 0}, {"1": 401, "2": 4, "3": 0, "4": "qs_love", "11": -1, "12": 1, "13": 0}, {"1": 601, "2": 6, "3": 0, "4": "overFriendGame", "11": 0, "12": 1, "13": 2, "14": {}}], "3": "false", "6": []}]}, "23": [], "24": 0, "25": [], "26": [], "100": "txk00001", "101": "pb00001", "102": "zb00001", "103": "lzb00001", "104": "tz00001", "105": "st00001", "106": "dtbj001", "107": "hptx00001", "108": "lztx00001", "109": "lzyy00001", "110": "mptx00001", "111": "cg_0_1", "112": "flk00001", "113": "hpk00001", "114": "jdt00001", "201": 0, "300": ["2"], "301": 1, "302": 1, "303": 1, "304": 2, "305": 0, "306": "", "307": 0, "308": {"5": 1}, "309": {"1": 23, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}, "400": {"2": [], "3": []}, "401": 0, "403": 1, "506": 0, "600": {"1": [{"1": 500, "2": true}, {"1": 1000, "2": true}, {"1": 2000, "2": true}]}}'''
b = '''{"4": [], "5": [], "10": {"1": 72, "7": [{}, {"1": 2}], "8": [{}, {"1": 2}, {"1": 3}], "11": 1696086000}, "11": {"1": 2, "6": [{"1": "hb001", "2": 25000}]}, "12": {"guyi": 0, "mode": 1, "tips": 1, "fanfu": 1, "shiti": 0, "rounds": 1, "shiduan": 1, "thinks1": 60, "thinks2": 0, "zimosun": 1, "chibaopai": 2, "maxPlayers": 3, "initialPoints": 35000, "requirePoints": 40000, "showHandCards": 0}, "13": {"time": 1696086000228, "flashTime": 0, "shopDataList": [{"id": "1", "flag": [2], "item": {"id": "lw00010", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00010", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 0, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "7", "flag": [2], "item": {"id": "hpk00002", "type": 2, "count": 1, "expiry": null, "created": "2023-09-25T06:23:42.568Z", "boxedTarget": ""}, "name": "Item_hpk00002", "type": [], "price": 900000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 1, "sellPrice": 810000, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "2", "flag": [0], "item": {"id": "zb00005", "type": 2, "count": 1, "expiry": null, "created": "2023-09-25T06:23:42.569Z", "boxedTarget": ""}, "name": "Item_zb00005", "type": [], "price": 900000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 1, "sellPrice": 900000, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "5", "flag": [0], "item": {"id": "lw00081", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00081", "type": [], "price": 67500, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 67500, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "4", "flag": [2], "item": {"id": "lw00050", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00050", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 4500, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "8", "flag": [2], "item": {"id": "lw00080", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00080", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 13500, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "3", "flag": [0], "item": {"id": "lw00070", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00070", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 15000, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}, {"id": "6", "flag": [0], "item": {"id": "lw00050", "type": 1, "count": 1, "expiry": null, "created": null, "boxedTarget": ""}, "name": "Item_lw00050", "type": [], "price": 15000, "limited": 1, "freebies": null, "overTime": null, "priceType": 1, "repeatBuy": 0, "sellPrice": 15000, "showOrder": [0], "startTime": null, "freebiesStr": null, "limitedTime": 0}], "shopSnapshotMap": {}}, "14": {"version": 1, "productIDs": [], "firstChargeFlag": false}, "15": {"flashTime": 1696086000166, "presentationMap": {}}, "17": {"15": "0"}, "20": {}, "21": {"1": [{"0": "discordActivity"}, {"0": "sign7Activities", "1": "true", "2": [{"1": -1, "2": 1692543600339, "3": 1, "4": 1, "5": 1}, {"1": -1, "2": 1692630000836, "3": 2, "4": 1, "5": 2}, {"1": 1, "2": 1696086000166, "3": 3, "4": 1, "5": 3}, {"1": 0, "2": 0, "3": 4, "4": 1, "5": 4}, {"1": 0, "2": 0, "3": 5, "4": 1, "5": 5}, {"1": 0, "2": 0, "3": 6, "4": 1, "5": 6}, {"1": 0, "2": 0, "3": 7, "4": 1, "5": 7}], "3": 1696086000166, "4": [{"1": 1, "2": 1696086000166, "3": 1, "4": 2, "5": 11}, {"1": 0, "2": 0, "3": 2, "4": 2, "5": 12}, {"1": 0, "2": 0, "3": 3, "4": 2, "5": 13}, {"1": 0, "2": 0, "3": 4, "4": 2, "5": 14}, {"1": 0, "2": 0, "3": 5, "4": 2, "5": 15}, {"1": 0, "2": 0, "3": 6, "4": 2, "5": 16}], "5": "1696172400166", "6": "1696086000166", "7": "false"}, {"0": "MonthlyCardActivities", "1": "false", "2": "0", "3": "false", "4": 0, "5": "false"}, {}, {"0": "transmitActivity", "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}, {"0": "recharge_model_56", "2": [{"1": 1, "2": 0, "3": 0, "4": "", "16": 0, "17": 200}, {"1": 2, "2": 0, "3": 0, "4": "", "16": 0, "17": 988}, {"1": 3, "2": 0, "3": 0, "4": "", "16": 0, "17": 1800}, {"1": 4, "2": 0, "3": 0, "4": "", "16": 0, "17": 4588}, {"1": 5, "2": 0, "3": 0, "4": "", "16": 0, "17": 6888}], "3": "false", "5": false, "-1": 56}, {"0": "goodReviewActivity"}, {}, {"0": "noviceGiftActivity", "1": 1693126837863, "4": 1}, {"0": "goodReviewActivity_IOS"}, {"0": "rookiesMonthlyActivities", "1": false, "2": 0, "3": [{"1": 1, "2": 0}, {"1": 2, "2": 0}, {"1": 3, "2": 0}, {"1": 4, "2": 0}, {"1": 5, "2": 0}, {"1": 6, "2": 0}, {"1": 7, "2": 0}, {"1": 8, "2": 0}, {"1": 9, "2": 0}, {"1": 10, "2": 0}, {"1": 11, "2": 0}, {"1": 12, "2": 0}, {"1": 13, "2": 0}, {"1": 14, "2": 0}, {"1": 15, "2": 0}, {"1": 16, "2": 0}, {"1": 17, "2": 0}, {"1": 18, "2": 0}, {"1": 19, "2": 0}, {"1": 20, "2": 0}, {"1": 21, "2": 0}, {"1": 22, "2": 0}, {"1": 23, "2": 0}, {"1": 24, "2": 0}, {"1": 25, "2": 0}, {"1": 26, "2": 0}, {"1": 27, "2": 0}, {"1": 28, "2": 0}, {"1": 29, "2": 0}, {"1": 30, "2": 0}], "4": false, "5": 0}, {"0": "questionnaireSurvey01Activity", "4": 4}, {"0": "jigsaw_model_57", "1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "2": [1, 2, 3, 4, 5, 6, 7], "3": 1696086000228, "4": {"1": 3, "2": 0, "3": 0, "4": "overRankOrder", "11": 0, "12": 1, "15": 2}, "5": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "7": 0, "8": 0, "-1": 57}, {"0": "goodReviewActivity_ANDROID"}, {"0": "practiceTaskActivities", "1": "false", "2": [{"1": 101, "2": 1, "3": 0, "4": "overRank", "11": 0, "12": 1}, {"1": 201, "2": 2, "3": 0, "4": "overChallenge", "11": 0, "12": 1}, {"1": 301, "2": 3, "3": 0, "4": "level", "11": 1, "12": 0}, {"1": 401, "2": 4, "3": 0, "4": "qs_love", "11": -1, "12": 1, "13": 0}, {"1": 601, "2": 6, "3": 0, "4": "overFriendGame", "11": 0, "12": 1, "13": 2, "14": {}}], "3": "false", "6": []}, {}, {"0": "goodReviewActivity_WINDOWS"}]}, "22": 0, "24": 0, "25": [], "100": "txk00001", "101": "pb00001", "102": "zb00001", "103": "lzb00001", "104": "tz00001", "105": "st00001", "106": "dtbj001", "107": "hptx00001", "108": "lztx00001", "109": "lzyy00001", "110": "mptx00001", "111": "cg_0_1", "112": "flk00001", "113": "hpk00001", "114": "jdt00001", "201": 0, "300": ["2"], "301": 1, "302": 1, "303": 1, "304": 2, "305": 0, "306": "", "307": 0, "308": {"5": 1}, "309": {"1": 23}, "400": {"2": [], "3": []}, "401": 0, "403": 1, "504": {"1": {}}, "505": [], "506": 0, "600": {"1": [{"1": 500, "2": true}, {"1": 1000, "2": true}, {"1": 2000, "2": true}]}}'''

def is_none(v):
    if v == 0 or v == "" or v is None:
        return True
    if isinstance(v, list):
        if len(v)==0:
            return True
        for i in v:
            if not is_none(i):
                return False
        return True
    if isinstance(v, dict):
        if len(v)==0:
            return True
        for k,vv in v.items():
            if not is_none(vv):
                return False
        return True
    if v == '0001-01-01T00:00:00Z':
        return True
    return False

def clean(value):
    if isinstance(value, dict):
        nd = {}
        for k, v in value.items():
            if is_none(v):
                continue
            nd[k] = clean(v)
        return nd
    if isinstance(value, list):
        nl = []
        for i in value:
            if is_none(i):
                continue
            nl.append(clean(i))
        return nl
    return value

def special_clean(value):
    nd = {}
    for k, v in value.items():
        if k == "11":
            d11 = {}
            for kk, vv in v.items():
                if kk == "2" or kk == "3":
                    continue
                d11[kk] = vv
            nd[k] = d11
        elif k == "13":
            continue
        elif k== "21":
            continue
        else:
            nd[k] = v
    return nd

def e(a,b):
    if type(a) != type(b):
        return "type not equal"
    if isinstance(a, dict):
        for k,v in a.items():
            if k not in b:
                return "key not equal"
            d = e(v, b[k])
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "list len not equal"
        for i in range(len(a)):
            d = e(a[i], b[i])
            if d:
                return d
        return None
    return a==b

if __name__ == '__main__':
    
    # a = json.loads(a)
    # b = json.loads(b)
    # a = clean(a)
    # b = clean(b)
    # a = special_clean(a)
    # b = special_clean(b)
    
    # equal=e(a, b)
    # if not equal:
    #     print(a)
    #     print(b)
    # e = is_none({"a":[{"a":0}]})


    db1_dict = get_db1_dict()
    db2_dict = get_db2_dict()
    for k,v in db1_dict.items():
        db2c = db2_dict[k]
        try:
            a = json.loads(v)
            b = json.loads(db2c)
        except:
            print(k)
            continue
        a = clean(a)
        b = clean(b)
        a = special_clean(a)
        b = special_clean(b)
        equal=e(a, b)
        if not equal:
            print(a)
            print(b)
        

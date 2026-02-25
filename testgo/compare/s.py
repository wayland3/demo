import json
from deepdiff import DeepDiff

# 对json进行排序
def sort(obj):
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, list):
                sort(item)
            elif isinstance(item, dict):
                sort(item)
        obj.sort(key=sort_dict)
    elif isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], list):
                sort(obj[key])
            elif isinstance(obj[key], dict):
                sort(obj[key])
        obj_sorted = sorted(obj.items(), key=lambda x: x[0])
        obj.clear()
        obj.update(obj_sorted)


# 定义一个比较函数，用于比较两个字典的大小
def sort_dict(d):
    return json.dumps(d, sort_keys=True)


def diff(obj1,obj2):
    obj1=json.loads(obj1)
    obj2=json.loads(obj2)
    sort(obj1)
    sort(obj2)
    return DeepDiff(obj1, obj2)

# 比较两个Python对象
def printDiff(obj1,obj2):  
    # 对Python对象进行排序
    sort(obj1)
    sort(obj2)    
    
    diff = DeepDiff(obj1, obj2)

    # 输出差异
    print(diff)

if __name__ == '__main__':
    # 定义两个Python对象
    s1 = '{"1": [1, 66, 4, 68, 70, 7, 73, 10, 12, 76, 14, 78, 16, 80, 18, 83, 20, 22, 87, 24, 26, 90, 28, 93, 30, 32, 96, 34, 36, 100, 38, 40, 42, 44, 46, 48, 50, 52, 56, 60, 62], "3": 1}'
    s2 = '{"1": [16, 93, 90, 96, 26, 78, 83, 22, 66, 48, 4, 40, 7, 73, 62, 70, 10, 24, 87, 50, 18, 30, 32, 14, 28, 68, 34, 42, 80, 38, 60, 1, 46, 56, 76, 20, 36, 52, 100, 12, 44], "2": [], "3": 1}'


    



    
    obj1 = json.loads(s1)
    obj2 = json.loads(s2)    

    # printDiff(obj1,obj2)
    
    sort(obj1)
    sort(obj2)

    print(json.dumps(obj1))
    print(json.dumps(obj2))

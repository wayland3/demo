import json
from pymongo import MongoClient


url = 'mongodb://mahjong:Mahjong#2021@10.0.1.54/'
db_name = 'game_test'

collection_weeks_core = 'week_score'
collection_player_summary = 'playersummaries'
collection_player_actor_amount = 'player_actor_amount'


client = MongoClient(url)

db = client[db_name]

week_score = db[collection_weeks_core]
player_summary = db[collection_player_summary]
actor_amount = db[collection_player_actor_amount]

# 查询条件
scores = week_score.find()

score_ids = []
for score in scores:
    score_ids.append(score['_id'])

player_summaries = player_summary.find({'_id': {'$in': score_ids}})

players = set()
for player in player_summaries:
    players.add(player['_id'])

for i in score_ids:
    if i not in players:
        print(i)
        week_score.delete_one({'_id': i})
        print(f'delete: {i}')

actor_amounts = actor_amount.find()
actor_amount_ids = []
for amount in actor_amounts:
    actor_amount_ids.append(amount['_id'])

for i in actor_amount_ids:
    if i not in players:
        print(i)
        actor_amount.delete_one({'_id': i})
        print(f'delete: {i}')

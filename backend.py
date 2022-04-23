import pymongo
from pymongo import errors
client = pymongo.MongoClient('localhost', 27017)
db = client['genshin_bot_db']
users = db['users']

async def add_user(user_id):
    data = {
        '_id': user_id,
        'uid': None,
        'nickname': None,
        'adventure_rank': None,
        'world_level': None,
        'message': None,
        'likes': 0
    }
    users.insert_one(data)

import redis
cache = redis.Redis()

async def add_user_queue(user_id):
    user = users.find_one({'_id': user_id})
    cache.set(user['_id'], user['likes'], 60*60)


def current_queue():
    data = []
    for i in cache.keys('*'):
        t = users.find_one({'_id': int(i)})
        data.append(t)
    data.sort(key=lambda x: x['likes'])
    return data


def get_player_by_queue(num: int):
    data = current_queue()
    try:
        result = data[num]
    except IndexError:
        result = f'список закончился!'

    return result

# import sqlite3
# from config import DB_NAME
# from aiogram.types import Message

# try:
#     sqlite_connection = sqlite3.connect(DB_NAME)
#     cursor = sqlite_connection.cursor()
#     print("База данных создана и успешно подключена к SQLite")
#
#     sqlite_select_query = "select sqlite_version();"
#     cursor.execute(sqlite_select_query)
#     record = cursor.fetchall()
#     print("Версия базы данных SQLite: ", record)
# except sqlite3.Error as error:
#     print("Ошибка при подключении к sqlite", error)
#
#
# async def start_db(message: Message):
#     try:
#         user = cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.chat.id};").fetchone()
#     except sqlite3.OperationalError:
#         if


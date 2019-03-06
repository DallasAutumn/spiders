# -*- coding: utf-8 -*-
import asyncio
import motor.motor_asyncio
import pprint
import pathlib
import aiofiles
from config import *


# class MotorBase:
#     _db = {}
#     _collection = {}

#     def __init__(self, loop=None):
#         self.motor_uri = ''
#         self.loop = loop or asyncio.get_event_loop()

#     def client(self, db):
#         self.motor_uri = f"mongodb://localhost:27017/{db}"
#         return motor.motor_asyncio.AsyncIOMotorClient(self.motor_uri, io_loop=self.loop)

#     def get_db(self, db=MOTOR_DB):
#         if db not in self._db:
#             self._db['db'] = self.client(db)[db]
#         return self._db[db]


# async def save_data(items):
#     mb = MotorBase().get_db(db=MOTOR_DB)
#     for item in items:
#         try:
#             await mb.comments.update_one(
#                 {'rpid': item.get('rpid')},
#                 {'$set', item},
#                 upsert=True
#             )
#         except Exception as e:
#             print('error', e.args)
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client[MOTOR_DB]
collection = db[COLLECTION]


async def do_insert(items):
    for item in items:
        try:
            await collection.update_one(
                {'rpid': item.get('rpid')},
                {'$set': item},
                upsert=True
            )
        except Exception as e:
            print('error', e.args)


async def do_find():
    data = collection.find()
    # data = cursor.to_list(length=20000)
    return data


async def mongo2file():
    data = await do_find()
    fp = pathlib.Path.joinpath(pathlib.Path.cwd(), 'msg.txt')
    async with aiofiles.open(fp, 'a+', encoding='utf-8') as f:
        async for document in data:
            t = document.get('content').get('message').strip()
            await f.write(t)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mongo2file())

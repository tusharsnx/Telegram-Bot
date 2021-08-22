import os
import asyncio

from motor import motor_asyncio
import urllib.parse


username = os.environ["USERNAME"]
password = os.environ["PASS"]
password = urllib.parse.quote(password)
loop = asyncio.get_event_loop()
client = motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{username}:{password}@cluster0.i7jqe.mongodb.net", io_loop=loop)

db = client["telegram_bot"]
users = db["users"]
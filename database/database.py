import os

from motor import motor_asyncio
import urllib.parse
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())
username = os.environ["USER_NAME"]
password = os.environ["PASS"]
password = urllib.parse.quote(password)
client = motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{username}:{password}@cluster0.i7jqe.mongodb.net")

db = client["telegram_bot"]
users = db["users"]
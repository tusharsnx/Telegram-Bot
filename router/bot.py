import os
from responses.generate_responses import generate_response
from fastapi import APIRouter, Body, Response, BackgroundTasks
import aiohttp
import dotenv
from router.utils import send_message

router = APIRouter()

dotenv.load_dotenv(dotenv.find_dotenv())

API_KEY = os.getenv("API_KEY")



@router.get("/")
async def index():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/bot{API_KEY}/getMe") as resp:
            res = await resp.json()
    return res


@router.post(f"/{API_KEY}")
async def webhook(task: BackgroundTasks, update = Body(None)):
    task.add_task(send_message_backgroud_task, update=update)
    return {}


async def send_message_backgroud_task(update):
    text = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    username = update["message"]["from"]["username"]
    print(f"update recieved from {username}: ", update)
    resp = await generate_response(text, username)
    await send_message(resp, chat_id)
import os

from fastapi import APIRouter, Body, BackgroundTasks
import aiohttp
import dotenv

from responses.generate_responses import generate_response
from router.utils import send_message, set_webhook

router = APIRouter()

dotenv.load_dotenv(dotenv.find_dotenv())

API_KEY = os.getenv("API_KEY")

# setting up webhook using WEBHOOK env
set_webhook()

@router.get("/")
async def index():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/bot{API_KEY}/getMe") as resp:
            res = await resp.json()
    return res


@router.post(f"/{API_KEY}")
async def webhook(task: BackgroundTasks, update = Body(None)):
    """
    args:
        task: BackgroundTasks object to create task and do it in backgroung
        update: Request body in json

    Return:
        empty json with status code 200

    Immediately sends ack to the telegram api for recieved request and creates a backgroud task 
    to generate response and send it to user. 
    """
    task.add_task(send_message_backgroud_task, update=update)
    return {}


# background task to generate response and send message
async def send_message_backgroud_task(update):
    text = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    username = update["message"]["from"]["username"]
    print(f"update recieved from {username}: ", update)
    
    # generate response
    resp = await generate_response(text, username)

    # send the response to the user
    await send_message(resp, chat_id)
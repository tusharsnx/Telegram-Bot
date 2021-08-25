import os

import aiohttp
import dotenv
import urllib.parse
import requests

dotenv.load_dotenv(dotenv.find_dotenv())

API_KEY = os.getenv("API_KEY")


async def send_message(texts, chat_id):
    bot_url = f"https://api.telegram.org/bot{API_KEY}"
    
    # single message
    if not isinstance(texts, list):
        texts = [texts]
    
    async with aiohttp.ClientSession() as session:
        for text in texts:
            safe_string = urllib.parse.quote_plus(text)
            url = bot_url+f"/sendMessage?chat_id={chat_id}&text={safe_string}"
            async with session.get(url) as resp:
                if resp.status==200:
                    print("message sent")
                else:
                    print("message sending failed")


# setup a webhook using env when server starts
def set_webhook():
    WEBHOOK = os.getenv("WEBHOOK")
    print("webhook:", WEBHOOK)
    url = f"https://api.telegram.org/bot{API_KEY}/setWebhook?url={WEBHOOK}/{API_KEY}"
    resp = requests.get(url)
    body = resp.json()
    if resp.status_code==200:
        print("webhook setup with response:", body)
    else:
        print("webhook setup failed")
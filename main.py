from fastapi import FastAPI
from router import bot


app = FastAPI()

app.include_router(bot.router)

# url to setup webhook
# https://api.telegram.org/bot{API_KEY}/setWebhook/url=
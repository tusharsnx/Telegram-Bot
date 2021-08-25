from fastapi import FastAPI
from router import bot


app = FastAPI()

app.include_router(bot.router)
import requests
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())
API_KEY = os.getenv("API_KEY")
WEBHOOK = os.getenv("WEBHOOK")
print("api key:", API_KEY)
print("webhook:", WEBHOOK)

url = f"https://api.telegram.org/bot{API_KEY}/setWebhook?url={WEBHOOK}/{API_KEY}"

resp = requests.get(url)
body = resp.json()
if resp.status_code==200:
    print("succeeded with response:", body)
else:
    print("failed")
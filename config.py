from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", 29893020))
API_HASH = getenv("API_HASH", "28e79037f0b334ef0503466c53f08af5")
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 6399386263))
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Blissfull_Music")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/akaChampu")
OWNER_USERNAME = "itsMeShivanshu"

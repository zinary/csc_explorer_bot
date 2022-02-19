import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CSC_API_KEY_PROD = os.environ.get("CSC_API_KEY")
DEV_CHAT_ID = os.environ.get("DEV_CHAT_ID")
DEV_WALLET_ADDRESS = os.environ.get("DEV_WALLET_ADDRESS")

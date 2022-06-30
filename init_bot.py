import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

storage = MemoryStorage()

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
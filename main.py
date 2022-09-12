from aiogram import Dispatcher, Bot, executor
import asyncio

from config import BOT_TOKEN
from db import Database

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)
db = Database('database.db')

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, loop=loop)


import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
import os
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from base import DataBase
from scheduler import start_scheduler

db = DataBase()

load_dotenv()
token = os.getenv('TOKEN')
weather_token = os.getenv('WEATHER_TOKEN')

async def main():
    print('НАЧАЛС')
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    await db.init_db()
    dp.include_router(router)
    await start_scheduler(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from base import DataBase
from weather import get_weather
import os
from dotenv import load_dotenv
from ai_req import ai_response
load_dotenv()

db=DataBase()
api_key = os.getenv('WEATHER_TOKEN')

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

async def start_scheduler(bot: Bot):
    @scheduler.scheduled_job('cron',hour=10,minute=0)
    async def scheduler_job():
        users = await db.get_all_users()

        for tg_id, city in users:
            try:
                response = await get_weather(city, api_key)
                req_ai = await ai_response(response, city)
                await bot.send_message(tg_id,f'Добрый день, {req_ai}')
            except Exception as e:
                print(e)

    scheduler.start()
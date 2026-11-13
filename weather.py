import os
import asyncio
import requests
from dotenv import load_dotenv
import aiohttp

load_dotenv()
api_key = os.getenv('WEATHER_TOKEN')

async def random_city(api_key):
    url='https://random-city-api.vercel.app/api/random-city'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return data['city']
    except Exception as e:
        return f'Ошибка код: {e}'

async def get_weather_digets(city,api_key):
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    try:
        async with aiohttp.ClientSession( ) as session:
            async with session.get(url) as response:
                data = await response.json()
                if str(data.get('cod')) != '200':
                    return None
                return data['main']['temp']
    except Exception as e:
        return f'Ошибка код: {e}'

async def get_weather(city, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if str(data.get('cod')) != '200':
                    return f'Город:{city} не найден!'
                return f'Температура: {data['main']['temp']}°C, Погода: {data['weather'][0]['description']}'
    except Exception as e:
        return f'Ошибка код: {e}'


async def get_weather_random(api_key):
    city = await random_city(api_key)
    if city.startswith('Ошибка'):
        return city
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if str(data.get('cod')) != '200':
                    return f'Город:{city} не найден!'
                return f'В городе: {city}, Температура: {data['main']['temp']}°C, Погода: {data['weather'][0]['description']}'
    except Exception as e:
        return f'Ошибка код: {e}'
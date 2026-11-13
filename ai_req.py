import asyncio

import requests
import os
from dotenv import load_dotenv
import aiohttp
from weather import get_weather_digets
load_dotenv()
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
API_KEY = os.getenv("AI_TOKEN")

async def ai_response(us_mess, city):
    url = "https://api.odirouter.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        'model': 'free-gemini-2.5-pro',
        'messages': [
            {
                    'role':'system',
                    'content': 'Ты советуешь, что надеть зависимо от погоды. Отвечай коротко максимум 2 предложения в которых будет написано, то как одеться'
                },
                {
                    'role':'user',
                    'content':f'{us_mess}'
            }
        ]

    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:

                temp = await get_weather_digets(city, WEATHER_TOKEN)
                if isinstance(temp, (int, float)):
                    if temp >= 25:
                        result='Надень что-то лёгкое, возьми воду'
                    elif 18 <= temp < 25:
                        result= 'Достаточно футболки и джинсов'
                    elif 10 <= temp < 18:
                        result = 'Надень лёгкую куртку или ветровку'
                    elif 0<= temp < 10:
                        result = 'Нужна тёплая куртка и шарф'
                    elif temp < 0:
                        result = 'Надень зимнюю куртку, шапку и перчатки'
                else:
                    result = 'Не удалось получить погоду, оденься по сезону'
                return result
            else:


                try:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                except Exception as e:
                    return f'Ошибка кода: {e}'
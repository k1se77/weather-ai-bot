from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states_for_reg import StatesForReg, Get, Now
from base import DataBase
import os
from dotenv import load_dotenv
from weather import get_weather, random_city, get_weather_random
from ai_req import ai_response
load_dotenv()
db = DataBase()
router = Router()

api_key = os.getenv('WEATHER_TOKEN')
@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, я ПогодаAI помощник!\n'
                         'У меня есть команды:\n'
                         '"/reg_city"-команда для регестрации своего города,\n'
                         'чтобы получать информацию о погоде при нажатии на \n'
                         'и рекомендации как одеться команду "/get_my_city"\n'
                         '(также 10:00 круглосуточно скидывает какая\n'
                         'погода и как лучше одеться)\n'
                         '\n'
                         '"/now_city" - дает информацию о городе, котором попросите\n'
                         '(нажимаешь на кнопку->после вписываешь\n'
                         'город и она выдает погоду с рекомендациями\n'
                         'о том как лучше одеться)\n'
                         '\n'
                         '"/random_city" - команда сделанная ради забавы\n'
                         'Она дает информацию о погоде в рандомном городе\n'
                         'со всей планеты')

@router.message(Command('reg_city'))
async def reg_city(message: Message, state: FSMContext):
    await state.set_state(StatesForReg.city)
    await message.answer('Напишите свой город')

@router.message(StatesForReg.city)
async def fsm_reg_city(message: Message, state: FSMContext):
    await db.save_city(message.text, message.from_user.id)
    await state.update_data(city=message.text)
    await message.answer(f'Город: "{message.text}" сохранен!')
    await state.clear()

@router.message(Command('get_my_city'))
async def get_city(message: Message, state: FSMContext):
    try:
        city = await db.get_city(message.from_user.id)
        if not city:
            await message.answer('Сначала зарегестрируйте свой город, с помощью команды: "/reg_city"')
            return
        response = await get_weather(city, api_key)
        req_ai = await ai_response(response, city)

        await message.answer(f'Город: {city}\n'
                             f'{response}\n'
                             f'Что поэтому говорит ИИ: {req_ai}')

    except Exception as e:
        await message.answer(f'Ошибка кода:{e}')

@router.message(Command('now_city'))
async def now_city(message: Message, state: FSMContext):
    await state.set_state(Now.city)
    await message.answer('Впишите город:')

@router.message(Now.city)
async def fsm_now_city(message: Message, state: FSMContext):
    city = message.text
    try:
        response = await get_weather(city, api_key)
        req_ai = await ai_response(response, city)
        await message.answer(f'В городе {city} погода:{response}\n'
                             f'Что поэтому говорит ИИ: {req_ai}')
    except Exception as e:
        await message.answer(f'ошибка кода:{e}')
    await state.clear()

@router.message(Command('random_city'))
async def cmd_random_city(message: Message):
    weather = await get_weather_random(api_key)
    await message.answer(weather)
from aiogram.fsm.state import State, StatesGroup

class StatesForReg(StatesGroup):
    name = State()
    city = State()

class Get(StatesGroup):
    city = State()

class Now(StatesGroup):
    city = State()
# -*- coding: utf-8 -*-
# module_13_4.py
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = "ABCDEF"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Calories', 'calories', 'CALORIES'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш возраст = {data['age1']}")
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш рост = {data['growth1']}")
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш вес = {data['weight1']} ")
    # Расчёт калорий по формуле Миффлина-Сан Жеора
    w1 = float(data['weight1'])   # Вес
    g1 = float(data['growth1'])   # Рост
    a1 = float(data['age1'])   # Возраст
    calories_male = 10 * w1 + 6.25 * g1 - 5 * a1 + 5
    calories_female = 10 * w1 + 6.25 * g1 - 5 * a1 - 161
    # Выдаём результат вычислений
    await message.answer(f"Расчёт калорий для оптимального похудения или сохранения нормального веса")
    await message.answer(f"по формуле Нефелина-Сан Жеора")
    await message.answer(f"Для мужчины: \n10 * {w1} + 6.25 * {g1} - 5 * {a1} + 5 = {calories_male}")
    await message.answer(f"Для женщины: \n10 * {w1} + 6.25 * {g1} - 5 * {a1} - 161 = {calories_female}")
    await state.finish()


@dp.message_handler()   # Прочие неопознанные сообщения от человека
async def all_message(message):
    await message.answer(message.text)  # Отправим человеку его же сообщение обратно


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
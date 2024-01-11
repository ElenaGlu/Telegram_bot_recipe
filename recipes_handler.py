import aiohttp

import requests
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types

from utils import recipes

router = Router()


class OrderRecipes(StatesGroup):
    waiting_for_recipes = State()

    @router.message(Command("category_search_random"))
    async def category_search_random(message: Message, command: CommandObject, state: FSMContext):
        if command.args is None:
            await message.answer(
                "Ошибка: не переданы аргументы"
            )
            return
        async with aiohttp.ClientSession() as session:
            await state.set_data({'count': int(command.args)})

            builder = ReplyKeyboardBuilder()
            response = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list').json()['meals']
            for d in response:
                for v in d.values():
                    builder.add(types.KeyboardButton(text=str(v)))
                builder.adjust(4)
            await message.answer(f"Выберите категорию:", reply_markup=builder.as_markup(resize_keyboard=True))

            await state.set_state(OrderRecipes.waiting_for_recipes.state)


@router.message(OrderRecipes.waiting_for_recipes)
async def weather_by_date(message: types.Message, state: FSMContext):
    if message is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    async with aiohttp.ClientSession() as session:
        count = await state.get_data()
        category = message.text

        recipe = await recipes(session, category, count)
    await message.answer(recipe)

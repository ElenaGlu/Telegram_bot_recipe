import asyncio
from random import choices

from aiogram.fsm.context import FSMContext
from googletrans import Translator

translator = Translator()


async def recipes(session, state: FSMContext, message):
    count = (await state.get_data())['count']
    async with session.get(url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={message}') as resp:
        data = (await resp.json())['meals']
        selection = choices(data, k=count)
        title_recipes = []
        id_recipes = []
        for d in selection:
            recipe = (translator.translate(d['strMeal'], dest='ru')).text
            title_recipes.append(recipe)
            id_recipes.append(d['idMeal'])

        await state.set_data({'id_recipes': id_recipes})
        return title_recipes


async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()


async def detail(session, state: FSMContext):
    id_recipes = (await state.get_data())['id_recipes']
    fetch_awaitables = [
            fetch(session,
                  f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={el}')
            for el in id_recipes
        ]
    content = await asyncio.gather(*fetch_awaitables)
    await state.set_data({'content': content})





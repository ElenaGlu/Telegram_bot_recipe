import asyncio
from random import choices

from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from googletrans import Translator

translator = Translator()


async def recipes(session, state: FSMContext, message):
    user_data = await state.get_data()
    count = user_data['count']
    async with session.get(url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={message}') as resp:
        data = (await resp.json())['meals']
        selection = choices(data, k=count)
        name_recipe = []
        id_recipe = []
        for d in selection:
            recipe = (translator.translate(d['strMeal'], dest='ru')).text
            name_recipe.append(recipe)
            id_recipe.append(d['idMeal'])

        await state.set_data({'id_recipe': id_recipe})
        return name_recipe


async def fetch(session, url):
    async with session.get(url) as resp:
        # print(resp.status)
        return await resp.json()


async def detail(state: FSMContext):
    user_data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        fetch_awaitables = [
            fetch(session,
                  f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={el}')
            for el in user_data.values()
        ]
        content = await asyncio.gather(*fetch_awaitables)
        await state.set_data({'content': content})





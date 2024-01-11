from random import choices


async def recipes(session, category, count):
    async with session.get(url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}') as resp:
        data = (await resp.json())['meals']
        lst = []
        for d in data:
            for k in d.keys():
                if k == 'strMeal':
                    lst.append(d[k])
        return choices(lst, k=count['count'])

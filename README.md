<p align="center">
  <img src="./assets/shiki4py_logo.svg" alt="Shiki4py" width="35%">
</p>

<p align="center">
  <a href="https://github.com/ren3104/Shiki4py/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ren3104/Shiki4py"></a>
  <a href="https://pypi.org/project/shiki4py"><img src="https://img.shields.io/pypi/v/shiki4py?color=blue" alt="PyPi package version"></a>
  <a href="https://pypi.org/project/shiki4py"><img src="https://img.shields.io/pypi/pyversions/shiki4py.svg" alt="Supported python versions"></a>
</p>

Асинхронный клиент для взаимодействия с [api Shikimori](https://shikimori.one/api/doc/1.0), написанный на Python 3.7 c использованием [asyncio](https://docs.python.org/3/library/asyncio.html) и [aiohttp](https://github.com/aio-libs/aiohttp).

Версии shiki4py v0.2.2 и раньше являются синхронными, но начиная с v2.0.0 этот пакет стал асинхронным. Рекомендую использовать в своих проектах только shiki4py >= v2.0.0!

Сравнение shiki4py v0.2.2 и v2.0.0 по времени отправки 25 запросов:

<img src="https://raw.githubusercontent.com/ren3104/Shiki4py/main/assets/sync_vs_async.svg" alt="Shiki4py sync vs async" width="500">

shiki4py v0.2.2 ~10.5 секунд
<details>
<summary>Код</summary>

```python
from shiki4py import Client


client = Client("APP_NAME",
                "CLIENT_ID",
                "CLIENT_SECRET")
for i in range(25):
    client.get(f"/users/{i}/info")
```
</details>

shiki4py v2.0.0 ~5.07 секунд
<details>
<summary>Код</summary>

```python
from shiki4py import Shikimori
import asyncio


async def main():
    async with Shikimori("APP_NAME", "CLIENT_ID", "CLIENT_SECRET") as api:
        await asyncio.gather(*[api.users.info(i) for i in range(25)])


asyncio.run(main())
```
</details>

## Особенности
* Поддержка api v1 и v2
* Ограничения 5rps и 90rpm
* OAuth2 авторизация
* Контроль срока действия токена
* Хранение токенов в `.env` файле
* Свой класс с методами для каждого ресурса api (пока только для `comments` и `users`)
* Представление json данных как python классы

## Установка
```bash
pip install shiki4py
```

## Использование
### Быстрый старт
```python
from shiki4py import Shikimori
import asyncio
import logging


logging.basicConfig(level=logging.INFO)


async def main():
    # Клиент без авторизации
    async with Shikimori("APP_NAME") as api:
        clubs = await api.users.clubs(555400)
        print(clubs)

    # Клиент с авторизацией
    api = Shikimori("APP_NAME",
                    "CLIENT_ID",
                    "CLIENT_SECRET")
    await api.open()
    # Отправляем запросы
    # await api.client.request(...)
    # await api.users.favourites(...)
    # await api.comments.show_one(...)
    # ...
    await api.close()


asyncio.run(main())
```
### Сохранение токенов авторизации
По умолчанию клиент сохраняет токены авторизации в файле .env, но при инициализации можно выбрать другой вариант хранения токенов, либо создать свой вариант унаследовав базовый класс и переопределив его методы.
```python
from shiki4py import Shikimori
from shiki4py.store import BaseTokenStore
from shiki4py.store.memory import MemoryTokenStore


class MyTokenStore(BaseTokenStore):
    ...


api = Shikimori("APP_NAME",
                "CLIENT_ID",
                "CLIENT_SECRET",
                # store=MyTokenStore()
                store=MemoryTokenStore())
```

## Зависимости
* [aiohttp](https://github.com/aio-libs/aiohttp) - для асинхронных http запросов
* [PyrateLimiter](https://github.com/vutran1710/PyrateLimiter) - для ограничения частоты запросов
* [attrs](https://github.com/python-attrs/attrs) - для преобразования данных json в python классы
* [cattrs](https://github.com/python-attrs/cattrs) - дополнение к attrs для структурирования и деструктурирования данных
* [python-dotenv](https://github.com/theskumar/python-dotenv) - для сохранения токенов авторизации в `.env` файл

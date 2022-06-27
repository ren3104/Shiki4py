# Shiki4py
[![PyPI](https://img.shields.io/pypi/v/shiki4py?color=blue)](https://pypi.org/project/shiki4py)

Клиент для api Shikimori.

Мой профиль на шики https://shikimori.one/Ren3104

## Особенности
* Поддержка api v1 и v2
* Ограничения 5rps и 90rpm
* Система логирования
* OAuth2 авторизация
* Несколько вариантов хранения токенов для авторизации: .ini, .env
* Функция безопасного создания комментариев

## Установка
```bash
pip install shiki4py
```

## Использование
```python
from shiki4py import Client
from pprint import pprint


# Клиент без авторизации
client = Client('APP_NAME')
# Клиент с авторизацией
client = Client('APP_NAME',
                'CLIENT_ID',
                'CLIENT_SECRET')

clubs = client.get('clubs', params={
    'search': 'Детектив Конан'
})

pprint(clubs)
# [{'comment_policy': 'free',
#   'id': 3483,
#   'is_censored': False,
#   'join_policy': 'free',
#   'logo': {'main': '/system/clubs/main/3483.gif?1637694999',
#            'original': '/system/clubs/original/3483.gif?1637694999',
#            'x48': '/system/clubs/x48/3483.gif?1637694999',
#            'x73': '/system/clubs/x73/3483.gif?1637694999',
#            'x96': '/system/clubs/x96/3483.gif?1637694999'},
#   'name': 'Детектив Конан'}]
```
По умолчанию клиент сохраняет токены авторизации в файле конфигурации INI, но при инициализации можно выбрать другой вариант хранения токенов, либо создать свой вариант унаследовав базовый класс и переопределив его методы.
```python
from shiki4py import Client
from shiki4py.store import BaseTokenStore
from shiki4py.store.env import EnvTokenStore


class MyTokenStore(BaseTokenStore):
    ...


client = Client('APP_NAME',
                'CLIENT_ID',
                'CLIENT_SECRET',
                #store=EnvTokenStore()
                store=MyTokenStore())
```

## Зависимости
Обязательные:
* [requests](https://github.com/psf/requests) [>=2.20] - для HTTP запросов
* [requests-ratelimiter](https://github.com/JWCook/requests-ratelimiter) [>=0.3.1] - для ограничения количества запросов

Дополнительные:
* [python-dotenv](https://github.com/theskumar/python-dotenv) [>=0.20.0] - при иморте `shiki4py.store.env` для сохранения токенов авторизации в переменные среды

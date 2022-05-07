# Shiki4py

Тестовая версия клиента для api Shikimori.

Реализовано:
* Поддержка api v1 и v2
* Ограничения 5rps и 90rpm
* Логирование ошибок
* OAuth2 авторизация (Будет обновлено)
* Сохранение токенов (Будет обновлено)
* Авто обновление токена доступа

В планах:
* Безопасное создание комментариев
* Debug логирование
* Вспомогательные функции

Мой профиль на шики https://shikimori.one/3104

## Установка

```bash
pip install shiki4py
```

## Использование

```python
from shiki4py import Client
from pprint import pprint


APP_NAME = 'APP_NAME'
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'


# Клиент без авторизации
client = Client(APP_NAME)
# Клиент с авторизацией
client = Client(APP_NAME, CLIENT_ID, CLIENT_SECRET)

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

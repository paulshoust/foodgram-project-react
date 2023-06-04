[![Django-app workflow](https://github.com/paulshoust/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/paulshoust/foodgram-project-react/actions/workflows/main.yml)


Проект позволяет создавать новые рецепты, добавлять их в избранное, генерировать список покупок, подписываться на авторов рецепта.

Данные superuser для проверки:
login: admin
email: admin@admin.ru
password: 194100

Адрес сервера: http://158.160.28.141

## Технологии

* Django, Postgresql, Nginx, Docker, React.
* Проект размещен в контейнерах Docker.

## Шаблон наполнения .env файла
* Файл .env включает следующие переменные:
	* DB_ENGINE=django.db.backends.postgresql (проект работает с postresql)
	* DB_NAME (название базы данных)
	* POSTGRES_USER (имя пользователя)
	* POSTGRES_PASSWORD (пароль пользователя)
	* DB_HOST (название контейнера, по умолчанию - db)
	* DB_PORT (порт для подключения к БД)
  * SECRET_KEY (секретный код для Django в settings.py)
  * DEBUG_SETTING (всегда False, если только в явной форме не указано как True)

## Запуск приложения в контейнерах
* Клонирование проекта
```bash
git clone git@github.com:paulshoust/foodgram-project-react.git
```

* Параметры загрузки в Docker Hub и разворачивания контейнеров на сервере - в .github/workflows/main.yml

## API

Для управления записями проект использует API.

Документация API доступна по адресу ```http://server/api/docs/```

Примеры запросов:

* Получение списка всех рецептов

**Запрос**: `GET /api/recipes/?page=<integer>&limit=<integer>&is_favorited=1&is_in_shopping_cart=1&author=<integer>&tags=<string>&tags=<string>`

**Ответ (200)**: 
```json
{
  "count": "<integer>",
  "next": "<uri>",
  "previous": "<uri>",
  "results": [
    {
      "tags": [
        {
          "id": "<integer>",
          "name": "<string>",
          "color": "<string>",
          "slug": "vMk5rpoqU"
        },
        {
          "id": "<integer>",
          "name": "<string>",
          "color": "<string>",
          "slug": "wSW1y"
        }
      ],
      "author": {
        "username": "_z",
        "email": "<email>",
        "id": "<integer>",
        "first_name": "<string>",
        "last_name": "<string>",
        "is_subscribed": "<boolean>"
      },
      "is_favorited": "<boolean>",
      "is_in_shopping_cart": "<boolean>",
      "name": "<string>",
      "image": "<string>",
      "text": "<string>",
      "cooking_time": "<integer>",
      "id": "<integer>",
      "ingredients": [
        {
          "name": "<string>",
          "measurement_unit": "<string>",
          "id": "<integer>",
          "amount": "<integer>"
        },
        {
          "name": "<string>",
          "measurement_unit": "<string>",
          "id": "<integer>",
          "amount": "<integer>"
        }
      ]
    },
    {
      "tags": [
        {
          "id": "<integer>",
          "name": "<string>",
          "color": "<string>",
          "slug": "FpgIk5"
        },
        {
          "id": "<integer>",
          "name": "<string>",
          "color": "<string>",
          "slug": "SJ"
        }
      ],
      "author": {
        "username": "-10E7z",
        "email": "<email>",
        "id": "<integer>",
        "first_name": "<string>",
        "last_name": "<string>",
        "is_subscribed": "<boolean>"
      },
      "is_favorited": "<boolean>",
      "is_in_shopping_cart": "<boolean>",
      "name": "<string>",
      "image": "<string>",
      "text": "<string>",
      "cooking_time": "<integer>",
      "id": "<integer>",
      "ingredients": [
        {
          "name": "<string>",
          "measurement_unit": "<string>",
          "id": "<integer>",
          "amount": "<integer>"
        },
        {
          "name": "<string>",
          "measurement_unit": "<string>",
          "id": "<integer>",
          "amount": "<integer>"
        }
      ]
    }
  ]
}
```

## Регистрация новых пользователей
Через админку или через фронт сайта
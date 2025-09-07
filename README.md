# Библиотека API

REST API для управления библиотекой книг на Django + Django REST Framework.

## Описание проекта

Система управления библиотекой с возможностью:
- Просмотра каталога книг и авторов
- Фильтрации и поиска по различным критериям
- Добавления/редактирования контента (только для администраторов)

## Технологический стек

- **Backend**: Django 5.2.6, Django REST Framework 3.16.1
- **База данных**: PostgreSQL (основная) / SQLite (разработка)
- **Аутентификация**: JWT (Simple JWT)
- **Документация**: drf-spectacular (Swagger/OpenAPI)

## Основные возможности

### API Endpoints

#### Книги (`/api/v1/books/`)
- `GET` - Получение списка всех книг
- `GET /{id}/` - Получение конкретной книги
- `POST` - Добавление новой книги (только админы)
- `PUT/PATCH /{id}/` - Редактирование книги (только админы)
- `DELETE /{id}/` - Удаление книги (только админы)

**Доступные фильтры:**
- `?author=1` - фильтр по автору
- `?year=1869` - фильтр по году издания
- `?search=война` - поиск по названию книги
- `?ordering=title` - сортировка по названию (A-Z)
- `?ordering=-title` - сортировка по названию (Z-A)
- `?ordering=year` - сортировка по году
- `?ordering=author__last_name` - сортировка по фамилии автора

#### Авторы (`/api/v1/authors/`)
- `GET` - Получение списка авторов
- `GET /{id}/` - Получение конкретного автора
- `POST` - Добавление автора (только админы)
- `PUT/PATCH /{id}/` - Редактирование автора (только админы)
- `DELETE /{id}/` - Удаление автора (только админы)

**Доступные фильтры:**
- `?search=толстой` - поиск по ФИО автора
- `?ordering=last_name` - сортировка по фамилии

#### Аутентификация
- `POST /api/v1/token/` - Получение JWT токена
- `POST /api/v1/token/refresh/` - Обновление JWT токена

#### Документация
- `/api/v1/docs/` - Swagger UI
- `/api/v1/redoc/` - ReDoc
- `/api/v1/schema/` - OpenAPI схема

## Установка и запуск

### Требования
- Python 3.10+
- PostgreSQL (опционально)

### Локальная разработка

1. **Клонирование репозитория**
```bash
git clone https://github.com/Kotpilota/test_library_api.git
cd test_library_api
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Настройка переменных окружения**
```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Для разработки (SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Для продакшена (PostgreSQL)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=library
# DB_USER=postgres
# DB_PASSWORD=your-password
# DB_HOST=127.0.0.1
# DB_PORT=5432
```

5. **Применение миграций**
```bash
python manage.py migrate
```

6. **Загрузка тестовых данных**
```bash
python manage.py loaddata db.json
```

7. **Создание суперпользователя**
```bash
python manage.py createsuperuser
```

8. **Запуск сервера разработки**
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Примеры использования API

### Получение всех книг
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/"
```

### Фильтрация книг по автору и году
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/?author=1&year=1869"
```

### Поиск книг по названию
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/?search=война"
```

### Сортировка книг по алфавиту (Z-A)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/?ordering=-title"
```

### Получение JWT токена
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/token/" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "your-password"}'
```

### Добавление новой книги (требует аутентификации)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/books/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Новая книга",
       "year": 2024,
       "author_id": 1,
       "preface": "Описание книги"
     }'
```

## Структура проекта

```
mylibrary/
├── api/                    # API приложение
│   └── v1/                # Версия 1 API
│       ├── serializers.py # Сериализаторы DRF
│       ├── views.py       # ViewSets
│       └── urls.py        # URL маршруты
├── library/               # Основные модели
│   ├── models.py         # Модели Author и Book
│   ├── admin.py          # Настройки админки
│   └── migrations/       # Миграции БД
├── users/                # Пользователи
│   ├── models.py        # Кастомная модель User
│   └── admin.py         # Админка пользователей
├── mylibrary/           # Настройки проекта
│   ├── settings.py      # Основные настройки
│   └── urls.py          # Главные URL
├── requirements.txt     # Python зависимости
├── db.json             # Тестовые данные
└── .env.example        # Пример переменных окружения
```

## Оптимизация и масштабирование

### Индексы базы данных
Проект оптимизирован для работы с большими объемами данных:

- **Составные индексы** для частых запросов (автор+год, автор+название)
- **Индексы поиска** для полнотекстового поиска по ФИО и названиям
- **Foreign Key индексы** для быстрых JOIN операций

## Тестовые данные

В проекте предустановлены данные о классических русских писателях:
- 6 авторов (Толстой, Достоевский, Пушкин, Чехов, Тургенев, Гоголь)
- 12 книг с их основными произведениями

## Админ-панель

Доступна по адресу: http://127.0.0.1:8000/admin/

Функции:
- Управление авторами и книгами
- Поиск и фильтрация записей
- Управление пользователями и правами

## Документация API

Интерактивная документация доступна по адресам:
- **Swagger UI**: http://127.0.0.1:8000/api/v1/docs/
- **ReDoc**: http://127.0.0.1:8000/api/v1/redoc/
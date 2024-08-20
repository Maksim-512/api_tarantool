# Tarantool API
___
## Описание
Это решение предоставляет API для работы с базой данных Tarantool. Оно включает в себя Аутентификацию и Авторизацию пользователей, а также методы для записи и чтения данных пачками.

___
## Инструкция по запуску
___
### 1. Клонирование репозитория
Клонируйте репозиторий:
```bash
git clone https://github.com/Maksim-512/api_tarantool.git
```

Перейдите в директорию проекта:
```bash
cd api_tarantool
```

### 2. Установка зависимостей
Создайте виртуальное окружение:
```bash
python3 -m venv venv
```

Активируйте виртуальное окружение:
```bash
source venv/bin/activate
```


### 3. Настройка Tarantool
Соберите контейнеры с помощью Docker Compose:
```bash
docker-compose build
```

Запустите контейнеры:
```bash
docker-compose up
```

___
## API Документация
### 1. Получение токена авторизации
**Описание**: Выполняет аутентификацию пользователя и возвращает JWT-токен.
#### Пример запроса:
```bash
curl -X POST http://localhost:5005/api/login \
-H "Content-Type: application/json" \
-d '{
  "username": "admin",
  "password": "presale"
}'
```

#### Пример ответа:
```bash
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.I-TirsYlzT61pa7ORgE0DVlyyaV2nR9xpj067nnDghg"
}
```

#### Возможные ошибки:
+ **401 Unauthorized**: Неверные учетные данные.

### 2. Запись данных пачками
**Описание**: Записывает данные пачками в базу Tarantool.
#### Пример запроса:
```bash
curl -X POST http://localhost:5005/api/write \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.I-TirsYlzT61pa7ORgE0DVlyyaV2nR9xpj067nnDghg" \
-H "Content-Type: application/json" \
-d '{
  "data": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}'
```

#### Пример ответа:
```bash
{
  "status": "success"
}
```

#### Возможные ошибки:
+ **400 Bad Request**: Нет данных.
+ **500 Internal Server Error**: Ошибка записи данных.
+ **401 Unauthorized**: Недействительный токен.

### 3. Чтение данных пачками
**Описание**: Читает данные пачками из Tarantool по переданным ключам.
#### Пример запроса:
```bash
curl -X POST http://localhost:5005/api/read \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.I-TirsYlzT61pa7ORgE0DVlyyaV2nR9xpj067nnDghg" \
-H "Content-Type: application/json" \
-d '{
  "keys": ["key1", "key2", "key3"]
}'
```

#### Пример ответа:
```bash
{
  "data": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

#### Возможные ошибки:
+ **400 Bad Request**: Нет ключей.
+ **500 Internal Server Error**: Ошибка чтения данных.
+ **401 Unauthorized**: Недействительный токен.

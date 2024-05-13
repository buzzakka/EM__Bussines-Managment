# [EM] Busines Managment
Effective Mobile

## Подготовка к работе
### Установка poetry
- Установите виртуальное окружение командой `python -m venv venv`
- Активируйте виртуальное окружение
    - Для Windows: `venv\Scripts\activate`
    - Для систем Linux: `source venv/bin/activate`
- Установите poetry: `pip install poetry`
- Eстановите все атрибуты `poetry install`
### Подготовка файлов
Создайте следующие файлы с переменными окружения:

**.env**
```bash
MODE=PROD

PG_NAME=postgres
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASS=postgres

REDIS_HOST=localhost
REDIS_PORT=6379
```

Вместо `db_name` и `db_password` укажите имя базы данных и пароль от вашей базы данных соответственно. При необходимости можете также заменить значения других параметров.

### Gодготовка базы данных в PostgreSQL
Создайте базу данных с именем `DB_NAME`, если она не создана, следующей командой:
```bash
CREATE DATABASE db_name;
```
заменив `db_name` на нужное значение.

Внутри базы данных пропишите следующую команду:
```bash
CREATE EXTENSION ltree;
```

## Запуск программы
Для запуска программы в тестовом режиме необходимо воспользоваться командой `uvicorn src.main:app --reload`.

Для запуска Celery воспользуйтесь командой `celery -A src.celery_app.celery_worker:celery worker --loglevel=INFO --pool=solo`

## Тестирование программы
Для тестирования программы создайте файл .test.env со следующим содержимым:

```bash
MODE=TEST

PG_NAME=postgres
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASS=postgres

REDIS_HOST=localhost
REDIS_PORT=6379
```

### Запуск тестов
Тесты запускаются командой `pytest --maxfail=1 -vv -p no:warnings`.
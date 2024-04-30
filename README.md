# [EM] Busines Managment
Effective Mobile

## Подготовка к работе
### .env файл
Создайте файл .env в корневой папке проекта со следующим содержимым:

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

### Создание базы данных в PostgreSQL
Создайте базу данных с именем `DB_NAME`, если она не создана, следующей командой:
```bash
CREATE DATABASE db_name;
```
заменив `db_name` на нужное значение.

### Создание виртуального окружения
- Установка venv: `python -m venv venv`
- Использование venv: `source bin/bash/activate `
- Установка зависимостей: `pip install -r requirements.txt`

## Запуск программы
Для запуска программы в тестовом режиме необходимо воспользоваться командой `uvicorn src.main:app --reload`.

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
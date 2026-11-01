README — Загрузка документов

1. Описание проекта

Это веб-приложение на Python (Flask) для загрузки и хранения документов.
Можно загружать файлы, смотреть список, искать по названию, скачивать и удалять документы.
Информация о файлах хранится в PostgreSQL.

2. Структура проекта

app.py — основная программа Flask.
crud.py — работа с базой данных.
Dockerfile — создание Docker-образа.
compose.yaml — запуск приложения и PostgreSQL.
templates/ — HTML-страницы.
static/ — стили сайта.
uploads/ — загруженные файлы.

Для запуска также нужны requirements.txt, init.sql и .env.

3. Запуск проекта

Нужно установить Docker и открыть терминал в папке проекта.
Создать .env с настройками:

DB_NAME=documents_db
DB_USER=postgres
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key

Запустить:
docker compose up -d --build

Открыть в браузере:
http://localhost:8000

Остановить:
docker compose down

4. Основные маршруты

GET  /                         — главная страница
POST /upload                   — загрузка файла
GET  /documents-list           — список документов
GET  /documents/<name>         — скачивание файла
GET  /documents/<id>/view      — просмотр файла
POST /documents/<id>/delete    — удаление файла
POST /documents/filter         — поиск документов


## 5. Резервное копирование

Для резервного копирования базы данных PostgreSQL используется инструмент `pg_dump`.

В проект добавлен скрипт `backup.py`, который автоматически создаёт резервную копию базы данных.

**Как создать резервную копию:**

1. Запустить Docker-контейнеры:

```bash
docker compose up -d
```

2. Выполнить скрипт:

```bash
python backup.py
```

Резервные копии сохраняются в папке `backups` с указанием даты и времени.

Пример файла:

`backup_2026-11-02_153000.sql`

Для ручного создания резервной копии можно использовать команду:

```bash
docker compose exec -T db pg_dump -U postgres documents_db > backups/backup.sql
```

Папка `backups` должна существовать. Если имя пользователя или базы данных отличается, его нужно изменить в команде.

Резервные копии позволяют сохранить данные и восстановить их при необходимости.

6. Технологии

Python, Flask, PostgreSQL, Docker, HTML и CSS.

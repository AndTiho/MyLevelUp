# MyLevelUp

Бэкенд-часть SPA веб-приложения «Трекер полезных привычек».

---

## 📌 Описание проекта

MyLevelUp — это REST API для управления привычками.  
Проект реализован на Django + Django REST Framework и развернут с использованием Docker и CI/CD.

---

## 🚀 Стек технологий

- Python 3.13
- Django / DRF
- PostgreSQL
- Redis
- Celery + Celery Beat
- Docker / Docker Compose
- Nginx
- GitHub Actions (CI/CD)

---

## 🌍 Развернутое приложение

Приложение доступно по адресу:

http://158.160.79.58

Админ-панель:

http://158.160.79.58/admin/

---

## 🐳 Запуск проекта локально

### 1. Клонирование репозитория

git clone https://github.com/AndTiho/MyLevelUp.git
cd MyLevelUp

### 2. Создание файла `.env`

Создайте файл `.env` в корне проекта:

SECRET_KEY=
DEBUG=False
POSTGRES_DB=
POSTGRES_HOST=db
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=5432
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
STRIPE_API_KEY=
TELEGRAM_TOKEN=
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0


### 3. Запуск через Docker Compose

docker compose up --build

После запуска приложение будет доступно по адресу:

http://localhost

---

## ⚙️ Архитектура проекта

Проект разбит на сервисы:

- web — Django + Gunicorn
- db — PostgreSQL
- redis — брокер сообщений
- celery — обработка фоновых задач
- celery-beat — планировщик задач
- nginx — проксирование и раздача статики

---

## 🔄 CI/CD

В проекте настроен автоматический процесс CI/CD с использованием GitHub Actions.

### Этапы:

1. Линтинг кода (black, flake8)
2. Запуск тестов
3. Сборка Docker-образов
4. Автоматический деплой на сервер

---

## 🚀 Деплой на сервер

Деплой происходит автоматически при push в ветку:

feature/course_project_5

### Что происходит:

- GitHub Actions подключается к серверу по SSH
- Выполняется git pull
- Пересобираются контейнеры
- Перезапускается проект:

docker compose up -d --build

---

## 🖥️ Настройка сервера

Для запуска проекта сервер должен содержать:

- Docker
- Docker Compose
- Клонированный репозиторий проекта
- Настроенный .env файл

### Клонирование проекта на сервер:

git clone https://github.com/AndTiho/MyLevelUp.git
cd MyLevelUp

---

## 📚 Документация API

После запуска доступна:

- Swagger: http://localhost/swagger/
- ReDoc: http://localhost/redoc/

---

## Лицензия

Проект распространяется без лицензии.
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

```
git clone https://github.com/AndTiho/MyLevelUp.git
cd MyLevelUp
```

### 2. Создание файла `.env`

Файл `.env` создается автоматически при деплое.  
Чувствительные данные берутся из GitHub Secrets.

Пример содержимого:

```env
SECRET_KEY=${{ secrets.SECRET_KEY }}
DEBUG=False
POSTGRES_DB=${{ secrets.POSTGRES_DB }}
POSTGRES_USER=${{ secrets.POSTGRES_USER }}
POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_USER=${{ secrets.EMAIL_HOST_USER }}
EMAIL_HOST_PASSWORD=${{ secrets.EMAIL_HOST_PASSWORD }}
STRIPE_API_KEY=${{ secrets.STRIPE_API_KEY }}
TELEGRAM_TOKEN=${{ secrets.TELEGRAM_TOKEN }}
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 3. Запуск через Docker Compose

```
docker compose up --build
```

После запуска приложение будет доступно по адресу:

http://localhost

---

## ⚙️ Архитектура проекта

Проект разбит на сервисы:

- `web` — Django + Gunicorn
- `db` — PostgreSQL
- `redis` — брокер сообщений
- `celery` — обработка фоновых задач
- `celery-beat` — планировщик задач
- `nginx` — проксирование и раздача статики

---

## 🔄 CI/CD

В проекте настроен автоматический процесс CI/CD с использованием GitHub Actions.

### Этапы:

1. Линтинг кода (black, flake8)
2. Запуск тестов
3. Проверка сборки Docker-образов
4. Автоматический деплой на сервер

### Когда происходят проверки

Проверки происходят при:
```
  pull_request:
    branches:
      - develop
      - main
  push:
    branches:
      - develop
      - main
```

### Когда происходит деплой

Деплой выполняется при push в ветку:

```
main
```

### Что делает GitHub Actions

- Подключается к серверу по SSH  
- Обновляет код (`git pull`)  
- Создает/обновляет файл `.env`  
- Перезапускает контейнеры  

Команды деплоя:

```
docker compose down
docker compose up -d --build
```

---

## 🚀 Настройка сервера

Для запуска проекта на сервере должны быть установлены:

- Git
- Docker
- Docker Compose plugin

Остальные сервисы (`PostgreSQL`, `Redis`, `Celery`, `Celery Beat`, `Nginx`, `web`)
запускаются в контейнерах через `docker compose`.

### Установить зависимости

```
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
curl -fsSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker
```

### Проверка

```
docker --version
docker compose version
```

### Клонирование проекта

```
git clone https://github.com/AndTiho/MyLevelUp.git
cd MyLevelUp
```

---

## 🔐 Переменные окружения (.env)

Для локального запуска `.env` создается вручную используя файл `env.exemple`.

При CI/CD деплое `.env` автоматически формируется на сервере из GitHub Secrets.

---

## 🔑 GitHub Secrets

Необходимо добавить в репозиторий:

- `SSH_KEY`
- `SERVER_USER`
- `SERVER_IP`
- `SECRET_KEY`
- `DEBUG`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`

Дополнительно (если используется):

- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `STRIPE_API_KEY`
- `TELEGRAM_TOKEN`

---

## 🖥️ Проверка деплоя

### Подключение к серверу

```
ssh <user>@<server_ip>
```

### Перейти в проект

```
cd /home/<user>/MyLevelUp
```

### Проверить контейнеры

```
docker compose ps
```

Должны быть запущены (все UP):

- web
- db
- redis
- celery
- celery-beat
- nginx

### Логи

```
docker compose logs -f
```

или:

```
docker compose logs -f web
```

---

## 🌐 Проверка работы

Открыть в браузере:

- http://<server_ip>
- http://<server_ip>/admin/

Если всё открывается — деплой успешен.

---

## 📚 Документация API

- http://<server_ip>/swagger/
- http://<server_ip>/redoc/

---

## 📄 Лицензия

Проект распространяется без лицензии.
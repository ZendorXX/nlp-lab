# Лабораторная работа 2: NLP

Ибрагимов Роман Рифхатович, М8О-403Б-22

## Условие

Задание на Четверку

— Бизнес-задача

Заказчик — провайдер сотовой связи. В рамках повышения удержания пользователей открыта
инициатива исследования борьбы со спамом в СМС посредством LLM технологий. Ваша задача —
предложить proof-of-concept прототип, иллюстрирующий применимость LLM к распознаванию спама.

— Инженерно-исследовательская задача
1. Обязательная инженерная часть (LLM-сервис):
- a) Поднять Docker контейнер от любого Ubuntu+Python базового образа (не slim версии).
Например с python:3.12.16-ubuntu22.04
- b) Развернуть внутри контейнера сервер ollama с моделью Qwen2.5:0.5B
- d) Протестировать работоспособность обращений к серверу ollama через терминал
- e) Собрать сервис на FastAPI внутри контейнера, оборачивающий ollama сервер одним
эндпоинтом на пересылку запросов и возвращение ответов.
- f) Сконфигурировать контейнер для проброса порта FastAPI вовне. Например внутри docker-
compose.yml (потребуется перезапуск контейнера)
- g) Протестировать работоспособность LLM-сервиса.

— Стек
1. Docker
2. FastAPI
3. Ollama
4. Qwen2.5:0.5B

— Требования
1. Docker контейнер с проброшенными портами на сервер ollama
2. Инференс Qwen2.5:0.5B на сервере ollama, слушающий и отвечающий на запросы по HTTP
3. Скрипт вне контейнера, отправляющий запросы (curl или requests) на сервер ollama для LLM
модели внутри контейнера
4. Dosctring документация всех функций

## Что реализовано

1. Docker-контейнер на базе `ubuntu:22.04` (не slim) с установленным Python внутри.
2. Ollama-сервер внутри контейнера.
3. Загрузка и инференс модели `qwen2.5:0.5b`.
4. FastAPI-обертка с endpoint `POST /generate`.
5. Проброс портов наружу:
   - `11434` (прямой доступ к Ollama);
   - `8000` (FastAPI).
6. Внешние скрипты проверки с хост-машины.
7. Docstring-документация для всех функций Python.

## Структура проекта

- `Dockerfile`
- `docker-compose.yml`
- `app/main.py`
- `app/ollama_client.py`
- `scripts/test_ollama_outside.py`
- `scripts/test_fastapi_outside.py`
- `requirements.txt`
- `start.sh`

## Требования к окружению

- Docker Engine
- Docker Compose plugin (`docker compose`)
- Python 3.10+ на хосте (для внешних скриптов)

Проверка:

```bash
docker --version
docker compose version
```

## Пошаговый запуск и проверка

### 1) Запуск контейнера

```bash
docker compose up --build
```

Дождитесь логов:
- `Starting Ollama server...`
- `Pulling model qwen2.5:0.5b...`
- `Starting FastAPI...`

Примечание: первый запуск может занять заметное время из-за загрузки модели.

### 2) Проверка HTTP endpoints (в новом терминале)

Проверка Ollama:

```bash
curl http://localhost:11434/api/tags
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:0.5b",
    "prompt": "Определи, является ли сообщение спамом: Вы выиграли приз, перейдите по ссылке",
    "stream": false
  }'
```

Проверка FastAPI:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Определи, является ли сообщение спамом: Срочно перейдите по ссылке и получите бонус"}'
```

### 3) Подготовка хост-окружения для Python-скриптов

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Проверка внешними Python-скриптами (с хоста)

Скрипт `scripts/test_ollama_outside.py` поддерживает 3 режима:

1. Интерактивный произвольный запрос:
```bash
python3 scripts/test_ollama_outside.py
```

2. Произвольный запрос через аргумент:
```bash
python3 scripts/test_ollama_outside.py --prompt "Определи, является ли сообщение спамом: Получите бонус по ссылке"
```

3. Batch-режим на 10 заготовленных сообщений:
```bash
python3 scripts/test_ollama_outside.py --batch10
```

В batch-режиме скрипт выводит для каждого из 10 сообщений:
- отправленный текст (`Sent message`)
- ответ сервера (`Response`)

Скрипт `scripts/test_fastapi_outside.py` поддерживает те же режимы:

1. Интерактивный произвольный запрос:
```bash
python3 scripts/test_fastapi_outside.py
```

2. Произвольный запрос через аргумент:
```bash
python3 scripts/test_fastapi_outside.py --prompt "Определи, является ли сообщение спамом: Получите бонус по ссылке"
```

3. Batch-режим на 10 заготовленных сообщений через LLM-сервис:
```bash
python3 scripts/test_fastapi_outside.py --batch10
```

Ожидаемый результат: скрипты выводят `Model: qwen2.5:0.5b` и текст ответа модели.

## Остановка

```bash
docker compose down
```
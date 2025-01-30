# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем зависимости для Redis и Poetry
RUN apt-get update && apt-get install -y \
    build-essential && \
    apt-get clean

ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_HTTP_TIMEOUT=100

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы для установки зависимостей
COPY pyproject.toml poetry.lock ./
# COPY pyproject.toml poetry.lock README.md ./

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false && poetry install --only main --no-root
# RUN poetry install --only main --no-root


# Копируем оставшиеся файлы проекта
COPY . .

# Копируем файл .env
COPY .env /app/.env

# Указываем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Экспортируем порт
EXPOSE 8000

# Команда для запуска сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

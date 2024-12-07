# Используем официальный Python-образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev musl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry для управления зависимостями
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Собираем статические файлы
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

RUN python manage.py collectstatic --noinput

# Открываем порт для Django
EXPOSE 8000

# Указываем команду по умолчанию для запуска контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

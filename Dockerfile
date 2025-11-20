# Используем нормальный образ Python (не slim)
FROM python:3.12.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для сборки бинарников (PostgreSQL client, gcc, и т.д.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock /app/

# Ставим все зависимости через uv
RUN pip install uv==0.8.13
RUN uv sync --frozen --no-cache

# Копируем весь проект
COPY . /app/

# Прокидываем порт
EXPOSE 8000

# Запуск через gunicorn
CMD ["uv", "run", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind=0.0.0.0:8000"]
    
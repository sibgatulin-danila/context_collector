# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Предотвращаем создание .pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаём рабочую директорию
WORKDIR /context_collector

# Создаём непривилегированного пользователя
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY . .

# Устанавливаем venv и зависимости
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    /venv/bin/pip install -e .

# Делаем виртуальную среду доступной через PATH
ENV PATH="/venv/bin:$PATH"

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8008

# Запускаем приложение
CMD ["bash"]

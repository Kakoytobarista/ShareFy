FROM python:3.11 as requirements-stage

WORKDIR /app
COPY . /app
COPY .env /app/

# Создаем папку Dev и перемещаем app
RUN mkdir /Dev && mv /app /Dev

# Устанавливаем зависимости
WORKDIR /Dev/app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Устанавливаем uvicorn и fastapi
RUN pip install uvicorn
RUN pip install fastapi

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/Dev/app


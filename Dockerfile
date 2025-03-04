FROM python:3.13-slim
LABEL maintainer="asgefes1@gmail.com"

ENV PYTHONDOWNTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

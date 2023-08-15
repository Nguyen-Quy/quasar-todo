FROM python:3.10 AS backend

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8888

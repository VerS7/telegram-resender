FROM python:3.13-alpine

WORKDIR /app

COPY . .

RUN apk update && apk add tzdata && apk add ca-certificates

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

ENV TZ="Europe/Moscow"

ENTRYPOINT [ "python", "./src/main.py" ]
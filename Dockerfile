FROM python:alpine3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY simpleproxy/requirements.txt /app/requirements.txt

RUN apk --update add --virtual build-base \
&& pip3 install --no-cache-dir -r /app/requirements.txt \
&& apk del build-base

COPY simpleproxy /app/

EXPOSE 8080

ENTRYPOINT python app.py

# BUILDER
FROM python:3.8-alpine as builder
LABEL stage=builder

WORKDIR /usr/src/app

ENV PYTHONDONOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

COPY . /usr/src/app/
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# FINAL
FROM python:3.8-alpine

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME && mkdir $APP_HOME/static \
    && mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apk update && apk add libpq sudo jpeg-dev zlib-dev libjpeg
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN chown -R app:app $APP_HOME && chown -R app:app $HOME
RUN sudo -H pip install --upgrade pip \
    && sudo -H pip install --no-cache /wheels/*

COPY . $APP_HOME
COPY ./foodgram/.env $APP_HOME/foodgram/.env
RUN chown -R app:app $APP_HOME

USER app
RUN ./manage.py collectstatic --no-input
CMD gunicorn foodgram.wsgi:application --bind 0:8000
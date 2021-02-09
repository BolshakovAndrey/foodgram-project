FROM python:3.8.5 
 
LABEL name='Foodgram - Yandex Practicum' version=3.1
 
WORKDIR /code 
 
COPY requirements.txt .
 
RUN pip install -r requirements.txt 
 
COPY . .
 
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
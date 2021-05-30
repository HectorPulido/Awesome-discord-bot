FROM ubuntu:18.04

# set work directory
RUN mkdir /app
WORKDIR /app

COPY . .

# install dependencies
RUN apt-get update && apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt

# set environment variables
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

RUN useradd -m myuser
USER myuser

RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn discord_bot.wsgi:application --bind 0.0.0.0:$PORT
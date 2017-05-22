#!/usr/bin/env bash


git pull origin master
docker-compose build
docker-compose stop
docker-compose up -d
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
docker-compose exec app python manage.py loaddata initial_data.json

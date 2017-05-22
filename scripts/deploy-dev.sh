#!/usr/bin/env bash

git checkout develop
git pull
docker-compose build
docker-compose stop
docker-compose up -d
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput

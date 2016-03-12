#!/bin/bash
echo 'switching to prod env'
eval "$(docker-machine env production)"
docker-compose build
docker-compose -f production.yml up -d
docker-compose run --rm web python manage.py collectstatic --noinput
docker-compose restart
echo 'Done'
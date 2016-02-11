echo 'switching to local env'
eval "$(docker-machine env default)"
docker-compose build
docker-compose -f docker-compose.yml up -d
docker-compose run --rm web python manage.py collectstatic --noinput
docker-compose restart
echo 'Done'

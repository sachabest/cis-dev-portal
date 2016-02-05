echo 'switching to prod env'
eval "$(docker-machine env production)"
docker-compose build
docker-compose -f production.yml up -d
docker-compose run web /usr/local/bin/python manage.py migrate
eval "$(docker-machine env default)"
echo 'switching back to local env'

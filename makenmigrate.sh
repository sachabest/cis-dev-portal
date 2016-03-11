docker-compose run --rm web bash -c "python manage.py makemigrations && python manage.py migrate auth && python manage.py migrate" 

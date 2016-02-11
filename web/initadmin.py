from django.contrib.auth.models import User
User.objects.create_superuser('sachab', 'sachab@seas.upenn.edu', 'fuckwithme')
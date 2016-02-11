from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=255)
	client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	pm_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class Event(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField('Start Time')
	end_date = models.DateTimeField('End Time')
	owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class SiteApp(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=100)
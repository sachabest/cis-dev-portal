from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from annoying.fields import AutoOneToOneField

# Create your models here.

class Student(models.Model):
    user = AutoOneToOneField(User, primary_key=True)
    github_token = models.CharField(max_length=100)
    github_username = models.CharField(max_length=50)
    major = models.CharField(max_length=5)
    year = models.IntegerField()
    avatar = models.CharField(max_length=255)
    jira_username = models.CharField(max_length=50)
    jira_token = models.CharField(max_length=100)
    jira_token_secret = models.CharField(max_length=100)

class Project(models.Model):
	name = models.CharField(max_length=255)
    number = models.IntegerField()
	client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_client_user+')
	pm_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_pm_user+')

class Event(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField('Start Time')
	end_date = models.DateTimeField('End Time')
	owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner_user+')

class OAuthState(models.Model):
    key = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauthstate_user+')
    active_flag = models.BooleanField(default=False)

class SecretKeyState(models.Model):
    key = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secretkeystate_user+')
    active_flag = models.BooleanField(default=False)
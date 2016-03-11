from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Event, Project, Student
# Register your models here.

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class StudentInline(admin.StackedInline):
    model = Student

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(Project)
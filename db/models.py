import os
import sys

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
from django.conf import settings
# if not settings.configured:
#     settings.configure(DATABASES=my_settings.DATABASES, DEBUG=True)
#     settings.configure(INSTALLED_APPS=my_settings.INSTALLED_APPS, DEBUG=True)
django.setup()

try:
    from django.db import models
except Exception:
    print("Exception: Django Not Found, please install it with \"pip install django\".")
    sys.exit()


class Location(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "location"


class Department(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "department"


class Team(models.Model):
    name = models.CharField(max_length=50)
    dept = models.ForeignKey(Department, db_column='dept_id', blank=True, null=True)

    class Meta:
        db_table = "team"


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    job_title = models.CharField(max_length=64, blank=True, null=True)
    team = models.ForeignKey(Team, db_column='team_id', null=True, blank=True)
    dept = models.ForeignKey(Department, db_column='dept_id', null=True, blank=True)
    location = models.ForeignKey(Location, db_column='location_id', null=True, blank=True)
    avatar_url = models.TextField(blank=True, null=True)
    manager = models.ForeignKey("self", db_column='manager_id', null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    fun_facts = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    udemy_user_id = models.IntegerField()
    created = models.DateField()
    modified = models.DateField()

    class Meta:
        db_table = "employee"

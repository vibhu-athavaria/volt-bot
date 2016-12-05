import os
import sys
import csv
import django
from datetime import datetime

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import *

headline = [
    'full_name', 'first_name', 'office_phone', 'last_name', 'nick_name', 'email', 'mobile', 'start_date',
    'job_title', 'bio', 'skills', 'interest', 'my_job', 'team', 'birthday', 't_shirt_size', 'team_old',
    'udemy_user_id', 'last_seen', 'updated', 'created', 'avatar_url', 'manager_email', 'department',
    'location', 'facebook', 'github', 'twitter', 'linkedin'
]


def parse_for_locations(csv_file_path, update_db=False):
    locations = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,
             _, _, _, _, _, _, _, location, _, _, _, _) = row

            location = location.strip()

            if location and location not in locations:
                if location is "HQ":
                    location = "San Francisco"
                locations.append(location)
                print(location)
                if update_db:
                    Location.objects.create(name=location)


def parse_for_departments(csv_file_path, update_db=False):
    departments = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,
             _, _, _, _, _, _, department, _, _, _, _, _) = row

            department = department.strip()

            if department and department not in departments:
                departments.append(department)
                print(department)
                if update_db:
                    Department.objects.create(name=department)


def parse_for_teams(csv_file_path, update_db=False):
    teams = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            (_, _, _, _, _, _, _, _, _, _, _, _, _, team, _, _, _,
             _, _, _, _, _, _, department, _, _, _, _, _) = row

            team = team.strip()

            if team and team not in teams:
                teams.append(team)
                print(team)
                if update_db:
                    try:
                        dept = Department.objects.get(name=department.strip())
                        Team.objects.create(name=team, dept=dept)
                    except Department.DoesNotExist:
                        Team.objects.create(name=team)


def parse_for_employee(csv_file_path, update_db=False):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            (_, first_name, _, last_name, _, email, _, start_date,
             job_title, bio, _, _, _, team_name, birthday, _, _,
             udemy_user_id, _, updated, created, avatar_url, manager_email, department_name,
             location_name, _, _, _, _) = row
            try:
                manager = Employee.objects.get(email=manager_email.strip())
            except Employee.DoesNotExist:
                manager = None

            try:
                team = Team.objects.get(name=team_name.strip())
            except Team.DoesNotExist:
                team = None

            try:
                dept = Department.objects.get(name=department_name.strip())
            except Department.DoesNotExist:
                dept = None

            try:
                location = Location.objects.get(name=location_name.strip())
            except Location.DoesNotExist:
                location = None

            if start_date:
                start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
            else:
                start_date = None

            if birthday:
                birthday = datetime.strptime(birthday, "%m/%d/%Y").date()
            else:
                birthday = None

            created = datetime.strptime(created, "%m/%d/%Y").date()
            updated = datetime.strptime(updated, "%m/%d/%Y").date()

            print("{first_name}\t{last_name}\t{email}\t{job_title}\t{team}\t{dept}\t{location}\t{avatar_url}"
                  "\t{manager}\t{birthday}\t{start_date}\t{fun_facts}"
                  "\t{bio}\t{udemy_user_id}\t{created}\t{updated}".format(
                first_name=first_name,
                last_name=last_name,
                email=email,
                job_title=job_title,
                team=team,
                dept=dept,
                location=location,
                avatar_url=avatar_url,
                manager=manager,
                birthday=birthday,
                start_date=start_date,
                fun_facts=None,
                bio=bio,
                udemy_user_id=udemy_user_id,
                created=created,
                updated=updated
            ))
            if update_db:
                Employee.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    job_title=job_title,
                    team=team,
                    dept=dept,
                    location=location,
                    avatar_url=avatar_url,
                    manager=manager,
                    birthday=birthday,
                    start_date=start_date,
                    fun_facts=None,
                    bio=bio,
                    udemy_user_id=udemy_user_id,
                    created=created,
                    modified=updated
                )


def update_manager_data(csv_file_path, update_db=False):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            (_, first_name, _, last_name, _, email, _, start_date,
             job_title, bio, _, _, _, team_name, birthday, _, _,
             udemy_user_id, _, updated, created, avatar_url, manager_email, department_name,
             location_name, _, _, _, _) = row

            employee = Employee.objects.get(email=email.strip())
            if not employee.manager:
                try:
                    manager = Employee.objects.get(email=manager_email.strip())
                except Employee.DoesNotExist:
                    manager = None

                if manager:
                    print("Updating {} manager information: {}", employee.first_name, manager.first_name)
                    if update_db:
                        employee.manager = manager
                        employee.save()


def parse_csv(csv_file_path, update_db=False):
    parse_for_locations(csv_file_path, update_db)
    parse_for_departments(csv_file_path, update_db)
    parse_for_teams(csv_file_path, update_db)
    parse_for_employee(csv_file_path, update_db)

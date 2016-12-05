from db.models import *
from constant import *


def get_employee_info(employee_name):
    split_name = employee_name.split(' ')
    first_name = split_name[0]
    last_name = None
    length = len(split_name)
    if length > 1:
        last_name = ' '.join(split_name[1:length])

    team_members = Employee.objects.filter(first_name__iexact=first_name)
    if last_name:
        team_members = team_members.filter(last_name__iexact=last_name)
    return team_members.select_related('manager', 'team')


def get_team_info(team_name):
    team = Team.objects.filter(name=team_name)
    if team.exists():
        team_members = Employee.objects.filter(team=team.first())
        return team_members.select_related('manager', 'team')

    return Employee.objects.none()


def get_dept_info(dept_name):
    dept = Department.objects.filter(name=dept_name)
    if dept.exists():
        dept_members = Employee.objects.filter(team=dept.first())
        return dept_members.select_related('manager', 'team')

    return Employee.objects.none()


def get_team_list():
    return Team.objects.all().values_list('name', flat=True).order_by('name')


def get_department_list():
    return Department.objects.all().values_list('name', flat=True).order_by('name')


def get_upcoming_birthday():
    pass

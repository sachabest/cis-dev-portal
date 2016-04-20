import csv, logging
from .models import Student, Project
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def parse_input_csv(csv_file_wrapper, project_file_wrapper):
    '''
    Takes in raw text and outputs json for group information.

    Expected format of project_file:
    Name / Number / PM PennKey / Customer PennKey

    Expected format of csv_file:
    Name / Class / PennKey / Major / Team # 
    '''
    new_projects = {}
    new_students = []
    data = csv.reader(project_file_wrapper.read().decode(encoding='UTF-8').splitlines())
    for row in data:
        project_number = int(row[1])
        username = row[2] + "@upenn.edu"
        customer_username = row[3] + "@upenn.edu"
        try:
            pm_user = User.objects.get(username=username)
        except:
            pm_user = User(username=username)
        try:
            customer_user = User.objects.get(username=customer_username)
        except:
            customer_user = User(username=customer_username)
        pm_user.save()
        customer_user.save()
        try:
            new_project = Projects.objects.get(number=project_number)
        except:
            new_project = Project(name=row[0], number=project_number, pm_user=pm_user, \
                client_user=customer_user)
        new_project.save()
        # set pm_user and customer_user later
        new_projects[project_number] = new_project

    data = csv.reader(csv_file_wrapper.read().decode(encoding='UTF-8').splitlines())
    project_mapping = {}
    for row in data:
        username = row[2] + "@upenn.edu"
        try:
            student = User.objects.get(username=username)
        except:
            student = User(username=username)
            student.first_name = "Not"
            student.last_name = "Registered"
            student.save()
            student.student = Student()
        student.student.year = row[1]
        student.student.major = row[3]
        student.student.save()
        student.save()
        # add code here to find if the PM user exists
        project_number = int(row[4])
        new_project = new_projects[project_number]
        student.student.project = new_project
        student.student.save()
        if project_number not in project_mapping:
            project_mapping[project_number] = []
        project_mapping[project_number].append(student)

    return (new_projects.values(), project_mapping)
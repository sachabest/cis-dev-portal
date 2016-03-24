import csv
from .models import Student, Project
from django.contrib.auth.models import User

def parse_input_csv(csv_file, project_file):
    '''
    Takes in raw text and outputs json for group information.

    Expected format of project_file:
    Name / Number / PM PennKey / Customer PennKey

    Expected format of csv_file:
    Name / Class / PennKey / Major / Team # 
    '''
    new_projects = {}
    new_students = []

    with open(project_file, 'r') as project_file_wrapper:
        reader = csv.reader(csv_file_wrapper)
        for row in reader:
            project_number = int(row[1])
            username = row[3] + "@upenn.edu"
            customer_username = row[4] + "@upenn.edu"
            pm_user = User(username=username)
            customer_user = User(username=customer_username)
            new_project = Project(name=row[0], number=project_number, pm_user=pm_user, \
                customer_user=customer_user)
            new_projects[project_number] = new_project

    with open(csv_file, 'r') as csv_file_wrapper:
        reader = csv.reader(csv_file_wrapper)
        for row in reader:
            student = User()
            student.student = Student()
            student.student.displayName = "Not Registered"
            student.student.year = row[1]
            student.username = row[2] + "@upenn.edu"
            student.student.major = row[3]

            # add code here to find if the PM user exists
            project_number = int(row[4])
            new_project = new_projects[project_number]
            student.student.project = new_project

    return new_projects.value()
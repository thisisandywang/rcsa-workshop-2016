from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Student

class Command(BaseCommand):
    help = "This command checks to see if there are any name conflicts in the students."

    def handle(self, *args, **options):


        students = list(Student.objects.all())
        name_conflicts = {}

        for student in students:
            last_name = student.last_name
            first_name = student.first_name
            email = student.email

            same_last_name = []
            for other_student in students:
                if last_name == other_student.last_name and email != other_student.email:
                    same_last_name.append(other_student)

            same_names = []
            if same_last_name:
                for other_student in same_last_name:
                    if other_student.first_name == first_name:
                        same_names.append(other_student)

            if same_names:
                same_names.append(student)
                name_conflicts[first_name + " " + last_name] = same_names

            students.remove(student)
        if name_conflicts:
            for name in name_conflicts.keys():
                people = name_conflicts[name]
                print("This name: " + name + " has " + str(len(people)) + " people with the same name")
                emails = ""
                for person in people:
                    emails = emails + person.email + ","
                print(emails[:-1] + "\n")

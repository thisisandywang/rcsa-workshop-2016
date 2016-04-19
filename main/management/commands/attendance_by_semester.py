from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Student, Event

import csv

class Command(BaseCommand):
    help = "This command takes in a semester <Fall/Spring> <Year> and creates a csv file \
            of students and the number of events they attended"

    def handle(self, *args, **options):
        year = int(args[1])
        semester = args[0].lower()
        if (semester == "spring"):
            months = range(1, 6)
        elif (semester == "fall"):
            months = range(7, 13)
        else:
            raise ValueError("That's not a semester. Choose spring or fall")
        print(months)
        #output_file = csv.writer(open(semester + str(year) + "_Attendance", 'wb'), dialect='excel')
        output_file = open(semester + str(year) + "_Attendance", 'wb')
        students = {}
        events = Event.objects.all()
        for event in events:
            if ((event.date.month in months and int(event.date.year) == year)):
                print(event.name, event.date.month, event.date.year, '\n')
                for s in event.attendees.all():
                    if s in students:
                        students[s] += 1
                    else:
                        students[s] = 1

        for s in students:
            output_file.write(s.last_name + "\t" + s.first_name + "\t"+ str(students[s]) + "\n")
            print("Wrote student: " + s.first_name + s.last_name)

        output_file.close()

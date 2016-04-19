from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event, Student

import csv

class Command(BaseCommand):
    help = "This command saves all of the students into a excel style csv file. \
            It takes one argument: the name of the file you want to write to."

    def handle(self, *args, **options):
        """
        This command will save events in the following manner:
        Each event will be on its own line with its attribures separated by commas.
        Each event has a name, location, date, and whether or not it's eligible for
        house points.
        """
        csv_file_name = args[0]

        csv_file = csv.writer(open(csv_file_name, 'wb'), dialect='excel')

        students = Student.objects.all()

        for student in students:
            s_first_name = student.first_name
            s_last_name = student.last_name
            s_email = student.email
            s_year = student.year
            s_sid = student.sid
            s_house = student.house

            # Write the wrote
            csv_file.writerow([s_first_name, s_last_name, s_email, s_year, s_sid, s_house])

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Student

import csv


class Command(BaseCommand):
    help = "This command populates the database from a excel csv\
            file taken as the first argument"

    def handle(self, *args, **options):
        """
        Right now, this reads in a csv file for the roster with the order
        of last name, first name, email, year, extra info, and then house.

        If the student already exists in the database, then it updates its house.
        """
        roster_file = args[0]

        # Create a reader for the csv file
        roster = csv.reader(open(roster_file, 'rb'), dialect='excel')

        # Add each student from the roster
        for student in roster:
            first_name = student[0].strip().title()
            last_name = student[1].strip().title()
            email = student[2].strip().lower()
            year = student[3].strip()
            sid = student[4].strip()
            house = student[5].strip()

            print("Acquired: " + first_name + " " + last_name + "; " + email + "; " + house + "; " + year)

            # First, let's check to see if this person is already in the database
            try:
                existing_student = Student.objects.get(email=email)
                student_exists = True
            except ObjectDoesNotExist:
                student_exists = False


            if not student_exists:
                # Let's execute the SQL command
                # The order of the columns for main_student is first name, last name,
                # email address, and then house
                new_student = Student(first_name=first_name,
                                                    last_name=last_name,
                                                    email=email,
                                                    house=house,
                                                    year=year,
                                                    sid=sid)

                # Save the student
                new_student.save()

                print("Saved: " + first_name + " " + last_name + "; " + email + "; " + house + "; " + year)
                
            else: # Update house
                house_old = existing_student.house
                if house_old != house:
                    existing_student.house = house
                    existing_student.save()
                    print("Updated house from {0} to {1}".format(house_old, house))    
                print("Was Already There: " + first_name + " " + last_name + "; " + email + "; " + house + "; " + year)

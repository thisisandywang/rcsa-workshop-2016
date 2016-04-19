from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event, Student

import csv

class Command(BaseCommand):
    help = "This command extracts event attendance from the current sqlite3 database  \
            and writes it to a excel-like csv file. It takes one argument: the name \
            of the csv file you want to write to."

    def handle(self, *args, **options):
        """
        This command will extract event attendance from an sqlite3 database,
        and it will write it to a csv file for later integration into other
        databases or spreadsheets. It will do so as an excel csv, which means
        that there are no quotes or anything--just information separated by
        commas.

        To properly use this, you must have the database you want to extract from
        be the current database. The settings should be configured for an sqlite3
        database as well.
        """

        csv_file_name = args[0]

        # Create a writer for the csv file.
        csv_file = csv.writer(open(csv_file_name, 'wb'), dialect='excel')

        # Get all of the events
        events = Event.objects.all()

        for event in events:
            event_name = event.name
            attendees = event.attendees.all()

            print("Acquired event: " + event_name)

            for attendee in attendees:
                csv_file.writerow([event_name, attendee.email])
                print("Added student: " + attendee.first_name + " " +
                    attendee.last_name + "; " + attendee.email + "; at event: " + event_name)
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event, Student

import csv

class Command(BaseCommand):
    help = "This command populates the database with attendees for events from a csv file. \
            It takes one argument: the name of the file to read from."

    def handle(self, *args, **options):
        """
        This command will populate the database with a csv file folloiwng
        the format of event name, email.

        This command assumes the event is already in the database.
        """

        event_file = args[0]

        # Create a reader for the csv file
        event_csv = csv.reader(open(event_file, 'rb'), dialect='excel')

        for attendance in event_csv:
            event_name = attendance[0].strip()
            attendee_email = attendance[1].strip()

            print("Event: " + event_name + "; Attendee: " + attendee_email)

            try:
                event = Event.objects.get(name=event_name)
            except ObjectDoesNotExist:
                print("Event: " + event_name + " does not exist.")
                continue

            try:
                attendee = Student.objects.get(email=attendee_email)
                event.attendees.add(attendee)
            except ObjectDoesNotExist:
                print("Attendee: " + attendee_email + " does not exist.")
                with open("wrong_email", 'a') as f:
                    f.write(attendee_email + "\n")
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event, Student

import csv

class Command(BaseCommand):
    help = "This command populates the database with events from a csv file. \
            It takes one argument: the name of the file to read from."

    def handle(self, *args, **options):
        """
        This command assumes that the csv file follows the format of:
        event name, event location, event date, and event house points
        eligibility.
        """

        event_file = args[0]

        event_csv = csv.reader(open(event_file, 'rb'), dialect='excel')

        for event in event_csv:
            event_name = event[0].strip()
            event_location = event[1].strip()
            event_date = event[2].strip()
            event_house_points = event[3].strip()

            # Create the event
            new_event = Event(name=event_name,
                              location=event_location,
                              date=event_date,
                              house_points=event_house_points)

            # Save the event
            new_event.save()

            print("Event was saved: {0},{1},{2},{3}".format(event_name,
                                                            event_location,
                                                            event_date,
                                                            event_house_points))
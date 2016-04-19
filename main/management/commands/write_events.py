from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event

import csv

class Command(BaseCommand):
    help = "This command saves all of the events into a excel style csv file. \
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

        events = Event.objects.all()

        for event in events:
            event_name = event.name
            event_location = event.location
            event_date = event.date
            event_house_points = event.house_points

            # Write the wrote
            csv_file.writerow([event_name, event_location, event_date, event_house_points])

            print("Wrote event: {0}, {1}, {2}, {3}".format(event_name,
                                                         event_location,
                                                         event_date,
                                                         event_house_points))
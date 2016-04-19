ffrom django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import HousePointsOther

import csv

class Command(BaseCommand):
    help = "This command populates the database with events from a csv file. \
            It takes one argument: the name of the file to read from."

    def handle(self, *args, **options):
        """
        This command assumes that the csv file follows the format of:
        house points other event name, description, and the points
        earned by each house.
        """

        hpo_file = args[0]

        hpo_csv = csv.reader(open(hpo_file, 'rb'), dialect='excel')

        for hpo in hpo_csv:
            hpo_name = hpo[0].strip()
            hpo_description = hpo[1].strip()
            hpo_points_R = hpo[2].strip()
            hpo_points_C = hpo[3].strip()
            hpo_points_S = hpo[4].strip()
            hpo_points_A = hpo[5].strip()

            # Create the event
            new_hpo = HousePointsOther(name=hpo_name,
                            description=hpo_name, points_R=hpo_points_R,
                            points_C=hpo_points_C, points_S=hpo_points_S,
                            points_A = hpo_points_A)

            # Save the event
            new_hpo.save()

            print("HousePointsOther was saved: {0}, {1}, {2}, {3}, {4}, {5}".format(hpo_name,
                                                         hpo_description,
                                                         hpo_points_R,
                                                         hpo_points_C,
                                                         hpo_points_S,
                                                         hpo_points_A))
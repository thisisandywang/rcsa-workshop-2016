from django.core.management.base import BaseCommand, CommandError
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

        csv_file_name = args[0]

        csv_file = csv.writer(open(csv_file_name, 'wb'), dialect='excel')

        hpos = HousePointsOther.objects.all()

        for hpo in hpos:
            hpo_name = hpo.name
            hpo_description = hpo.description
            hpo_points_R = hpo.points_R
            hpo_points_C = hpo.points_C
            hpo_points_S = hpo.points_S
            hpo_points_A = hpo.points_A

            # Create the event
            new_hpo = HousePointsOther(name=hpo_name,
                            description=hpo_name, points_R=hpo_points_R,
                            points_C=hpo_points_C, points_S=hpo_points_S,
                            points_A = hpo_points_A)

            # Write the wrote
            csv_file.writerow([hpo_name, hpo_description, hpo_points_R, hpo_points_C,
                                hpo_points_S, hpo_points_A])

            print("Wrote HousePointsOther: {0}, {1}, {2}, {3}, {4}, {5}".format(hpo_name,
                                                         hpo_description,
                                                         hpo_points_R,
                                                         hpo_points_C,
                                                         hpo_points_S,
                                                         hpo_points_A))
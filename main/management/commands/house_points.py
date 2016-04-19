from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Event, Student, HousePointsOther
from main.views import get_house_points


class Command(BaseCommand):
    help = "This command calculates the total number of house points for each house"

    def handle(self, *args, **options):
        """
        This command calculates the house points for Rockefeller, Chavez, Savio,
        and Apperson. It does so by relying upon the existence of a house
        attribute for each Student instance. It will caclulate the total number
        of house points based on the events so far.
        """

        r_points, c_points, s_points, a_points = get_house_points()

        print("Rockefeller has {0} points".format(r_points))
        print("Chavez has {0} points".format(c_points))
        print("Savio has {0} points".format(s_points))
        print("Apperson has {0} points".format(a_points))
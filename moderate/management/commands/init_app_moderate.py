from django.core.management.base import BaseCommand

from moderate.tests.scenario import default_moderate_state


class Command(BaseCommand):

    help = "Initialise 'moderate' application"

    def handle(self, *args, **options):
        default_moderate_state()
        print "Initialised 'moderate' app..."

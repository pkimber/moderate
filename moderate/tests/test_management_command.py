from django.test import TestCase

from moderate.management.commands import init_app_moderate


class TestCommand(TestCase):

    def test_init_app(self):
        """ Test the management command """
        command = init_app_moderate.Command()
        command.handle()

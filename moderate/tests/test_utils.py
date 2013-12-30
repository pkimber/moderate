from django.test import TestCase

from login.tests.scenario import (
    get_user_staff,
    get_user_web,
)


class PermTestCase(TestCase):

    def assert_any(self, url):
        """all users (logged in or not) should have access to this url"""
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "status {}: everyone should have access to '{}'".format(
                response.status_code, url
            )
        )

    def assert_logged_in(self, url):
        self._assert_no_perm(url)
        self._assert_web(url)

    def assert_staff_only(self, url):
        """only members of staff should have access to this URL"""
        self._assert_no_perm(url)
        self._assert_no_web(url)
        self._assert_staff(url)

    def _assert_no_perm(self, url):
        """a user who is not logged in should not have access to this URL"""
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: no user login - "
            "so should not have access to '{}'".format(
                response.status_code, url
            )
        )

    def _assert_no_web(self, url):
        """a user who is logged in should not have access to this url"""
        user = self._login_web()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, user.username, url
            )
        )

    def _assert_staff(self, url):
        staff = get_user_staff()
        self.client.login(
            username=staff.username, password=staff.username
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "status {}: staff user '{}' should have access "
            "to this url: '{}'".format(
                response.status_code, staff.username, url
            )
        )

    def _assert_web(self, url):
        """check that a logged in user can view the url"""
        user = self._login_web()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "status {}: web user '{}' (logged in) should have access "
            "to this url: '{}'".format(
                response.status_code, user.username, url
            )
        )

    def _login_web(self):
        web = get_user_web()
        self.client.login(
            username=web.username, password=web.username
        )
        return web

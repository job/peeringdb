import pytest
import json

from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import Group

import peeringdb_server.models as models

# from django.template import Context, Template
# from django.utils import translation


class UserLocaleTests(TestCase):
    """
    Test peeringdb_server.models.User functions
    """

    @classmethod
    def setUpTestData(cls):
        user_group = Group.objects.create(name="user")
        for name in ["user_undef", "user_en", "user_pt"]:
            setattr(
                cls,
                name,
                models.User.objects.create_user(
                    name,
                    "%s@localhost" % name,
                    first_name=name,
                    last_name=name,
                    password=name,
                ),
            )

        cls.user_en.set_locale("en")
        cls.user_pt.set_locale("pt")

        user_group.user_set.add(cls.user_en)
        user_group.user_set.add(cls.user_pt)
        user_group.user_set.add(cls.user_undef)

        cls.user_undef.save()
        cls.user_en.save()
        cls.user_pt.save()

    def setUp(self):
        self.factory = RequestFactory()

    def test_user_locale(self):
        """
        Tests if user profile page has the right language

        Note: Don't use Client.login(...) since it will miss language setting in the session
        """

        # t = Template("{% load i18n %}{% get_current_language as LANGUAGE_CODE %}{{ LANGUAGE_CODE }}")
        # print(t.render(Context({})))
        # translation.activate('pt')
        # print(t.render(Context({})))
        # u_pt = models.User.objects.get(username="user_pt")
        # print(u_pt.get_locale())

        c = Client()
        resp = c.get("/profile", follow=True)
        data = {"next": "/profile", "username": "user_en", "password": "user_en"}
        resp = c.post("/auth", data, follow=True)
        self.assertGreater(resp.content.find("<!-- Current language: en -->"), -1)

        c.logout()
        data = {"next": "/profile", "username": "user_pt", "password": "user_pt"}
        resp = c.post("/auth", data, follow=True)
        self.assertGreater(resp.content.find("<!-- Current language: pt -->"), -1)

        c.logout()
        data = {"next": "/profile", "username": "user_undef", "password": "user_undef"}
        resp = c.post("/auth", data, follow=True)
        self.assertGreater(resp.content.find("<!-- Current language: en -->"), -1)

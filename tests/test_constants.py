# -*- coding: utf-8 -*-

from django.test import TestCase

from mongoengine.connection import DEFAULT_CONNECTION_NAME
from mongo_connection.constants import DEFAULT_ALIAS


class ConstantsTestCase(TestCase):

    def test_default_alias(self):
        self.assertEqual(DEFAULT_ALIAS, DEFAULT_CONNECTION_NAME)

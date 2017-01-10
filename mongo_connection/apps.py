# -*- coding: utf-8 -*-

from django.apps import AppConfig

from . import connections


class MongoConnectionConfig(AppConfig):
    name = 'mongo_connection'
    label = 'mongo_connection'

    def ready(self):
        """
        Reload all mongo connections.
        """
        connections.reload_all()

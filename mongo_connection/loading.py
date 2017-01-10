# -*- coding: utf-8 -*-

import threading

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from mongoengine import connect
from mongoengine.connection import _connections, disconnect

from .constants import DEFAULT_ALIAS


class ConnectionHandler(object):
    """
    Manage connections for the local thread.
    """

    def __init__(self, connections_info):
        self.connections_info = connections_info
        self.thread_local = threading.local()

    def __getitem__(self, item):
        if not hasattr(self.thread_local, 'connections'):
            self.thread_local.connections = {}
        elif item in self.thread_local.connections:
            return self.thread_local.connections[item]

        self.ensure_defaults(item)
        self.thread_local.connections[item] = ConnectionWrapper(using=item)
        return self.thread_local.connections[item]

    def all(self):
        return [self[alias] for alias in self.connections_info]

    def ensure_defaults(self, alias):
        try:
            self.connections_info[alias]
        except KeyError:
            raise ImproperlyConfigured('The key "%s" isn\'t an available connection.' % alias)

    def reload(self, alias):
        if not hasattr(self.thread_local, 'connections'):
            self.thread_local.connections = {}
        try:
            del self.thread_local.connections[alias]
        except KeyError:
            pass

        return self.__getitem__(alias)

    def reload_all(self):
        for alias in settings.MONGO_CONNECTIONS.keys():
            self.reload(alias)


class ConnectionWrapper(object):

    def __init__(self, using=None):
        self.using = using or DEFAULT_ALIAS
        self.options = settings.MONGO_CONNECTIONS.get(self.using, {})
        self._connection = None

        # Make an initial connection
        self.connect()

    @property
    def is_connected(self):
        return self._connection is not None and self.using in _connections

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connect()
        return self._connection

    def connect(self):
        self._connection = connect(alias=self.using,
                                   tz_aware=settings.USE_TZ,
                                   db=self.options.get('NAME', None),
                                   host=self.options.get('HOST', None),
                                   port=self.options.get('PORT', None),
                                   username=self.options.get('USERNAME', None),
                                   password=self.options.get('PASSWORD', None))
        return self.connection

    def reset_connection(self):
        disconnect(self.using)
        self._connection = None

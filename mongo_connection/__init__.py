# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .constants import DEFAULT_ALIAS
from .loading import ConnectionHandler

__title__ = 'django-mongo-connection'
__version__ = '0.0.1a'
__author__ = 'Rolf Haavard Blindheim'
__license__ = 'MIT License'

VERSION = __version__


default_app_config = 'mongo_connection.apps.MongoConnectionConfig'

if not hasattr(settings, 'MONGO_CONNECTIONS'):
    raise ImproperlyConfigured('The MONGO_CONNECTIONS setting is required.')

if DEFAULT_ALIAS not in settings.MONGO_CONNECTIONS:
    raise ImproperlyConfigured('The default alias "%s" must be included '
                               'in the MONGO_CONNECTIONS setting.' % DEFAULT_ALIAS)

# Load connections
connections = ConnectionHandler(settings.MONGO_CONNECTIONS)

# django-mongo-connection

[![Build Status](https://travis-ci.org/inonit/django-mongoengine-connection.svg?branch=master)](https://travis-ci.org/inonit/django-mongoengine-connection)
[![Coverage Status](https://coveralls.io/repos/github/inonit/django-mongoengine-connection/badge.svg?branch=master)](https://coveralls.io/github/inonit/django-mongoengine-connection?branch=master)


Simple Mongoengine connection wrapper for Django.

## Setup

Set up Mongo connections in `settings.py`

```
MONGO_CONNECTIONS = {
    'default': {
        'NAME': 'default',  # Hostname or URI. If using URI, it will override all other options.
        'HOST': os.environ.get('MONGO_HOST', 'localhost')
    }
}
```

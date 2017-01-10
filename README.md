# django-mongo-connection

[![Build Status](https://travis-ci.org/inonit/django-mongo-connection.svg?branch=master)](https://travis-ci.org/inonit/django-mongo-connection)
[![Coverage Status](https://coveralls.io/repos/github/inonit/django-mongo-connection/badge.svg?branch=master)](https://coveralls.io/github/inonit/django-mongo-connection?branch=master)


Simple Mongoengine connection wrapper for Django.

## Installation

```
$ pip install django-mongo-connection
```

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

## Usage

Now you can define and query your documents as usual. 
No need to manually manage Mongo connections.

See the [official documentation](http://docs.mongoengine.org/) for more info on how to use mongoengine.

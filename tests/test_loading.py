# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from mongoengine.connection import _connections, get_connection

from mongo_connection.loading import ConnectionHandler, ConnectionWrapper


class ConnectionHandlerTestCase(TestCase):

    def test_class_init(self):
        handler = ConnectionHandler({})
        self.assertEqual(handler.connections_info, {})

        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })
        self.assertEqual(handler.connections_info, {
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })

    def test_get_all_connections(self):
        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            },
            'other': {
                'NAME': 'other',
                'HOST': 'localhost'
            }
        })

        for wrapper in map(lambda e: repr(e).strip('<>').split(' object at ')[0], handler.all()):
            self.assertEqual(wrapper, 'mongo_connection.loading.ConnectionWrapper')

    def test_get_item(self):
        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })
        wrapper = handler['default']
        self.assertIsInstance(wrapper, ConnectionWrapper)

    def test_get_item_same_instance(self):
        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })

        # Make sure we get the same item when getting by same alias
        path1, address1 = repr(handler['default']).strip('<>').split(' object at ')
        path2, address2 = repr(handler['default']).strip('<>').split(' object at ')
        self.assertEqual(path1, path2)
        self.assertEqual(address1, address2)

    def test_get_item_invalid_alias(self):
        handler = ConnectionHandler({})
        try:
            handler['default']
            self.fail('Did not fail when trying to get a non-existing connection alias.')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The key "default" isn\'t an available connection.')

    def test_reload(self):
        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })

        # Make sure we get a new object when reloaded
        self.assertNotEqual(handler['default'], handler.reload('default'))

    def test_reload_invalid_alias(self):
        handler = ConnectionHandler({
            'default': {
                'NAME': 'default',
                'HOST': 'localhost'
            }
        })

        try:
            handler.reload('slave')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The key "slave" isn\'t an available connection.')
        else:
            self.fail('Should fail with ImproperlyConfigured when reloading an invalid alias.')


@override_settings(MONGO_CONNECTIONS={
    'default': {
        'NAME': 'default',
        'HOST': 'localhost',
    }
})
class ConnectionWrapperTestCase(TestCase):

    def test_is_connected_by_default(self):
        wrapper = ConnectionWrapper(using='default')
        self.assertTrue(wrapper.is_connected)

    def test_reset_connection(self):
        wrapper = ConnectionWrapper(using='default')
        wrapper.reset_connection()
        self.assertFalse(wrapper.is_connected)

    def test_connect(self):
        wrapper = ConnectionWrapper(using='default')
        wrapper.reset_connection()
        self.assertFalse(wrapper.is_connected)

        wrapper.connect()
        self.assertTrue(wrapper.is_connected)

    def test_automatic_reconnect_when_reading_property(self):
        wrapper = ConnectionWrapper(using='default')

        wrapper.reset_connection()
        self.assertFalse(wrapper.is_connected)

        wrapper.connection
        self.assertTrue(wrapper.is_connected)

    def test_wrapper_register_connection(self):
        wrapper = ConnectionWrapper(using='default')
        self.assertTrue(wrapper.using in _connections)
        self.assertEqual(get_connection(wrapper.using), wrapper.connection)

import logging

logger = logging.getLogger(__name__)

from unittest import TestCase
from senpy.api import parse_params, API_PARAMS, NIF_PARAMS, WEB_PARAMS
from senpy.models import Error


class APITest(TestCase):

    def test_api_params(self):
        """The API should not define any required parameters without a default"""
        parse_params({}, API_PARAMS)

    def test_web_params(self):
        """The WEB should not define any required parameters without a default"""
        parse_params({}, WEB_PARAMS)

    def test_basic(self):
        a = {}
        try:
            parse_params(a, NIF_PARAMS)
            raise AssertionError()
        except Error:
            pass
        a = {'input': 'hello'}
        p = parse_params(a, NIF_PARAMS)
        assert 'input' in p
        b = {'i': 'hello'}
        p = parse_params(b, NIF_PARAMS)
        assert 'input' in p

    def test_plugin(self):
        query = {}
        plug_params = {
            'hello': {
                'aliases': ['hello', 'hiya'],
                'required': True
            }
        }
        try:
            parse_params(query, plug_params)
            raise AssertionError()
        except Error:
            pass
        query['hello'] = 'world'
        p = parse_params(query, plug_params)
        assert 'hello' in p
        assert p['hello'] == 'world'
        del query['hello']

        query['hiya'] = 'dlrow'
        p = parse_params(query, plug_params)
        assert 'hello' in p
        assert 'hiya' in p
        assert p['hello'] == 'dlrow'

    def test_default(self):
        spec = {
            'hello': {
                'required': True,
                'default': 1
            }
        }
        p = parse_params({}, spec)
        assert 'hello' in p
        assert p['hello'] == 1

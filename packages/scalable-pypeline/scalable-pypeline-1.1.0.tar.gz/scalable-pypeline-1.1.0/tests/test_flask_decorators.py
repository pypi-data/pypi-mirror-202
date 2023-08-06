""" Test Flask Decorator methods
"""
import os
from importlib import reload
import responses
import mock
from pypeline import constants
from pypeline.flask import decorators
from pypeline.flask.decorators import validate_access_key
from pypeline.constants import DEFAULT_BASE_URL, AUTH_LOCK_KEY


class TestFlaskDecoratorsNonLocal:
    """ Test classes in flask/decorators.py in a CLOUD environment where the
        DEFAULT_BASE_URL != 'local'

        TODO Make the updated default base url process more repeatable through
        either a setup/teardown mechanism or some reusable code we can use
        in other tests instead of this copy/paste stuff. Also used in
        tests/test_sermos_deploy.py
    """
    @responses.activate
    def test_auth_lock(self, mock_redis):
        """ Verify proper access and caching behavior for auth decorator when
            against a valid /auth API endpoint.
        """
        fake_redis = mock.patch.object(decorators, 'redis_conn', mock_redis)
        with fake_redis:
            # Patch the /auth endpoint
            api_url = DEFAULT_BASE_URL + 'auth'
            responses.add(responses.POST, url=api_url, json={})

            # No lock set
            lock_key = mock_redis.get(AUTH_LOCK_KEY)
            assert lock_key is None

            # Granted access due to 200 response from the /auth api (mocked)
            valid = validate_access_key(access_key='123')
            assert valid is True

            # Lock was set, re-request and validate still true
            lock_key = mock_redis.get(AUTH_LOCK_KEY)
            valid = validate_access_key(access_key='123')
            assert lock_key is not None
            assert valid is True

            mock_redis.flushall()  # Clear lock

            # No api key provided and not in environment
            valid = validate_access_key(access_key=None)
            assert valid is False

            with mock.patch.dict(os.environ, {'SERMOS_ACCESS_KEY': 'foobar'}):
                # No access key provided but is set in environment
                valid = validate_access_key(access_key=None)
                assert valid is True

        mock_redis.flushall()

    @responses.activate
    def test_auth_401(self, mock_redis):
        """ Verify behavior when /auth endpoint returns a 401
        """
        fake_redis = mock.patch.object(decorators, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = DEFAULT_BASE_URL + 'auth'

            # Access with key but server sent a 401
            responses.add(responses.POST, url=api_url, json={}, status=401)
            valid = validate_access_key(access_key='123')
            assert valid is False
        mock_redis.flushall()


class TestFlaskDecoratorsLocal:
    """ Test classes in flask/decorators.py when in default test environment
        with DEFAULT_BASE_URL='local'
    """
    def test_auth_lock_local_env(self):
        """ Verify we're always gtg in local mode
        """
        # Run test with a 'local' base url
        with mock.patch.dict(os.environ, {'SERMOS_BASE_URL': 'local'}):
            reload(constants)
            reload(decorators)
            from pypeline.constants import DEFAULT_BASE_URL  # Re-import

            # Default test environment should have 'local' as the DEFAULT_BASE_URL
            # and therefore validate any key including None
            assert DEFAULT_BASE_URL == 'local'
            assert validate_access_key(access_key='123') is True
            assert validate_access_key(access_key=None) is True

        # Ensure we reset constants and decorators back to the default
        # for this test environment.
        reload(constants)
        reload(decorators)

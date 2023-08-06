""" Test sermos configuration utilities
"""
import os
import re
import mock
import json
import time
from importlib import reload
from urllib.parse import urljoin
from types import ModuleType
import pytest
import responses
from pypeline.flask import FlaskSermos
from pypeline.utils.config_utils import load_json_config_from_redis, \
    set_json_config_to_redis, _generate_api_url, get_access_key, \
    _retrieve_and_cache_config, retrieve_latest_pipeline_config, \
    retrieve_latest_schedule_config
from pypeline.utils import config_utils
from pypeline import constants, sermos_yaml
from pypeline.constants import DEFAULT_BASE_URL
from pypeline.schedule_config_schema import ScheduleSchemaV1

DEPLOYMENT_ID = os.environ.get('SERMOS_DEPLOYMENT_ID')


class TestConfigStoreRetrieve:
    """ Test utilities for pipeline/schedule configurations
    """
    def test_set_retrieve_refresh_key(self, mock_redis):
        """ Verify setting and retrieval of a key using helper methods
        """
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            key = load_json_config_from_redis('nonexistant')
            assert key is None

            data_dict = {'foo': 'bar'}
            set_json_config_to_redis('exists', data_dict)
            key = load_json_config_from_redis('exists')
            assert key == data_dict

            mock_redis.flushall()

    def test_get_access_key_not_in_env(self):
        """ Basic test for helper method
        """
        # Assert key error when no key in environment and none passed
        with pytest.raises(KeyError):
            access_key = get_access_key()

        # Returned as provided
        access_key = get_access_key('foobarbaz')
        assert access_key == 'foobarbaz'

    @mock.patch.dict(os.environ, {'SERMOS_ACCESS_KEY': 'foobar'})
    def test_get_access_key_in_env(self):
        """ Basic test for helper method when set in environment
        """
        # Assert key retrieved from environment when none passed explicitly
        access_key = get_access_key()
        assert access_key == 'foobar'

    def test_generate_api_url(self):
        """ Generate a joined api url
        """
        expected_url =\
            DEFAULT_BASE_URL + f'deployments/{DEPLOYMENT_ID}/pipelines'
        api_url = _generate_api_url(endpoint='pipelines')
        assert api_url == expected_url

    @responses.activate
    def test__retrieve_and_cache_config(self, mock_redis):
        """ Test the helper method for retrieving from api and cache
        """
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = 'https://foo.bar/api/baz'
            key = 'test_cache_key'

            responses.add(responses.GET, url=api_url, json={})
            data = _retrieve_and_cache_config(key=key,
                                              admin_api_endpoint=api_url,
                                              access_key='foo',
                                              refresh_rate=1)

            assert data == {}  # Provided empty response

            with open('tests/fixtures/api/demo_pipeline_conf.json', 'r') as f:
                resp = json.loads(f.read())

            responses.reset()
            responses.add(responses.GET, url=api_url,
                          json=resp)  # Ensure API returns an actual config now

            data = _retrieve_and_cache_config(key=key,
                                              admin_api_endpoint=api_url,
                                              access_key='foo')
            assert data == {}  # Still empty from initial cached value of {}

            time.sleep(1)  # wait for cache to expire

            data = _retrieve_and_cache_config(key=key,
                                              admin_api_endpoint=api_url,
                                              access_key='foo')

            assert data == resp  # Now it's re-retrieved from API

            mock_redis.flushall()

    @responses.activate
    def test_retrieve_latest_pipeline_config(self, mock_redis):
        """ Retrieve latest pipeline configuration from provided Admin endpoint
        """
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='pipelines')
            test_admin_pipeline_id = 'foo'

            with open('tests/fixtures/api/demo_pipeline_conf.json', 'r') as f:
                resp = json.loads(f.read())

            responses.add(responses.GET,
                          url=urljoin(api_url + '/', test_admin_pipeline_id),
                          json=resp)

            pipeline_config = retrieve_latest_pipeline_config(
                pipeline_id=test_admin_pipeline_id, access_key='foo')

            assert pipeline_config == resp['data']

            mock_redis.flushall()

    @responses.activate
    def test_retrieve_latest_schedule_config(self, mock_redis):
        """ Retrieve latest schedule configuration from provided Admin endpoint
        """
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='scheduled_tasks')

            with open('tests/fixtures/api/demo_schedule_conf.json', 'r') as f:
                resp = json.loads(f.read())

            responses.add(responses.GET, url=api_url, json=resp)

            schedule_config = retrieve_latest_schedule_config(access_key='foo')
            for schedule in schedule_config:
                del schedule['id']

            schema = ScheduleSchemaV1(many=True)
            expected = schema.load(resp['data']['results'])
            assert schedule_config == expected

            mock_redis.flushall()


# TODO update to pull from local sermos.yaml file
# TODO update the api fixtures for pipeline and schedule configuration to match
#      new format
# TODO update API endpoints to ensure they are sending expected format
# TODO ensure in coordination between sermos and sermos admin for API responses
class TestConfigStoreRetrieveLocal:
    """ Test utilities for pipeline/schedule configurations when in LOCAL mode
    """
    def test_retrieve_latest_pipeline_config(self, mock_redis):
        """ Retrieve latest pipeline configuration from LOCAL file system
        """
        # Run test with a 'local' base url
        with mock.patch.dict(
                os.environ, {
                    'SERMOS_BASE_URL': 'local',
                    'SERMOS_CLIENT_PKG_NAME': 'pypeline',
                    'SERMOS_YAML_PATH':
                    '../tests/fixtures/configs/sermos-valid.yaml'
                }):
            reload(constants)
            reload(config_utils)
            reload(sermos_yaml)
            from pypeline.constants import DEFAULT_BASE_URL  # Re-import

            fake_redis = mock.patch.object(config_utils, 'redis_conn',
                                           mock_redis)
            with fake_redis:
                with open('tests/fixtures/api/demo_pipeline_conf.json',
                          'r') as f:
                    resp = json.loads(f.read())

                pipeline_config = retrieve_latest_pipeline_config(
                    pipeline_id='demo-pipeline', access_key='foo')

                del resp['data']['results'][0]['id']
                del resp['data']['results'][0]['added_datetime']
                del resp['data']['results'][0]['changed_datetime']
                assert pipeline_config == resp['data']['results'][0]

        # Ensure we reset constants back to the default for this test env
        reload(constants)
        reload(config_utils)
        reload(sermos_yaml)
        mock_redis.flushall()

    def test_retrieve_latest_schedule_config(self, mock_redis):
        """ Retrieve latest schedule configuration from LOCAL file system
        """
        # Run test with a 'local' base url
        with mock.patch.dict(
                os.environ, {
                    'SERMOS_BASE_URL': 'local',
                    'SERMOS_CLIENT_PKG_NAME': 'pypeline',
                    'SERMOS_YAML_PATH':
                    '../tests/fixtures/configs/sermos-valid.yaml'
                }):
            reload(constants)
            reload(config_utils)
            reload(sermos_yaml)
            from pypeline.constants import DEFAULT_BASE_URL  # Re-import

            fake_redis = mock.patch.object(config_utils, 'redis_conn',
                                           mock_redis)
            with fake_redis:
                api_url = _generate_api_url(endpoint='scheduled_tasks')

                with open('tests/fixtures/api/demo_schedule_conf.json',
                          'r') as f:
                    resp = json.loads(f.read())

                responses.add(responses.GET, url=api_url, json=resp)

                schedule_config = retrieve_latest_schedule_config(
                    access_key='foo')

                for result in resp['data']['results']:
                    del result['id']
                assert schedule_config == resp['data']['results']

        # Ensure we reset constants back to the default for this test env
        reload(constants)
        reload(config_utils)
        reload(sermos_yaml)
        mock_redis.flushall()

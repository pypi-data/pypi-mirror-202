""" Test API utilities
"""
import json
from urllib.parse import urljoin
import mock
import responses
from celery.canvas import Signature, chord, _chain
from pypeline.utils.config_utils import _generate_api_url
from pypeline.flask.api.utils import chain_helper
from pypeline.utils import config_utils
from pypeline.constants import CHAIN_SUCCESS_MSG


class TestUtilsApi:
    """ Test classes in api/utils.py
    """
    with open('tests/fixtures/api/demo_pipeline_conf_single.json', 'r') as f:
        pipeline_config = json.loads(f.read())

    pipeline_id = 'simple-pipeline'
    api_url = _generate_api_url('pipelines')
    api_url = urljoin(api_url + '/', pipeline_id)  # Add pipeline ID

    @responses.activate
    def test_chain_helper_with_retry(self, mock_redis):
        """ Test get_execution_graph()
        """
        responses.add(responses.GET,
                      url=self.api_url,
                      json=self.pipeline_config)
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            gen = chain_helper(self.pipeline_id, access_key='foo')
            assert type(gen.chain) == _chain
            assert type(gen.chain.tasks[0]) == chord
            assert gen.loading_message == CHAIN_SUCCESS_MSG
            mock_redis.flushall()

    @responses.activate
    def test_chain_helper_without_retry(self, mock_redis):
        """ Test get_execution_graph()
        """
        responses.add(responses.GET,
                      url=self.api_url,
                      json=self.pipeline_config)
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            gen = chain_helper(self.pipeline_id,
                               access_key='foo',
                               add_retry=False)
            assert type(gen.chain) == _chain
            assert type(gen.chain.tasks[0]) == chord
            assert gen.loading_message == CHAIN_SUCCESS_MSG

            # Verify that retry logic was NOT added
            assert gen.chain.options.get('link_error', None) is None

            mock_redis.flushall()

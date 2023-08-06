""" Test utils/utils_task.py
"""
import os
import time
from importlib import reload
from urllib.parse import urljoin
import mock
import pytest
import responses
from marshmallow.exceptions import ValidationError
from networkx.classes.digraph import DiGraph
from celery.canvas import Signature, chord, _chain
from pypeline.utils import config_utils
from pypeline.utils.config_utils import _generate_api_url
from pypeline.utils.task_utils import PipelineRunWrapper, PipelineGenerator
from pypeline.utils import config_utils
from pypeline.utils.graph_utils import get_execution_graph
from pypeline.pipeline_config_schema import PipelineConfigValidator
from pypeline import constants, sermos_yaml
from pypeline.constants import DEFAULT_TASK_TTL,\
    DEFAULT_REGULATOR_TASK, DEFAULT_BASE_URL


class TestUtilsTask:
    """ Test classes in task_utils.py
    """

    pipeline_id = 'simple-pipeline'

    def test_pipeline_config_validator(self, pipeline_configs):
        """ Ensure pipeline validation is working as expected
        """
        validated = PipelineConfigValidator(
            config_dict=pipeline_configs['simple_pipeline'])
        assert validated.is_valid is True

        with pytest.raises(AttributeError):
            validated = PipelineConfigValidator(config_yaml={})

        with pytest.raises(ValidationError):
            validated = PipelineConfigValidator(config_dict="foo bar baz")
            assert validated.is_valid is False
            validation_error = {'_schema': ['Invalid input type.']}
            assert validated.validation_errors == validation_error

    def test_pipeline_run_wrapper_basics(self, mock_redis, pipeline_configs):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=pipeline_configs['simple_pipeline'])
            assert pipeline_wrapper.pipeline_id == self.pipeline_id
            assert pipeline_wrapper.execution_id is not None
            assert pipeline_wrapper.execution_id != '123'  # Should be random
            assert pipeline_wrapper.max_ttl == 60
            assert pipeline_wrapper.max_retry == 3
            assert pipeline_wrapper.retry_count == 0
            assert pipeline_wrapper.chain_payload == {}

            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id='hitl-pipeline',
                pipeline_config=pipeline_configs['hitl_pipeline'])
            assert pipeline_wrapper.max_ttl == 60
            pipeline_wrapper.load()
            assert pipeline_wrapper.max_ttl == 3600

            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=pipeline_configs['simple_pipeline'],
                execution_id='123')
            assert pipeline_wrapper.pipeline_id == self.pipeline_id
            assert pipeline_wrapper.execution_id is not None
            assert pipeline_wrapper.execution_id == '123'  # Should be set
            assert pipeline_wrapper.cache_key == 'sermos_simple-pipeline_123'

            assert pipeline_wrapper.dag_config is None  # Haven't loaded it yet
            assert pipeline_wrapper.execution_graph is None  # Not loaded yet

            chain_payload = {'custom_key1': 'val1', 'custom_key2': 'val2'}
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=pipeline_configs['simple_pipeline'],
                chain_payload=chain_payload)
            assert pipeline_wrapper.chain_payload == chain_payload

            assert pipeline_wrapper.dag_config is None  # Haven't loaded it yet
            assert pipeline_wrapper.execution_graph is None  # Not loaded yet

            mock_redis.flushall()

    def test_pipeline_run_wrapper_caching(self, mock_redis, pipeline_configs):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            # Verify caching and max_ttl behavior
            chain_payload = {'custom_key1': 'val1', 'custom_key2': 'val2'}
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id='customer-short-pipeline',
                pipeline_config=pipeline_configs['customer_short_pipeline'],
                execution_id='123',
                chain_payload=chain_payload)
            assert pipeline_wrapper.dag_config is None  # Not yet loaded
            assert pipeline_wrapper.chain_payload == chain_payload
            pipeline_wrapper.load()  # Loaded and cached
            assert pipeline_wrapper.max_ttl is 1
            assert pipeline_wrapper.dag_config is not None  # Config now exists

            # Get it again and manually load from cache - should still exist
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id='customer-short-pipeline',
                pipeline_config=pipeline_configs['customer_short_pipeline'],
                execution_id='123')
            assert pipeline_wrapper.dag_config is None
            pipeline_wrapper._load_from_cache()
            assert pipeline_wrapper.dag_config is None
            assert pipeline_wrapper.chain_payload == chain_payload  # cached

            pipeline_wrapper.load()
            assert pipeline_wrapper.dag_config is not None

            # Get it again after exceeding ttl, should no longer exist in cache
            time.sleep(1)  # Exceed ttl
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id='customer-short-pipeline',
                pipeline_config=pipeline_configs['customer_short_pipeline'],
                execution_id='123')
            assert pipeline_wrapper.dag_config is None
            pipeline_wrapper.load()
            assert pipeline_wrapper.dag_config is not None

            mock_redis.flushall()

    def test_pipeline_run_wrapper_graph(self, mock_redis, pipeline_configs):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=pipeline_configs['simple_pipeline'])
            # ensure not cached from previous run (config should be none until
            # load)
            assert pipeline_wrapper.dag_config is None
            pipeline_wrapper.load()  # Load pipeline + config from db or cache
            assert pipeline_wrapper.dag_config is not None

            G = pipeline_wrapper.execution_graph
            assert type(G) == DiGraph

            # Ensure the loaded value is the same as creating from config
            G2 = get_execution_graph(pipeline_wrapper.dag_config)
            assert G.graph == G2.graph

            mock_redis.flushall()

    def test_pipeline_run_wrapper_increment_retry(self, mock_redis,
                                                  pipeline_configs):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            pipeline_wrapper = PipelineRunWrapper(
                pipeline_id=self.pipeline_id,
                pipeline_config=pipeline_configs['simple_pipeline'])
            # Verify starts w/ defaults
            assert pipeline_wrapper.retry_count == 0
            assert pipeline_wrapper.retry_exceeded is False
            assert pipeline_wrapper.max_retry == 3
            pipeline_wrapper.load()
            pipeline_wrapper.load()  # Verify is_retry=False
            assert pipeline_wrapper.good_to_go
            assert pipeline_wrapper.loading_message == "Loaded Successfully."
            assert pipeline_wrapper.retry_count == 0  # Didn't change

            # Default behavior will automatically cache this so count remains
            pipeline_wrapper.increment_retry()
            assert pipeline_wrapper.retry_count == 1
            assert pipeline_wrapper.retry_exceeded is False

            # This load increments the retry count.
            pipeline_wrapper.load(is_retry=True)
            assert pipeline_wrapper.retry_count == 2
            assert pipeline_wrapper.retry_exceeded is False

            # Make this exceed it's max retry count
            pipeline_wrapper.increment_retry(exceed_max=True)
            assert pipeline_wrapper.retry_count == 4
            assert pipeline_wrapper.retry_exceeded is True

            # Test the deadletter upon exceeding max retry
            # TODO Improve this to actually verify self.deadletter() is called
            pipeline_wrapper.load()
            assert not pipeline_wrapper.good_to_go
            assert "Attempted to retry" in pipeline_wrapper.loading_message
            mock_redis.flushall()


class TestUtilsTaskPipelineGenerator:
    """ Test classes in task_utils.py
    """
    pipeline_id = 'simple-pipeline'
    api_url_base = _generate_api_url('pipelines')

    @responses.activate
    def test_pipeline_generator_init(self, mock_redis, pipeline_configs_api):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='pipelines')
            responses.add(
                responses.GET,
                url=urljoin(api_url + '/', self.pipeline_id),
                json=pipeline_configs_api['standard_pipeline_single'])
            gen = PipelineGenerator(pipeline_id=self.pipeline_id,
                                    access_key='123abc')
            assert gen.is_retry is False
            assert gen.pipeline_wrapper.retry_count == 0
            assert gen.good_to_go is True
            assert gen.queue == 'default-test-task-queue'
            assert gen.default_task_ttl == DEFAULT_TASK_TTL
            assert gen.regulator_queue == 'default-test-task-queue'
            assert gen.regulator_task == DEFAULT_REGULATOR_TASK
            assert gen.pipeline_wrapper.chain_payload == {}

            # Second instantiation in a row doesn't change retry count
            gen = PipelineGenerator(pipeline_id=self.pipeline_id,
                                    access_key='123abc')
            assert gen.is_retry is False
            assert gen.pipeline_wrapper.retry_count == 0

            # Instantiation w/ execution id provided turns this into a retry
            # Also test overriding some default values.
            gen = PipelineGenerator(self.pipeline_id,
                                    access_key='123abc',
                                    execution_id='456',
                                    default_task_ttl=10,
                                    chain_payload={'custom_key1': 'val1'})
            assert gen.is_retry is True
            assert gen.pipeline_wrapper.retry_count == 1
            assert gen.pipeline_wrapper.chain_payload == {
                'custom_key1': 'val1'
            }
            assert gen.queue == 'default-test-task-queue'
            assert gen.default_task_ttl is 10
            assert gen.regulator_task is DEFAULT_REGULATOR_TASK

            mock_redis.flushall()

    @responses.activate
    def test_pipeline_generator_internal_get_regulator(self, mock_redis,
                                                       pipeline_configs_api):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            responses.add(responses.GET,
                          url=urljoin(self.api_url_base + '/',
                                      self.pipeline_id),
                          json=pipeline_configs_api['simple_pipeline'])
            gen = PipelineGenerator(
                self.pipeline_id,
                access_key='123abc',
            )
            regulator = gen._get_regulator()
            assert type(regulator) == Signature
            assert regulator.task == DEFAULT_REGULATOR_TASK
            assert regulator.options['queue'] == 'default-test-task-queue'

            mock_redis.flushall()

    @responses.activate
    def test_pipeline_generator_internal_get_signature(self, mock_redis,
                                                       pipeline_configs_api):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='pipelines')
            responses.add(responses.GET,
                          url=urljoin(api_url + '/', self.pipeline_id),
                          json=pipeline_configs_api['simple_pipeline'])
            gen = PipelineGenerator(self.pipeline_id, access_key='123abc')
            G = gen.pipeline_wrapper.execution_graph
            for node in G.nodes:
                if node == 'entry1':
                    node1 = node
                    break
            signature = gen._get_signature(node1)
            node1_def = gen.pipeline_wrapper.pipeline_config[
                'taskDefinitions'][node1]
            assert type(signature) == Signature
            assert signature.options['queue'] == 'default-test-task-queue'
            assert signature.options['soft_time_limit'] == 30  # Non default
            assert signature.task == node1_def['handler']

            mock_redis.flushall()

    @responses.activate
    def test_pipeline_generator_generate_chain(self, mock_redis,
                                               pipeline_configs_api):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='pipelines')
            responses.add(responses.GET,
                          url=urljoin(api_url + '/', self.pipeline_id),
                          json=pipeline_configs_api['simple_pipeline'])
            keys = mock_redis.keys()
            gen = PipelineGenerator(self.pipeline_id, access_key='123abc')
            chain = gen.generate_chain()
            assert type(chain) == _chain
            assert type(chain.tasks[0]) == chord

            # The first task in the chain should comprise the two entrypoint
            # tasks from our simple-pipeline fixture (entry1 and fulltext)
            # Check a few custom properties set on these.
            keys = mock_redis.keys()

            assert chain.tasks[0].tasks[0].name == \
                'sermos.tasks.task_temp_entry1'
            assert type(chain.tasks[0]) == chord
            assert chain.tasks[0].tasks[1].name ==\
                'sermos.tasks.task_temp_fulltext'

            # Test a 'not good to go' generation.
            with mock.patch.dict(os.environ, {
                'SERMOS_BASE_URL': 'local',
                'SERMOS_CLIENT_PKG_NAME': 'pypeline',
                'SERMOS_YAML_PATH': '../tests/fixtures/configs/sermos-valid.yaml'
            }):
                reload(constants)
                reload(config_utils)
                reload(sermos_yaml)
                from pypeline.constants import DEFAULT_BASE_URL
                with pytest.raises(ValueError):
                    gen = PipelineGenerator('foo', access_key='bar')

            reload(constants)
            reload(config_utils)
            reload(sermos_yaml)
            mock_redis.flushall()

    @responses.activate
    def test_pipeline_generator_load_from_cache(self, mock_redis,
                                                pipeline_configs_api):
        fake_redis = mock.patch.object(config_utils, 'redis_conn', mock_redis)
        with fake_redis:
            api_url = _generate_api_url(endpoint='pipelines')
            responses.add(responses.GET,
                          url=urljoin(api_url + '/', self.pipeline_id),
                          json=pipeline_configs_api['simple_pipeline'])
            keys = mock_redis.keys()
            chain_payload = {'custom_key1': 'val1', 'custom_key2': 'val2'}
            gen = PipelineGenerator(self.pipeline_id,
                                    access_key='123abc',
                                    chain_payload=chain_payload)
            chain = gen.generate_chain()
            assert type(chain) == _chain
            assert type(chain.tasks[0]) == chord
            assert gen.pipeline_wrapper.chain_payload == chain_payload

            # Now try to load the wrapper directly from cache and verify
            # the chain payload is intact.
            run_wrapper = PipelineRunWrapper(pipeline_id=self.pipeline_id,
                                             execution_id=gen.execution_id)
            assert run_wrapper.chain_payload == {}
            run_wrapper.load()
            assert run_wrapper.chain_payload == chain_payload

            mock_redis.flushall()

    def test_task_signature_queue_from_sermos_config(self):
        """ TODO Write a test that shows you can specify the queue for any
            given registered task in the sermos.yaml file.
        """
        pass

    def test_task_signature_queue_from_pipeline_config(self):
        """ TODO Write a test that shows you can specify the queue for any
            given registered task in the pipeline config yaml and that it
            will override a value specified in sermos.yaml.
        """
        pass

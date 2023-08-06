""" Tests for the
"""
import json
import pytest
from marshmallow.exceptions import ValidationError
from pypeline.pipeline_config_schema import PipelineSchemaV1


class TestPipelines:
    """ Test Pipelines and Graphs

    TODO: Need to really beef up tests here.
    """

    with open('tests/fixtures/api/demo_pipeline_conf_simple.json', 'r') as f:
        simple_pipeline = json.loads(f.read())

    with open('tests/fixtures/api/demo_pipeline_conf_invalid.json', 'r') as f:
        invalid_pipeline = json.loads(f.read())

    def test_pipeline_tasks(self):
        """ Valid pipeline configuration
        """
        # When a pipeline is invoked, it dynamically generates
        # all of the PipelineTask objects for 'this' run
        pcs = PipelineSchemaV1()
        pipeline = pcs.load(
            self.simple_pipeline['data'])  # Verify it doesn't blow up

        # Assert some basics about the config to ensure it loaded correctly
        assert pipeline['description'] == 'Simple pipeline demo.'
        assert pipeline['config']['dagAdjacency']['entry1'][0] == \
            'consistent_hash'
        assert pipeline['config']['taskDefinitions']['fulltext']['queue'] == \
            'default'

    def test_invalid_pipeline_config(self):
        """ Invalid pipeline configuration will throw an exception
        """
        with pytest.raises(ValidationError):
            pcs = PipelineSchemaV1()
            pcs.load(self.invalid_pipeline)

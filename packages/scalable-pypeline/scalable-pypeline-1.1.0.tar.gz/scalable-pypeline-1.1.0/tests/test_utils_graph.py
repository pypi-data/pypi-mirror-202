""" Test graph utilities
"""
from unittest import mock
from networkx.classes.digraph import DiGraph
from pypeline.utils.task_utils import *
from pypeline.utils.graph_utils import *


class TestUtilsGraph:
    """ Test classes in task_graph.py
    """

    pipeline_id = 'simple-pipeline'

    def test_graph_get_execution_graph(self, mock_redis, pipeline_configs):
        """ Test get_execution_graph()
        """
        pipeline_config = pipeline_configs['simple_pipeline']

        # Normal operation on valid config
        graph = get_execution_graph(pipeline_config)
        assert type(graph) is DiGraph
        assert len(graph.nodes) == 5

        # Empty graph
        graph = get_execution_graph({})
        assert len(graph.nodes) == 0

        # Adjacency key provided does not have any tasks defined
        graph = get_execution_graph(pipeline_config, adjacency_key='foobar')
        assert len(graph.nodes) == 0

    def test_graph_find_entrypoint(self, mock_redis, pipeline_configs):
        """ Test find_entry_points()
        """
        pipeline_config = pipeline_configs['simple_pipeline']

        # The simple-pipeline has two entrypoints
        graph = get_execution_graph(pipeline_config)
        entrypoints = find_entry_points(graph)
        assert type(entrypoints) == list
        assert entrypoints[0] == 'entry1'
        assert entrypoints[1] == 'fulltext'

    def test_graph_find_successors(self, mock_redis, pipeline_configs):
        """ Test find_successors()
        """
        pipeline_config = pipeline_configs['long_pipeline']

        # The simple-pipeline has two entrypoints
        graph = get_execution_graph(pipeline_config)
        entrypoints = find_entry_points(graph)
        assert len(entrypoints) == 1
        assert entrypoints[0] == 'entry1'

        # Initial successor of the graph after entrypoint
        successors = find_successors(graph, entrypoints)
        assert type(successors) == list
        assert successors == ['downstream1']

        successors = find_successors(graph, ['downstream1'])
        assert type(successors) == list
        assert successors == ['downstream2']

        # Ensure it can properly handle a string instead of list for
        # starting node.
        successors = find_successors(graph, 'downstream2')
        assert type(successors) == list
        assert successors == ['downstream3']

    def test_graph_find_successors_non_dedup(self, mock_redis,
                                             pipeline_configs):
        """ Test find_successors() with deduplication turned off
        """
        pipeline_config = pipeline_configs['simple_pipeline']

        graph = get_execution_graph(pipeline_config)

        # Test WITH deduplication
        successors = find_successors(graph, ['entry1', 'fulltext'])
        assert successors == ['consistent_hash', 'date_extraction']

        # Test WITHOUT deduplication
        successors =\
            find_successors(graph, ['entry1', 'fulltext'], dedup=False)
        assert successors == [['consistent_hash'],
                              ['date_extraction', 'consistent_hash']]

    def test_graph_get_chainable_tasks(self, mock_redis, pipeline_configs):
        """ Test get_chainable_tasks()
        """
        # Try against `simple-pipeline`
        pipeline_config = pipeline_configs['simple_pipeline']
        graph = get_execution_graph(pipeline_config)
        chained_tasks = get_chainable_tasks(graph, None, [])
        expected_chain = [['entry1', 'fulltext'],
                          ['consistent_hash', 'date_extraction'],
                          ['custom_webhook']]
        assert chained_tasks == expected_chain

        # Try against `long-pipeline`
        pipeline_config = pipeline_configs['long_pipeline']
        graph = get_execution_graph(pipeline_config)
        chained_tasks = get_chainable_tasks(graph, None, [])
        expected_chain = [['entry1'], ['downstream1'], ['downstream2'],
                          ['downstream3'], ['downstream4'], ['downstream5'],
                          ['downstream6']]
        assert chained_tasks == expected_chain

    def test_graph_find_all_nodes(self, mock_redis, pipeline_configs):
        """ Test find_all_nodes()
        """
        pipeline_config = pipeline_configs['long_pipeline']

        # The simple-pipeline has two entrypoints
        graph = get_execution_graph(pipeline_config)
        nodes = find_all_nodes(graph)
        assert len(nodes) == 7
        assert nodes[2] == 'downstream2'

    def test_graph_find_all_edges(self, mock_redis, pipeline_configs):
        """ Test find_all_edges()
        """
        pipeline_config = pipeline_configs['long_pipeline']

        # The simple-pipeline has two entrypoints
        graph = get_execution_graph(pipeline_config)
        edges = find_all_edges(graph)
        assert len(edges) == 6
        assert edges[2] == ('downstream2', 'downstream3')

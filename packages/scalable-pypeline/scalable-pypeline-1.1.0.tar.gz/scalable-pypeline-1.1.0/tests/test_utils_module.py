""" Test pypeline configuration utilities
"""
import os
import re
import mock
import json
import time
from urllib.parse import urljoin
from types import ModuleType
import pytest
import responses
from pypeline.flask import FlaskSermos
from pypeline.utils.module_utils import SermosModuleLoader, match_prefix, \
    match_suffix, match_prefix_suffix, find_from_environment


class TestModuleUtils:
    """ Test classes in utils/module_utils.py
    """

    prefix_p = "foo"
    suffix_p = "baz"
    p1 = "foobar_baz"
    p2 = "bar_bam"
    p3 = "Foo_bar"
    p4 = "fobar_baz"
    p5 = "foo"

    def test_sermos_module_loader(self):
        """ The module loader helps load modules/classes/methods w/ string
        """
        loader = SermosModuleLoader()

        module = loader.get_module('pypeline.flask.FlaskSermos')
        assert isinstance(module, ModuleType)
        module = loader.get_module('pypeline.flask')
        assert isinstance(module, ModuleType)

        callable_name =\
            loader.get_callable_name('pypeline.flask.FlaskSermos')
        assert callable_name == 'FlaskSermos'

        the_callable = loader.get_callable('pypeline.flask.FlaskSermos')
        assert the_callable == FlaskSermos

    def test_match_prefix(self):
        assert match_prefix(self.p1, self.prefix_p) is True
        assert match_prefix(self.p2, self.prefix_p) is False
        assert match_prefix(self.p3, self.prefix_p) is False
        assert match_prefix(self.p4, self.prefix_p) is False
        assert match_prefix(self.p5, self.prefix_p) is True

    def test_match_suffix(self):
        assert match_suffix(self.p1, self.suffix_p) is True
        assert match_suffix(self.p2, self.suffix_p) is False
        assert match_suffix(self.p3, self.suffix_p) is False
        assert match_suffix(self.p4, self.suffix_p) is True

    def test_match_prefix_suffix(self):
        assert match_prefix_suffix(self.p1, self.prefix_p,
                                   self.suffix_p) is True
        assert match_prefix_suffix(self.p2, self.prefix_p,
                                   self.suffix_p) is False
        assert match_prefix_suffix(self.p3, self.prefix_p,
                                   self.suffix_p) is False
        assert match_prefix_suffix(self.p4, self.prefix_p,
                                   self.suffix_p) is False

    @mock.patch.dict(os.environ, {'foo_ENV_VAR_baz': 'foobar'})
    def test_find_from_environment(self):
        env_variables = find_from_environment(self.prefix_p, self.suffix_p)
        assert len(env_variables) == 1

        env_variables = find_from_environment('doesnt', 'exist')
        assert len(env_variables) == 0

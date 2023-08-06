""" Test the generic utilities.
"""
import os
from importlib import reload
import mock
import pytest
from pypeline import constants
from pypeline.utils import module_utils
from pypeline.utils.module_utils import normalized_pkg_name,\
    get_client_pkg_name


class TestUtils():
    def test_normalized_pkg_name(self):
        """ Verify it normalizes names appropriately
        """
        dashed_version = 'pkg-name'
        under_version = 'pkg_name'

        # Verify default behavior, which will replace any dashes with _
        normalized_dashed = normalized_pkg_name(dashed_version)
        normalized_under = normalized_pkg_name(under_version)
        assert normalized_dashed == normalized_under
        assert '-' not in normalized_dashed
        assert '_' in normalized_dashed

        # Verify 'dashed' behavior
        normalized_dashed = normalized_pkg_name(dashed_version, dashed=True)
        normalized_under = normalized_pkg_name(under_version, dashed=True)
        assert normalized_dashed == normalized_under
        assert '_' not in normalized_dashed
        assert '-' in normalized_dashed

    def test_get_client_pkg_name(self):
        """ Test helper method 'get_client_pkg_name()'

            Client package directory should be the actual directory name and
            not the hyphenated installed package name.

                e.g. my_package
        """
        # Verify it raises ValueError if no access key provided and none in
        # environment.
        with pytest.raises(ValueError):
            pkg_name = get_client_pkg_name()

        # access key returned as-is when provided directly
        pkg_name = get_client_pkg_name('my_package')
        assert pkg_name == 'my_package'

        # access key retrieved from Environment successfully.
        with mock.patch.dict(os.environ,
                             {'SERMOS_CLIENT_PKG_NAME': 'the_pkg'}):
            reload(constants)
            reload(module_utils)
            pkg_name = get_client_pkg_name()
            assert pkg_name == 'the_pkg'
        reload(constants)
        reload(module_utils)

""" Tests confirming proper sermos.yaml formatting / parsing.
"""
import re
import os
import ast
import pytest
import yaml
import mock
from yaml.loader import FullLoader
from yaml.nodes import ScalarNode
from pypeline.sermos_yaml import InvalidPackagePath, InvalidSermosConfig,\
    MissingSermosConfig, load_sermos_config, YamlPatternConstructor,\
    parse_config_file, InvalidImageConfig, load_client_config_and_version


class TestSermosYaml:
    """ Test classes in sermos/sermos_yaml.py
    """
    invalid_yaml_path = '/fixtures/configs/sermos-invalid-yaml.yaml'
    invalid_format_path = '/fixtures/configs/sermos-invalid-format.yaml'
    invalid_image_path =\
        '/fixtures/configs/sermos-invalid-mismatched-custom-image.yaml'
    invalid_name_path =\
        '/fixtures/configs/sermos-invalid-name-format.yaml'
    invalid_missing_required_for_type =\
        '/fixtures/configs/sermos-invalid-missing-required-for-type.yaml'
    valid_yaml_path = '/fixtures/configs/sermos-valid.yaml'
    valid_yaml_path_with_env =\
        '/fixtures/configs/sermos-valid-with-env.yaml'
    valid_empty_yaml_path = '/fixtures/configs/sermos-valid-empty.yaml'

    with open('tests' + invalid_format_path, 'r') as f:
        raw_invalid_file = f.read()
    with open('tests' + valid_yaml_path, 'r') as f:
        raw_file = f.read()

    # Load this before using load_sermos_config() so we don't add the
    # yaml constructor when loading the 'raw config'
    raw_config = yaml.load(raw_file, Loader=yaml.FullLoader)
    valid_config = load_sermos_config(__name__, valid_yaml_path)

    # TODO review the whole notion of the client version and what we do/don't need/expect
    def test_sermos_load_client_config_and_version(self):
        """ Helper function to load both client config and client pkg version
        """
        config, version = load_client_config_and_version(
            'pypeline', '../' + self.valid_yaml_path)
        _version_re = re.compile(r'__version__\s+=\s+(.*)')
        with open('pypeline/__init__.py', 'rb') as f:
            __version__ = str(
                ast.literal_eval(
                    _version_re.search(f.read().decode('utf-8')).group(1)))

        assert __version__ == version

    def test_sermos_exceptions(self):
        """ Verify some exceptions we provide
        """
        assert issubclass(InvalidPackagePath, Exception)
        assert issubclass(InvalidSermosConfig, Exception)
        assert issubclass(MissingSermosConfig, Exception)

    def test_yaml_env_loader_init(self):
        """ Verify basic YamlPatternConstructor initialization
        """
        # Verify that our test yaml has some non compliant keys that
        # exist in the yaml and are not modified by the yaml.load()
        # before we initialize tye YamlPatternConstructor()
        assert self.raw_config['non_compliant_env_var_key'] == '${MY_FOOBAR}'
        assert self.raw_config['non_compliant_env_var_key_2'] ==\
            '${MY_FOO_DEFAULT:default-value-here}'

        # Verify the default pattern is assigned correctly and that
        # a user could use a custom pattern if desired.
        loader = YamlPatternConstructor(add_constructor=False)
        assert loader.env_var_pattern == r'^\$\{(.*)\}$'
        assert type(loader.path_matcher) == re.Pattern
        custom_pattern_loader = YamlPatternConstructor(r'\%(\w)\%',
                                                       add_constructor=False)
        assert custom_pattern_loader.env_var_pattern == r'\%(\w)\%'

    def test_yaml_env_loader_constructor(self):
        """ Verify YamlPatternConstructor's _path_constructor() method
        """
        loader = YamlPatternConstructor(add_constructor=False)
        fl = FullLoader('')  # No actual loaded stream required

        # Test that a node matching the default env variable pattern
        # but without that env var in environment returns as None
        node = ScalarNode('!env_var', '${FOO}')
        resolved_val = loader._path_constructor(fl, node)
        assert resolved_val == 'unset'

        # Verify returns correctly if in environment
        # Basic initialization with environment
        with mock.patch.dict(os.environ, {'FOO': 'bar'}):
            resolved_val = loader._path_constructor(fl, node)
            assert resolved_val == 'bar'

        # Test that a node matching the default env variable pattern
        # but without that env var in environment returns as None
        # Make sure to keep in the characters common in db urls, etc.
        node = ScalarNode('!env_var', '${FOO:my-default:/val@here}')
        resolved_val = loader._path_constructor(fl, node)
        assert resolved_val == 'my-default:/val@here'

    def test_yaml_env_loader_yaml_init(self):
        """ Test functionality of sermos yaml env loader that allows
            the yaml parser to inject variables from environment
        """
        with open('tests' + self.valid_yaml_path_with_env, 'r') as f:
            raw_config = yaml.load(f.read(), Loader=yaml.FullLoader)

        # Validate that the yaml loading parser works, which includes ability
        # to interpret default values for our environment variable format.
        assert raw_config['non_compliant_key'] == 'foobar'
        assert raw_config['non_compliant_env_var_key'] == 'unset'
        assert raw_config['non_compliant_env_var_key_2'] ==\
            'default-value-here'
        env_vars = raw_config['serviceConfig'][1]['environmentVariables']
        assert env_vars[0]['value'] == 'something-specific-to-special-worker'
        assert env_vars[2]['value'] == 'default-val:here/foo'

        # Assert utils will add 'unset' to environment variable values
        # that are templated without a default.
        config = load_sermos_config(__name__, self.valid_yaml_path_with_env)
        env_vars = config['serviceConfig'][1]['environmentVariables']
        assert env_vars[0]['value'] == 'something-specific-to-special-worker'
        assert env_vars[1]['value'] == 'unset'

        # Assert non compliant keys don't exist
        assert 'non_compliant_key' not in config
        assert 'non_compliant_env_var_key' not in config
        assert 'non_compliant_env_var_key_2' not in config

        # Confirm environment variables are rendered correctly
        # when actually available in environment
        with mock.patch.dict(os.environ, {
                'SECRET_VAR': 'my-super-secret/url@password:5290',
        }):
            config = load_sermos_config(__name__,
                                        self.valid_yaml_path_with_env)
        raw_env_vars_list =\
            raw_config['serviceConfig'][1]['environmentVariables']
        env_vars_list =\
            config['serviceConfig'][1]['environmentVariables']
        assert raw_env_vars_list[0] == env_vars_list[0]
        assert raw_env_vars_list[1] != env_vars_list[1]
        assert env_vars_list[1]['value'] == 'my-super-secret/url@password:5290'
        assert env_vars_list[2]['value'] == 'default-val:here/foo'
        assert env_vars_list[3]['value'] == '$foo:invalid-format}'
        assert env_vars_list[4]['value'] == '1.*.*'

    def test_load_sermos_config_exception_modes(self):
        """ Test the loading of the sermos.yaml config file from a base
            package and catching all the known exception modes.
        """

        # Assert that invalid package name / config relative path results
        # in InvalidPackagePath
        with pytest.raises(InvalidPackagePath):
            load_sermos_config('bad_pkg_name', None)

        # Assert that the config doesn't exist in the base sermos package.
        with pytest.raises(MissingSermosConfig):
            load_sermos_config('pypeline')

        # Assert that invalid (but existing) config throws InvalidSermosConfig
        # When the yaml format is all wonky
        with pytest.raises(InvalidSermosConfig) as e:
            load_sermos_config(__name__, self.invalid_yaml_path)
        assert "Invalid Sermos configuration, likely due to" in str(e.value)

        # Assert that invalid (but existing) config throws InvalidSermosConfig
        # When the yaml format is correct but the config itself is missing
        # required keys.
        with pytest.raises(InvalidSermosConfig) as e:
            load_sermos_config(__name__, self.invalid_format_path)
        assert "Invalid Sermos configuration due to" in str(e.value)

        # Assert the parse_config_file() method will raise when invalid, and
        # not raise when valid.
        with pytest.raises(InvalidSermosConfig) as e:
            parse_config_file(self.raw_invalid_file)
        parse_config_file(self.raw_file)

        # Assert that, when a custom image is defined in a registered task,
        # Sermos yells if that image name does not match any known/defined
        # custom images
        with pytest.raises(InvalidImageConfig) as e:
            load_sermos_config(__name__, self.invalid_image_path)

    def test_load_sermos_invalid_missing_required(self):
        """ Verify that we properly validate required keys based on service type
        """
        with pytest.raises(InvalidSermosConfig) as e:
            load_sermos_config(__name__,
                               self.invalid_missing_required_for_type)

    def test_load_sermos_invalid_name_format(self):
        """ Verify that we properly validate required name format
        """
        with pytest.raises(InvalidSermosConfig) as e:
            load_sermos_config(__name__, self.invalid_name_path)

    def test_load_sermos_valid_config(self):
        """ Test the loading of a valid sermos.yaml config file
        """
        config = load_sermos_config(__name__, self.valid_yaml_path)

        # Assert that keys not explicitly allowed for in the SermosYamlSchema
        # do not pass through to the parsed config.
        assert 'non_compliant_key' not in config

        # Verify that the non_compliant_key is indeed in the raw .yaml file
        # we're testing
        assert 'non_compliant_key' in self.raw_file

    def test_load_sermos_valid_empty_config(self):
        """ Test the loading of a valid but empty sermos.yaml config file
        """
        config = load_sermos_config(__name__, self.valid_empty_yaml_path)

        # Assert that keys not explicitly allowed for in the SermosYamlSchema
        # do not pass through to the parsed config.
        assert 'non_compliant_key' not in config

        # Verify that the non_compliant_key is indeed in the raw .yaml file
        # we're testing
        assert 'non_compliant_key' in self.raw_file

    def test_load_sermos_valid_config_include_exclude(self):
        """ Verify some keys we know should be in the valid config and some
            known foobar keys in test file that should be excluded
        """
        config = load_sermos_config(__name__, self.valid_yaml_path)

        # Verify environmentVariables are preserved at top level
        assert 'environmentVariables' in config
        assert len(config['environmentVariables'])\
            == len(self.raw_config['environmentVariables'])

        # Verify environmentVariables are preserved at worker level
        workers = config['serviceConfig']
        raw_workers = self.raw_config['serviceConfig']
        assert 'environmentVariables' in workers[1]
        assert len(workers[1]['environmentVariables'])\
            == len(raw_workers[1]['environmentVariables'])

    def test_load_sermos_valid_config_env_vars(self):
        """ Verify environmentVariables behavior
        """
        # Basic initialization with environment
        config = load_sermos_config(__name__, self.valid_yaml_path)

        raw_workers = self.raw_config['serviceConfig']
        raw_tasks = self.raw_config['serviceConfig'][0]['registeredTasks']
        parsed_workers = config['serviceConfig']
        parsed_tasks = config['serviceConfig'][0]['registeredTasks']

        # Assert there are no environment variables provided for first worker
        assert 'environmentVariables' not in parsed_workers[0]
        # Verify that environmentVariables come through in each worker
        raw_env = raw_workers[1]['environmentVariables']
        parsed_env = parsed_workers[1]['environmentVariables']
        # assert parsed_env == raw_env
        assert parsed_env[0]['name'] == raw_env[0]['name']

        # Assert correct behavior when environment variables
        # that are defined in the sermos.yaml are NOT available
        # in the environment during load time but have a default.
        #
        raw_env_with_default = raw_workers[1]['environmentVariables'][1]
        parsed_env_with_default = parsed_workers[1]['environmentVariables'][1]
        assert raw_env_with_default['value'] ==\
            '${SECRET_FROM_ENV_WITH_DEFAULT:default-val:here/foo}'

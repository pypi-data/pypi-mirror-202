""" Test SermosDeploy() and supporting classes/methods.
"""
import os
import base64
import subprocess
import json
from importlib import reload
import pytest
import mock
import responses
import yaml
from pypeline import constants
from pypeline.constants import DEPLOYMENTS_DEPLOY_URL, DEPLOYMENTS_SERVICES_URL,\
    DEFAULT_BASE_URL
from pypeline import deploy
from pypeline.deploy import SermosDeploy
from pypeline import cloud
from pypeline.sermos_yaml import InvalidPackagePath
from pypeline.utils import module_utils


class TestSermosDeploy:
    """ Test deployment utilities.

    TODO Make the patched DEFAULT_BASE_URL process more repeatable through
    either a setup/teardown mechanism or some reusable code we can use
    in other tests instead of this copy/paste stuff. Also used in
    tests/test_flask_decorators.py
    """
    sermos_yaml_filename = '/fixtures/configs/sermos-valid.yaml'

    with open('tests/fixtures/api/deployment_status_response.json', 'r') as f:
        deployment_status_response = json.loads(f.read())

    def test_sermos_deploy_init(self):
        """ Test basic initialization of SermosDeploy()
        """
        # Should fail if no access key / client pkg dir provided and not
        # available in environment
        with pytest.raises(KeyError):
            sd = SermosDeploy()

        # Basic initialization by manually passing params
        sd = SermosDeploy(deployment_id='abc-123-8710',
                          access_key='foo',
                          pkg_name='my_pkg')
        assert sd.access_key == 'foo'
        assert sd.pkg_name == 'my_pkg'
        assert sd.commit_hash is None
        assert sd.deploy_url == DEPLOYMENTS_DEPLOY_URL.format(
            DEFAULT_BASE_URL, 'abc-123-8710')
        assert sd.headers == {
            'Content-Type': 'application/json',
            'apikey': 'foo'
        }

        # Basic initialization with environment
        with mock.patch.dict(os.environ, {
                'SERMOS_ACCESS_KEY': 'bar',
                'SERMOS_CLIENT_PKG_NAME': 'my_other_pkg',
        }):
            reload(constants)
            reload(module_utils)
            sd = SermosDeploy()
            assert sd.access_key == 'bar'
            assert sd.pkg_name == 'my_other_pkg'
        reload(constants)
        reload(module_utils)

    def test_sermos_deploy_set_commit_hash(self):
        """ Test ability to set current git commit hash
        """
        sd = SermosDeploy(access_key='foo', pkg_name='my_pkg')
        current_commit_hash = subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"]).strip().decode('utf-8')
        sd._set_commit_hash()
        assert sd.commit_hash == current_commit_hash

        # Verify you can override commit hash if you want a specific hash
        # that is not 'current'
        sd = SermosDeploy(access_key='foo',
                          pkg_name='my_pkg',
                          commit_hash='123')
        sd._set_commit_hash()
        assert sd.commit_hash != current_commit_hash
        assert sd.commit_hash == '123'

    def test_sermos_deploy_set_encoded_sermos_yaml(self, test_data_dir):
        """ Test retrieval/setting of the sermos yaml file and proper encoding
        """
        # Won't find a sermos.yaml file here...
        sd = SermosDeploy(access_key='foo', pkg_name='my_pkg')
        with pytest.raises(InvalidPackagePath):
            sd._set_encoded_sermos_yaml()

        # Get an actual yaml loading
        sd = SermosDeploy(access_key='foo',
                          pkg_name=__name__,
                          sermos_yaml_filename=self.sermos_yaml_filename)

        # Verify the encoded yaml starts as None and is then loaded.
        assert sd.encoded_sermos_yaml is None
        sd._set_encoded_sermos_yaml()
        assert sd.encoded_sermos_yaml is not None

        # Verify the encoded value is indeed encoded and that it can be
        # properly decoded / match what's on disk.
        with open('tests' + self.sermos_yaml_filename, 'r') as f:
            raw_sermos_yaml = f.read()
        loaded = yaml.load(sd.encoded_sermos_yaml, Loader=yaml.FullLoader)
        assert 'name' not in loaded  # This is an encoded string, so no keys
        # # Decode the encoded yaml
        decoded_yaml = base64.b64decode(sd.encoded_sermos_yaml).decode('utf-8')
        loaded = yaml.load(decoded_yaml, Loader=yaml.FullLoader)
        assert 'imageConfig' in loaded  # This is now a valid yaml again, keys back

    def test_sermos_deploy_set_deploy_payload(self):
        """ Verify the payload looks correct.
        """
        sd = SermosDeploy(access_key='foo',
                          pkg_name=__name__,
                          sermos_yaml_filename=self.sermos_yaml_filename)
        assert sd.deploy_payload is None
        sd._set_deploy_payload()
        assert sd.deploy_payload is not None
        assert list(sd.deploy_payload.keys()) == [
            'sermos_yaml', 'commit_hash', 'deploy_branch',
            'client_package_name'
        ]

    @responses.activate
    def test_sermos_deploy_get_deployment_status(self):
        """ Test status retrieval.
        """
        # Run test with a 'non local' base url, which is going to run as
        # though there is a Cloud API endpoint available.
        with mock.patch.dict(os.environ, {'SERMOS_BASE_URL': 'https://f.bar'}):
            reload(constants)
            reload(cloud)
            reload(deploy)
            from pypeline.constants import DEFAULT_BASE_URL  # Re-import
            from pypeline.deploy import SermosDeploy

            # Set up the mock response that catches the API call.
            status_response = {
                'data': {
                    'results': [{
                        'service_id': 'witty-lynx-baa91b',
                        'name': 'local-redis',
                        'status': 'active'
                    }]
                },
                'message': 'Status of all Deployment Services'
            }

            mock_url = DEPLOYMENTS_SERVICES_URL.format(DEFAULT_BASE_URL,
                                                       'abc-123-8710')

            responses.add(responses.GET,
                          mock_url,
                          json=self.deployment_status_response,
                          status=200)

            # Verify a basic, successful retrieval
            sd = SermosDeploy(access_key='foo', pkg_name='my_pkg')
            status = sd.get_deployment_status()
            assert status == status_response

        # RELOAD after context
        reload(constants)
        reload(cloud)
        reload(deploy)

    @responses.activate
    def test_sermos_deploy_invoke_deployment(self):
        """ Test deployment invocation.
        """
        # Run test with a 'non local' base url, which is going to run as
        # though there is a Cloud API endpoint available.
        with mock.patch.dict(os.environ, {'SERMOS_BASE_URL': 'https://f.bar'}):
            reload(constants)
            reload(cloud)
            reload(deploy)
            from pypeline.constants import DEFAULT_BASE_URL  # Re-import
            from pypeline.deploy import SermosDeploy

            deploy_url = DEPLOYMENTS_DEPLOY_URL.format(DEFAULT_BASE_URL,
                                                       'abc-123-8710')

            # Set up the mock response that catches the API call.
            mock_response = {
                'status': 200,
                'message': 'Build going on!',
                'deployment_uuid': 'abc-123-8710'
            }
            responses.add(responses.POST,
                          deploy_url,
                          json=mock_response,
                          status=200)

            # Verify a basic, successful invocation
            sd = SermosDeploy(access_key='foo',
                              pkg_name=__name__,
                              sermos_yaml_filename=self.sermos_yaml_filename)
            status = sd.invoke_deployment()
            assert status.json() == mock_response

        # RELOAD after context
        reload(constants)
        reload(cloud)
        reload(deploy)

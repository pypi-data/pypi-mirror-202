""" Test CLI tools provided with Sermos
"""
import responses
from click.testing import CliRunner
from pypeline.cli.deploy import deploy, status


class TestSermosCLITools:

    runner = CliRunner()
    sermos_yaml_filename = 'tests/fixtures/configs/sermos-valid.yaml'

    @responses.activate
    def test_cli_deploy(self):
        """ Test the `deploy` cli tool, registered as `sermos_deploy` in setup
        """
        # Run fails without any access key in environment nor as argument
        # Similarly, no client package directory.
        result = self.runner.invoke(deploy, [])
        assert result.exit_code == 1

    @responses.activate
    def test_cli_status(self):
        """ Test the `status` cli tool, registered as `sermos_status` in setup
        """
        # Run fails without any access key in environment nor as argument
        # and missing required argument pipeline-uuid
        result = self.runner.invoke(status, [])
        assert result.exit_code == 1

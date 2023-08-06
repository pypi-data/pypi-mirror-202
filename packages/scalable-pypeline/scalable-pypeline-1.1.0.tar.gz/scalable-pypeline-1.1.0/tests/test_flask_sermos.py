""" Test Flask Sermos methods
"""
from flask import Flask
from pypeline.logging_config import setup_logging
from pypeline.extensions import sermos_config
from pypeline.flask import oidc
from pypeline.constants import DEFAULT_OPENAPI_CONFIG, DEFAULT_RHOAUTH_CONFIG
from pypeline import __version__


class TestFlaskSermos:
    """ Test classes in flask/flask_sermos.py
    """
    def test_flask_sermos(self):
        """ Test basic initialization
        """
        from pypeline.flask import FlaskSermos
        app = Flask(__name__)
        fs = FlaskSermos()
        fs.init_app(app)
        assert isinstance(app, Flask)

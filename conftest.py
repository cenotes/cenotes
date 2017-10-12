import pytest
from cenotes import create_app
from config_backend import Testing


@pytest.fixture
def app():
    app = create_app(app_settings=Testing)
    return app

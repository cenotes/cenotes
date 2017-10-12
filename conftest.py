import pytest
from cenotes import create_app, utils
from config_backend import Testing


@pytest.fixture
def app():
    return create_app(app_settings=Testing)


@pytest.fixture(scope="session", name="testing_key")
def _key():
    return utils.craft_key_from_password("testing")


@pytest.fixture(scope="session", name="testing_box")
def _box(testing_key):
    return utils.craft_secret_box(testing_key)

from medium_scraper import create_app
import pytest
from medium_scraper.config import Config


@pytest.fixture(scope='module')
def test_client_without_autocomplete():
    config = Config
    config.RUN_AUTOCOMPLETER = False
    flask_app = create_app(config)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def test_client_with_autocomplete():
    config = Config
    config.RUN_AUTOCOMPLETER = True
    flask_app = create_app(config)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
